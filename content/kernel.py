"""Shared execution contract for the real browser and native verification."""
import ast
import asyncio
import base64
import builtins
import contextlib
import inspect
import io
import json
import logging
import os
from pathlib import Path
import shutil
import sys
import tempfile
import traceback
import types

_foundry_emit = None

class OutputLimitError(RuntimeError):
    pass

class Capture(io.StringIO):
    def __init__(self, kind, budget):
        super().__init__()
        self.kind = kind
        self.budget = budget
    def write(self, text):
        remaining = 20000 - self.budget[0]
        if len(text) > remaining:
            if remaining > 0:
                super().write(text[:remaining])
                if _foundry_emit:
                    _foundry_emit(self.kind, text[:remaining])
            self.budget[0] = 20000
            raise OutputLimitError('Output exceeded 20,000 characters. Stop the loop or print fewer values.')
        self.budget[0] += len(text)
        value = super().write(text)
        if _foundry_emit:
            _foundry_emit(self.kind, text)
        return value


def valid_path(name):
    return isinstance(name, str) and bool(name) and not name.startswith('/') and '\\' not in name and all(part not in ('', '.', '..') for part in name.split('/'))


def portable_source(source):
    """The async lessons define main(); only their final top-level call changes."""
    if source.rstrip().endswith('await main()'):
        return source.rstrip()[:-len('await main()')] + 'asyncio.run(main())\n'
    return source


async def execute(payload):
    files = payload['files']
    fixtures = payload.get('fixtures', {})
    binary_fixtures = payload.get('binaryFixtures', {})
    entry = payload.get('entry', 'main.py')
    if entry not in files or len(files) > 12 or not all(valid_path(name) for name in [*files, *fixtures, *binary_fixtures]):
        raise ValueError('Invalid project filenames or missing entry file.')
    if sum(len(text.encode('utf-8')) for text in files.values()) > 100_000:
        raise ValueError('Source exceeds the 100 KB project limit.')
    work = tempfile.mkdtemp(prefix='python-foundry-')
    previous_cwd, previous_argv, previous_path = os.getcwd(), sys.argv, sys.path[:]
    previous_input = builtins.input
    previous_tasks = asyncio.all_tasks()
    previous_handlers, previous_level = logging.root.handlers[:], logging.root.level
    budget = [0]
    stdout, stderr = Capture('stdout', budget), Capture('stderr', budget)
    input_lines = io.StringIO(payload.get('stdin', ''))
    previous_main=sys.modules.get('__main__')
    main_module=types.ModuleType('__main__')
    main_module.__file__=entry
    namespace=main_module.__dict__
    sys.modules['__main__']=main_module
    result = dict(ok=True, stdout='', stderr='', error=None, error_type=None, files=[], check=None)
    def input_line(prompt=''):
        if prompt:
            stdout.write(str(prompt))
        line = input_lines.readline()
        if line == '':
            raise EOFError('Program input has no more lines. Open Program input and arguments under the editor and add the required input.')
        return line.rstrip('\n').rstrip('\r')
    try:
        os.chdir(work)
        for name, text in {**fixtures, **files}.items():
            path = Path(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        for name, data in binary_fixtures.items():
            path = Path(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(base64.b64decode(data, validate=True))
        sys.path.insert(0, work)
        sys.argv = [entry, *payload.get('args', [])]
        builtins.input = input_line
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                code = compile(files[entry], entry, 'exec', flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
                value = eval(code, namespace)
                if inspect.isawaitable(value):
                    await value
            except BaseException as error:
                if not (isinstance(error, SystemExit) and error.code in (None, 0)):
                    result['ok'] = False
                    result['error_type'] = type(error).__name__
                    report = traceback.TracebackException.from_exception(error)
                    frames = [frame for frame in report.stack if frame.filename in files or frame.filename.startswith(work + '/')]
                    result['error'] = (('Traceback (most recent call last):\n' + ''.join(traceback.format_list(frames))) if frames else '') + ''.join(report.format_exception_only())
                    result['error'] = result['error'].replace(work + '/', '')
        result['stdout'], result['stderr'] = stdout.getvalue(), stderr.getvalue()
        check = payload.get('check')
        if check and result['ok']:
            failures = []
            if result['stdout'].rstrip() != check['expected'].rstrip():
                failures.append('Printed output differs from the practice target.')
            behaviour = check.get('behaviour')
            if behaviour:
                function = namespace.get(behaviour['function'])
                if not callable(function):
                    failures.append('Define ' + behaviour['function'] + ' as a callable function.')
                else:
                    for case in behaviour['cases']:
                        try:
                            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                                actual = function(*case['args'])
                            if actual != case['expected']:
                                failures.append(f"{behaviour['function']}({', '.join(map(repr, case['args']))}) returned {actual!r}; expected {case['expected']!r}.")
                        except Exception as error:
                            failures.append(f"{behaviour['function']} raised {type(error).__name__}: {error}")
            result['check'] = {'passed': not failures, 'messages': failures or ['All displayed practice checks passed.']}
        total = 0
        workspace_total = 0
        if payload.get('captureWorkspace'):
            result['workspaceFiles'] = []
        for path in sorted(Path('.').rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts:
                continue
            name = path.as_posix()
            if name in files:
                continue
            size = path.stat().st_size
            if size > 1_000_000:
                result['fileNotice'] = 'A generated file exceeds the 1 MB per-file download limit.'
                if payload.get('captureWorkspace'):result['workspaceIncomplete'] = True
                continue
            data = path.read_bytes()
            record = {'name': name, 'base64': base64.b64encode(data).decode(), 'bytes': len(data)}
            if payload.get('captureWorkspace'):
                if workspace_total + size > 2_000_000 or len(result['workspaceFiles']) >= 12:
                    result['workspaceIncomplete'] = True
                else:
                    workspace_total += size
                    result['workspaceFiles'].append(record)
            if name in binary_fixtures and data == base64.b64decode(binary_fixtures[name]):
                continue
            if name in fixtures and data == fixtures[name].encode('utf-8'):
                continue
            if len(data) > 1_000_000 or total + len(data) > 2_000_000 or len(result['files']) >= 12:
                result['fileNotice'] = 'Some generated files exceed the download limit (1 MB per file, 2 MB total, 12 files). Reduce the file size and run again.'
                continue
            total += len(data)
            result['files'].append(record)
        return result
    finally:
        remaining=[task for task in asyncio.all_tasks() if task not in previous_tasks and task is not asyncio.current_task()]
        for task in remaining:task.cancel()
        if remaining:
            with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
                await asyncio.gather(*remaining,return_exceptions=True)
            result['stdout'],result['stderr']=stdout.getvalue(),stderr.getvalue()
        builtins.input = previous_input
        if previous_main is None:sys.modules.pop('__main__',None)
        else:sys.modules['__main__']=previous_main
        sys.argv, sys.path[:] = previous_argv, previous_path
        for name, module in list(sys.modules.items()):
            if str(getattr(module, '__file__', '')).startswith(work + '/'):
                sys.modules.pop(name, None)
        for handler in logging.root.handlers[:]:
            if handler not in previous_handlers:
                handler.close()
        logging.root.handlers = previous_handlers
        logging.root.setLevel(previous_level)
        os.chdir(previous_cwd)
        shutil.rmtree(work, ignore_errors=True)

if __name__ == '__main__':
    print(json.dumps(asyncio.run(execute(json.load(sys.stdin)))))
