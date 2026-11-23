"""Authoritative Python Foundry curriculum. Run to export the browser catalog."""
import json
import textwrap

modules=[]
lessons=[]

def module(id,title,goal):
    modules.append(dict(id=id,title=title,goal=goal,lessons=[]))

def lesson(id,title,goal,explain,source,before,after,expected,changed,observe,practice,solution,answer,*,fixtures=None,files=None,stdin='',args=None,diagram=None,terminal=None,async_code=False,error=None,refs=None):
    source=textwrap.dedent(source).strip()+'\n'
    solution=textwrap.dedent(solution).strip()+'\n'
    entry='main.py'
    item=dict(id=id,title=title,module=modules[-1]['id'],goal=goal,explain=explain,files=files or {entry:source},entry=entry,focus=before,before=before,after=after,expected=expected,changed=changed,observe=observe,predict='Before running the starter, what will Console show? Explain the step that determines the answer.',practice=practice,practiceFiles={entry:solution.replace(solution,'# Write your practice program here.\n')},solutionFiles={entry:solution},practiceExpected=None,answer=answer,fixtures=fixtures or {},stdin=stdin,args=args or [],diagram=diagram,terminal=terminal,async_code=async_code,expectedError=error,refs=refs or [('Python tutorial','https://docs.python.org/3/tutorial/')])
    item['practiceFiles'][entry]='# Write your practice program here.\n'
    # Practice has its own target and output comparison; arbitrary example edits are never graded.
    item['prerequisites']=[lessons[-1]['id']] if lessons else []
    modules[-1]['lessons'].append(id);lessons.append(item)
    return item

module('first','Your first programs','Run a program, name values and read prepared input.')
lesson('first-program','Print your first message','Run Python and change the text it prints.',[
 'A program is a sequence of instructions. Python executes this program from top to bottom. The editor contains the complete program; you do not need to install Python to run it here.',
 'print("Hello, Python!") calls Python’s print function. The text inside quotes is a string. The quotes mark the string in the source; Console displays the text without the quotes.'
], 'print("Hello, Python!")','Hello, Python!','Hello, Ada!','Hello, Python!\n','Hello, Ada!\n','Find Hello, Ada! in Console. Did the quotation marks appear in the printed message?','In the practice editor, write two print calls: print Welcome on the first line and Ada on the second. Choose Check practice.','print("Welcome")\nprint("Ada")','Each print call ends its output with a new line. Two calls produce two lines.',refs=[('print and other built-ins','https://docs.python.org/3/library/functions.html#print')])
lesson('names','Give a value a name','Change a value and predict which uses of its name change.',[
 'An assignment such as count = 3 binds the name count to a value. Later expressions read the value bound to that name. The equals sign assigns a value; it does not ask whether two values are equal.',
 'Python evaluates the right side of an assignment before binding the name on the left. In count = count + 1, the old value is read, one is added, and count is rebound to the new value.'
],'''count = 3
print(count)
count = count + 1
print(count)''','count = 3','count = 8','3\n4\n','8\n9\n','Compare both printed lines. Which assignment makes the second line one larger?','Write a program that binds total to 12, prints it, adds 5 to total, then prints total again.','total = 12\nprint(total)\ntotal = total + 5\nprint(total)','Rebinding a name changes later reads, not text already printed.',diagram={'kind':'flow','question':'Which value does each read of count use?','parts':['count → 3','print: 3','count → 4','print: 4']})
lesson('arithmetic','Calculate before printing','Distinguish a calculation from the text that describes it.',[
 'Integers are whole numbers. The +, -, * and / operators add, subtract, multiply and divide numeric values. Python performs multiplication before addition unless parentheses change the grouping.',
 'A floating-point number approximates a real number with limited precision. Division with / produces a floating-point result; // gives floor division. Printing a quoted calculation displays text instead of performing arithmetic.'
],'''print(2 + 3 * 4)
print((2 + 3) * 4)
print(7 / 2)
print(7 // 2)''','2 + 3 * 4','2 + 5 * 4','14\n20\n3.5\n3\n','22\n20\n3.5\n3\n','Compare the first two lines to explain the effect of parentheses. The last two lines compare / with // on the same inputs.','Calculate the cost of 3 items at 7 each plus a delivery charge of 4. Print the numeric total, not the calculation as text.','print(3 * 7 + 4)','Multiplication computes 21 before addition computes 25.')
lesson('strings','Build and measure text','Join strings and count their characters.',[
 'A string is an ordered sequence of text characters. The + operator joins two strings. It does not insert spaces automatically; include a space in one of the strings when the output needs one.',
 'len(text) returns the number of characters in a string. A space counts as a character. Later lessons examine why a character count can differ from a file’s byte count.'
],'''first = "Ada"
message = "Hello, " + first
print(message)
print(len(message))''','first = "Ada"','first = "Linus"','Hello, Ada\n10\n','Hello, Linus\n12\n','Find the greeting and its length. Explain why adding two letters to the name adds two to the length.','Join Good, a single space, and morning. Print the joined string and then its length.','message = "Good" + " " + "morning"\nprint(message)\nprint(len(message))','The result Good morning contains 12 characters, including the space.')
lesson('formatting','Put values inside a message','Use an f-string to label numeric output.',[
 'An f-string starts with f before its opening quote. Python evaluates expressions inside braces and inserts their values into the surrounding text.',
 'A format such as :.2f displays a number with two digits after the decimal point. Formatting changes the displayed text; it does not change the original number or turn floating-point arithmetic into exact decimal arithmetic.'
],'''items = 3
price = 2.5
print(f"items: {items}")
print(f"total: {items * price:.2f}")''','items = 3','items = 4','items: 3\ntotal: 7.50\n','items: 4\ntotal: 10.00\n','Find the labels items and total. Why does total change even though price stays unchanged?','Bind name to Ada and score to 9. Print exactly Ada scored 9.','name = "Ada"\nscore = 9\nprint(f"{name} scored {score}")','Expressions inside braces are evaluated; text outside braces is kept as written.')
lesson('input','Read the prepared input','Read input text and convert it before arithmetic.',[
 'Program input below the editor already contains 19 and 23 on separate lines. input() reads one line and returns a string. In this browser, input comes from that field; Python does not open a separate prompt.',
 'int(text) converts integer text to an integer. Adding two strings joins their text, while adding two integers computes a sum. Keep the conversions so the program performs arithmetic.'
],'''left = int(input())
right = int(input())
print(left + right)''','print(left + right)','print(left * right)','42\n','437\n','With Program input unchanged, compare 42 with 437. Which operation changed, and which two values were read?','Keep the prepared input. Read both integers and print the second minus the first.','left = int(input())\nright = int(input())\nprint(right - left)','The prepared values are 19 and 23, so second minus first is 4.',stdin='19\n23\n',refs=[('input','https://docs.python.org/3/library/functions.html#input'),('int','https://docs.python.org/3/library/functions.html#int')])

module('control','Choose and repeat instructions','Use conditions and loops to control which statements run.')
lesson('comparisons','Ask a true-or-false question','Read comparison results as Boolean values.',[
 'A comparison produces True or False, the two Boolean values. == compares values; = assigns a value to a name. The operators <, <=, >, >= and != compare order or inequality.',
 'A boundary value is useful when checking a rule. The example compares the same age with both >= 18 and > 18 so you can see whether 18 itself is accepted.'
],'''age = 18
print(age >= 18)
print(age > 18)
print(age == 18)''','age = 18','age = 19','True\nFalse\nTrue\n','True\nTrue\nFalse\n','Compare the first two results at age 18. Which comparison includes the boundary?','Set count to 5. Print whether count is less than 10 and then whether count equals 0.','count = 5\nprint(count < 10)\nprint(count == 0)','The comparisons produce True and False, in that order.')
lesson('boolean-logic','Combine conditions','Explain when and, or and not produce True.',[
 'and requires both conditions to be true. or requires at least one true condition. not reverses a Boolean value. Parentheses can make the grouping of a rule easier to read.',
 'Python short-circuits and and or: it does not evaluate the second expression when the first already determines the result. The guard x != 0 prevents the division from being evaluated when x is zero.'
],'''age = 20
has_ticket = False
print(age >= 18 and has_ticket)
print(age >= 18 or has_ticket)
x = 0
print(x != 0 and 10 / x > 1)''','has_ticket = False','has_ticket = True','False\nTrue\nFalse\n','True\nTrue\nFalse\n','Explain why changing the ticket changes the and result but not the or result. Why does the final line avoid division by zero?','For age = 16 and has_ticket = True, print whether both age >= 18 and has_ticket hold.','age = 16\nhas_ticket = True\nprint(age >= 18 and has_ticket)','A ticket cannot make the age condition true; and therefore produces False.')
lesson('if','Choose whether a block runs','Use indentation to make a conditional block.',[
 'if checks a condition. A colon starts its block, and four spaces indent the statements in that block. Python runs the indented statements only when the condition is true.',
 'else introduces the alternative block. The final print below is not indented, so it runs after either branch. Keep the indentation when editing the threshold.'
],'''score = 7
if score >= 6:
    print("pass")
else:
    print("retry")
print("finished")''','score = 7','score = 5','pass\nfinished\n','retry\nfinished\n','Which line changes branch, and why does finished appear in both runs?','For temperature = 18, print warm if temperature is at least 20; otherwise print cool.','temperature = 18\nif temperature >= 20:\n    print("warm")\nelse:\n    print("cool")','The condition is false, so the else block prints cool.',diagram={'kind':'branch','question':'Which branch reaches the final print?','parts':['score ≥ 6?','True: print pass','False: print retry','Both: print finished']})
lesson('elif','Order several possible cases','Put a more specific condition before a broader condition.',[
 'elif means else if. Python tests branches in order and runs only the first branch whose condition is true. If none is true, the else block runs.',
 'A score of 90 also satisfies score >= 60. Testing >= 90 first prevents the broader passing condition from hiding the highest category.'
],'''score = 90
if score >= 90:
    print("excellent")
elif score >= 60:
    print("pass")
else:
    print("retry")''','score = 90','score = 75','excellent\n','pass\n','Which conditions are true for 90, and why is only excellent printed?','Classify value = -2 as positive, zero or negative using if, elif and else.','value = -2\nif value > 0:\n    print("positive")\nelif value == 0:\n    print("zero")\nelse:\n    print("negative")','Only the negative branch applies to -2.')
lesson('for','Run a block for each character','Trace the value assigned to a loop variable on each iteration.',[
 'A for loop takes one item at a time from a sequence. A string is a sequence, so for letter in name binds letter to each character in order.',
 'The indented print runs once per character. The unindented final print runs once after the loop, not once per character.'
],'''name = "Ada"
for letter in name:
    print(letter)
print("done")''','name = "Ada"','name = "Lin"','A\nd\na\ndone\n','L\ni\nn\ndone\n','Count the character lines separately from done. What determines the number of loop iterations?','Use a for loop to print each character of Hi on its own line.','for letter in "Hi":\n    print(letter)','The two characters produce two loop iterations.')
lesson('while','Repeat until a condition changes','Update a loop variable so a while loop can finish.',[
 'while checks its condition before each iteration. The example prints the current count and then increases it. Once count is no longer less than 3, the loop ends.',
 'A loop that never makes its condition false can run indefinitely. Stop in this workbench terminates the worker, and a run also has a time limit. Neither control fixes the program; the update inside the loop does.'
],'''count = 0
while count < 3:
    print(count)
    count = count + 1
print("done")''','count < 3','count < 2','0\n1\n2\ndone\n','0\n1\ndone\n','Why is the boundary value excluded? Explain how the assignment makes the loop finish.','Starting at 3, use a while loop to print 3, 2 and 1, then print go.','count = 3\nwhile count > 0:\n    print(count)\n    count = count - 1\nprint("go")','Decreasing count eventually makes count > 0 false.')

lesson('break-continue','Skip an item or stop a loop','Distinguish continue from break in the same loop.',[
 'continue skips the remainder of the current iteration and moves to the next item. break exits the nearest loop entirely.',
 'The starter skips the question mark, prints the next letter, and stops at the exclamation mark. Statements after break’s loop can still run; break does not end the entire program.'
],'''for letter in "A?B!C":
    if letter == "?":
        continue
    if letter == "!":
        break
    print(letter)
print("done")''','"A?B!C"','"A?BC!"','A\nB\ndone\n','A\nB\nC\ndone\n','Which character causes only one iteration to be skipped, and which prevents all later letters from being visited?','Loop over "a?b", skip ? with continue, and print each remaining character on its own line.','for letter in "a?b":\n    if letter == "?":\n        continue\n    print(letter)','continue skips the marker while allowing the following b to be processed.')

module('collections','Store groups of values','Choose and update lists, tuples, dictionaries and sets.')
lesson('lists','Keep values in order','Iterate over a list and compute a total.',[
 'A list stores an ordered group of values inside square brackets. A for loop visits those values in order. sum(values) adds numeric values; len(values) counts items.',
 'The same list is used by the loop, sum and len. Changing an element changes the printed item and the sum, while the number of items stays the same.'
],'''values = [4, 7, 2]
for value in values:
    print(value)
print("total", sum(values))
print("count", len(values))''','[4, 7, 2]','[4, 9, 2]','4\n7\n2\ntotal 13\ncount 3\n','4\n9\n2\ntotal 15\ncount 3\n','Separate the total from the item count. Which quantity changes when 7 becomes 9?','Create a list containing 2, 4 and 6. Print its sum and its length on separate lines.','values = [2, 4, 6]\nprint(sum(values))\nprint(len(values))','The sum is 12 and the list contains 3 items.')
lesson('index-slice','Select an item or a slice','Use zero-based indexes and an excluded slice endpoint.',[
 'List indexes start at zero: values[0] is the first item. A negative index counts backward from the end, so values[-1] is the last item.',
 'The slice values[start:stop] makes a new list from start up to, but not including, stop. A slice can contain several items; a single index selects one item.'
],'''values = [10, 20, 30, 40]
print(values[0])
print(values[-1])
print(values[1:3])''','values[1:3]','values[1:4]','10\n40\n[20, 30]\n','10\n40\n[20, 30, 40]\n','Why does stop 3 exclude the item at index 3?','From [5, 10, 15, 20], print the third item and then a slice containing the first two items.','values = [5, 10, 15, 20]\nprint(values[2])\nprint(values[:2])','Index 2 selects 15; the slice ending at 2 selects [5, 10].')
lesson('list-mutation','Change the contents of a list','Distinguish changing an existing item from appending an item.',[
 'A list is mutable: its contents can change. Assigning values[1] = 9 replaces one item. values.append(12) adds a new item at the end.',
 'A method is a function accessed through a value, such as values.append. append changes the list in place and returns None; print the list afterward to inspect the change.'
],'''values = [2, 4]
values[1] = 9
result = values.append(12)
print(values)
print(result)''','values[1] = 9','values[1] = 7','[2, 9, 12]\nNone\n','[2, 7, 12]\nNone\n','Which operation changes the length? Explain why result is None even though the list changed.','Start with [1, 2], append 3, then replace the first item with 9. Print the list.','values = [1, 2]\nvalues.append(3)\nvalues[0] = 9\nprint(values)','Appending adds a position; assigning index 0 changes an existing position.')
lesson('tuples','Group a fixed set of fields','Unpack a tuple into named values.',[
 'A tuple groups values in a fixed order, often as a small record. Unlike a list, a tuple does not allow its positions to be reassigned.',
 'Unpacking binds one name per item. The number of names must match the tuple’s items unless a starred target deliberately collects the remainder.'
],'''reading = ("north", 18)
location, temperature = reading
print(location)
print(temperature)''','("north", 18)','("south", 22)','north\n18\n','south\n22\n','Which tuple position supplies each name?','Unpack ("Ada", 9) into name and score, then print Ada scored 9 with an f-string.','name, score = ("Ada", 9)\nprint(f"{name} scored {score}")','The names follow the tuple’s positional order.')
lesson('dictionaries','Look up a value by its key','Read and update a dictionary without relying on numeric positions.',[
 'A dictionary maps keys to values. Here, the strings Ada and Lin are keys, and their scores are values. scores["Ada"] looks up Ada’s score.',
 'Assigning a value to an existing key replaces that value. get(key, default) returns a default for a missing key instead of raising KeyError. Choose a default that makes sense for the data.'
],'''scores = {"Ada": 9, "Lin": 7}
scores["Ada"] = 10
print(scores["Ada"])
print(scores.get("Sam", 0))
print(len(scores))''','scores["Ada"] = 10','scores["Ada"] = 8','10\n0\n2\n','8\n0\n2\n','Why does updating Ada leave the key count unchanged?','Create a dictionary mapping red to 3 and blue to 5. Print blue’s value and the default 0 for green.','counts = {"red": 3, "blue": 5}\nprint(counts["blue"])\nprint(counts.get("green", 0))','The key blue is present; green uses the explicit fallback.')
lesson('sets','Keep unique values','Use set membership and intersection without assuming set order.',[
 'A set keeps distinct values. Constructing a set from repeated values removes duplicates. Use in to ask whether a value belongs to a set.',
 'The & operator computes the intersection: values present in both sets. Set iteration order is not a sorting rule, so sorted converts the displayed result to a predictable ordered list.'
],'''attended = {"Ada", "Lin", "Ada"}
invited = {"Ada", "Sam"}
print(len(attended))
print("Lin" in attended)
print(sorted(attended & invited))''','"Lin" in attended','"Sam" in attended','2\nTrue\n[\'Ada\']\n','2\nFalse\n[\'Ada\']\n','Explain why repeated Ada is counted once and why only Ada is in the intersection.','Build a set from [3, 1, 3, 2] and print its unique values in ascending order.','values = set([3, 1, 3, 2])\nprint(sorted(values))','A set removes duplicates; sorted supplies a defined display order.')

module('iteration','Transform collections','Count iterations, combine sequences and build new collections.')
lesson('range','Choose a numeric loop boundary','Explain the excluded stop value in range.',[
 'range(start, stop) produces integer positions from start up to, but excluding, stop. A third argument sets the step. range does not construct a stored list of every number.',
 'Use an excluded stop deliberately: range(1, 4) produces 1, 2 and 3. Printing list(range(...)) is a small inspection tool here, not a requirement for using range in a loop.'
],'''for number in range(1, 4):
    print(number)
print(list(range(0, 6, 2)))''','range(1, 4)','range(1, 3)','1\n2\n3\n[0, 2, 4]\n','1\n2\n[0, 2, 4]\n','Which stop values are excluded, and how does step 2 change the second sequence?','Print the integers 2, 3 and 4 on separate lines using range.','for number in range(2, 5):\n    print(number)','The stop must be 5 to include 4.')
lesson('enumerate','Keep an item and its position','Use enumerate instead of manually updating a counter.',[
 'enumerate(items) produces pairs containing an index and an item. Unpack each pair into two loop names. The optional start argument changes the displayed counter.',
 'Changing start does not change the underlying list or its zero-based indexes. It changes the numbers produced by enumerate, which is useful for human-facing row numbers.'
],'''names = ["Ada", "Lin"]
for position, name in enumerate(names, start=1):
    print(position, name)''','start=1','start=0','1 Ada\n2 Lin\n','0 Ada\n1 Lin\n','Do the names change when the displayed counter starts at zero?','Enumerate ["red", "blue"] starting at 1 and print each number followed by its colour.','for position, colour in enumerate(["red", "blue"], start=1):\n    print(position, colour)','enumerate supplies each counter and value together.')
lesson('zip','Pair corresponding values','Identify where zip stops when lengths differ.',[
 'zip combines items at the same positions in separate sequences. Each iteration receives one tuple containing the corresponding values.',
 'By default, zip stops when the shortest input ends. strict=True raises an error instead when lengths differ; use that option when dropping unmatched data would be a mistake.'
],'''names = ["Ada", "Lin"]
scores = [9, 7, 5]
for name, score in zip(names, scores):
    print(name, score)''','names = ["Ada", "Lin"]','names = ["Ada", "Lin", "Sam"]','Ada 9\nLin 7\n','Ada 9\nLin 7\nSam 5\n','Which score was unmatched in the starter? Why does adding one name reveal it?','Pair ["a", "b"] with [2, 4] using zip and print each pair’s two values.','for name, value in zip(["a", "b"], [2, 4]):\n    print(name, value)','Corresponding positions are combined into one iteration.')
lesson('nested-loops','Trace a loop inside a loop','Count output pairs produced by two loops.',[
 'For each iteration of the outer loop, the inner loop runs through its input again. Two outer items and three inner items produce six pairs.',
 'The example shows a Cartesian product: every row is combined with every column. This differs from zip, which pairs only corresponding positions.'
],'''for row in [1, 2]:
    for column in ["a", "b"]:
        print(row, column)''','["a", "b"]','["a", "b", "c"]','1 a\n1 b\n2 a\n2 b\n','1 a\n1 b\n1 c\n2 a\n2 b\n2 c\n','Count lines before and after the edit. Why does one extra column add two lines?','Use nested loops to print every pair from [1, 2] and [3], with the outer value first.','for left in [1, 2]:\n    for right in [3]:\n        print(left, right)','Each outer item is combined with the single inner item.',diagram={'kind':'flow','question':'Why are there four pairs rather than two?','parts':['row 1','columns a, b','row 2','columns a, b']})
lesson('comprehensions','Build a list from a rule','Separate a comprehension’s expression from its filter.',[
 'A list comprehension builds a new list by evaluating an expression for each input item. In [value * 2 for value in values], value * 2 is the output expression.',
 'An if clause keeps only items that meet a condition. Filtering and transforming are separate decisions: the filter chooses which input items remain; the expression chooses their output values.'
],'''values = [1, 2, 3, 4]
result = [value * 2 for value in values if value > 2]
print(result)
print(values)''','if value > 2','if value >= 2','[6, 8]\n[1, 2, 3, 4]\n','[4, 6, 8]\n[1, 2, 3, 4]\n','Which extra input passes the edited filter? Why is the original list unchanged?','Build and print a list containing the squares of 1, 2 and 3 using a comprehension.','print([value * value for value in [1, 2, 3]])','The output expression computes each square in a new list.')
lesson('sorting','Sort by a chosen key','Choose a sort key without changing the original records.',[
 'sorted returns a new list in ascending order. The key argument supplies a function that extracts the value used for comparison. len is already a function, so key=len sorts strings by length.',
 'reverse=True reverses the ordering. The original list remains unchanged; list.sort is a different, in-place operation that returns None.'
],'''names = ["Sam", "Alex", "Bo"]
print(sorted(names, key=len))
print(names)''','key=len','key=len, reverse=True',"['Bo', 'Sam', 'Alex']\n['Sam', 'Alex', 'Bo']\n","['Alex', 'Sam', 'Bo']\n['Sam', 'Alex', 'Bo']\n",'Compare the returned order with the original list. Which name is shortest?','Print [8, 2, 5] in descending order without changing the original list.','values = [8, 2, 5]\nprint(sorted(values, reverse=True))','reverse=True requests descending numeric order.')

module('functions','Write reusable functions','Define inputs, return results and test boundaries.')
lesson('return-values','Return a result to the caller','Distinguish return from printing inside a function.',[
 'def names a function and introduces its indented body. Parameters name the inputs. Calling the function runs that body with the supplied values.',
 'return sends a value back to the caller and ends that call. The example prints outside the function so the same returned value could also be saved or used in another calculation.'
],'''def add(left, right):
    return left + right

result = add(19, 23)
print(result)''','add(19, 23)','add(5, 8)','42\n','13\n','Which expression creates the returned value, and which statement displays it?','Define double(value) to return twice value. Print double(6) and double(-2).','def double(value):\n    return value * 2\n\nprint(double(6))\nprint(double(-2))','A return value can be used by any caller; double works for both tested inputs.',diagram={'kind':'flow','question':'Where does 42 go after the function returns?','parts':['inputs: 19, 23','add body: left + right','return: 42','caller: print(result)']})
lesson('arguments','Match arguments to parameters','Use positional and named arguments deliberately.',[
 'Arguments are the values supplied in a call; parameters are the names in the function definition. Positional arguments match parameters in order.',
 'Keyword arguments name the parameter they supply. Reordering keyword arguments does not change which parameter gets each value. Prefer names when an argument’s role would otherwise be unclear.'
],'''def describe(name, score):
    return f"{name}: {score}"

print(describe("Ada", 9))
print(describe(score=7, name="Lin"))''','score=7','score=10','Ada: 9\nLin: 7\n','Ada: 9\nLin: 10\n','Explain why score=7 is bound to score even though it appears before name.','Define difference(left, right) returning left minus right. Print difference(right=3, left=10).','def difference(left, right):\n    return left - right\n\nprint(difference(right=3, left=10))','The keyword names determine the binding, so the result is 7.')
lesson('defaults','Provide a useful default','Explain which value is used when an argument is omitted.',[
 'A default value follows a parameter’s equals sign. Python uses that value when the caller omits the corresponding argument.',
 'Keep defaults simple and predictable. A later lesson explains why a mutable list is usually a poor default: default expressions are evaluated once when the function is defined.'
],'''def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Ada"))
print(greet("Lin", greeting="Welcome"))''','greeting="Hello"','greeting="Hi"','Hello, Ada!\nWelcome, Lin!\n','Hi, Ada!\nWelcome, Lin!\n','Which call uses the default, and which call supplies its own greeting?','Define multiply(value, factor=2). Print multiply(5), then multiply(5, factor=3).','def multiply(value, factor=2):\n    return value * factor\n\nprint(multiply(5))\nprint(multiply(5, factor=3))','Omitting factor uses 2; supplying factor replaces that default for one call.')
lesson('scope','Keep a function’s local names local','Distinguish local rebinding from an outer name.',[
 'A function call has local names for its parameters and assignments. Rebinding a local name does not rebind a name in the caller.',
 'The value returned by the function can be assigned by the caller. Making that assignment explicit usually makes data flow clearer than changing global variables from inside a function.'
],'''count = 3

def next_count(count):
    count = count + 1
    return count

print(next_count(count))
print(count)''','print(next_count(count))','count = next_count(count)\nprint(count)','4\n3\n','4\n4\n','Why does the starter leave the outer count at 3? What extra assignment changes that in the edit?','Define increment(value) returning value + 1. With start = 9, print increment(start) and then start.','def increment(value):\n    return value + 1\n\nstart = 9\nprint(increment(start))\nprint(start)','The returned 10 and the unchanged caller value 9 are separate observations.')
lesson('function-boundaries','Handle an empty collection','Choose a defined result at a function’s boundary.',[
 'A function’s contract says what it accepts and what it returns. An empty list is false in a condition, so not values is true for an empty list. The average function below returns None for an empty list instead of dividing by zero.',
 'None represents the absence of a result here, not a numeric average of zero. A caller must distinguish those cases before using the result in arithmetic.'
],'''def average(values):
    if not values:
        return None
    return sum(values) / len(values)

print(average([2, 4]))
print(average([]))''','[2, 4]','[2, 4, 9]','3.0\nNone\n','5.0\nNone\n','Explain why the empty case is checked before the division. Is None the same result as 0.0?','Define first_or_none(values). Return the first item when present and None for an empty list. Print results for [7, 8] and [].','def first_or_none(values):\n    if not values:\n        return None\n    return values[0]\n\nprint(first_or_none([7, 8]))\nprint(first_or_none([]))','The empty case is a distinct outcome rather than an invalid index access.')
lesson('recursion','Make a smaller recursive call','Identify the base case that ends recursion.',[
 'A recursive function calls itself. The countdown example prints the current number, then calls itself with a smaller number.',
 'The base case handles zero and returns without another call. Without a reachable base case, calls keep accumulating until Python raises a recursion error. A loop is often simpler for long sequences.'
],'''def countdown(number):
    if number == 0:
        print("go")
        return
    print(number)
    countdown(number - 1)

countdown(3)''','countdown(3)','countdown(2)','3\n2\n1\ngo\n','2\n1\ngo\n','Which call reaches the base case? How does every recursive call move toward it?','Define factorial(n) for nonnegative n, with factorial(0) returning 1. Print factorial(4).','def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(4))','Each call reduces n; the base case supplies 1, and returns multiply back up to 24.')

module('text-data','Turn text into structured data','Parse text, CSV and JSON without guessing their structure.')
lesson('split-join','Split a line and join its fields','Choose a delimiter and trim surrounding whitespace.',[
 'split(",") separates a string at commas and returns a list of strings. strip removes whitespace from the beginning and end of a string, not from its middle.',
 'separator.join(parts) builds one string from a sequence of strings. A comprehension can clean each field before joining; the original text remains unchanged.'
],'''line = " Ada, Lin ,Sam "
names = [part.strip() for part in line.split(",")]
print(names)
print(" | ".join(names))''','" | ".join(names)','" / ".join(names)',"['Ada', 'Lin', 'Sam']\nAda | Lin | Sam\n","['Ada', 'Lin', 'Sam']\nAda / Lin / Sam\n",'Which operation removes the spaces around Lin, and which operation adds the separators in the final line?','Split " red ; blue " at semicolons, strip each field and print the fields joined with a comma.','parts = [part.strip() for part in " red ; blue ".split(";")]\nprint(",".join(parts))','Parsing and display separators are separate choices.')
lesson('normalizing-text','Compare text after normalization','Make a deliberate case-insensitive comparison.',[
 'Text comparisons are exact unless you normalize the inputs. strip handles surrounding whitespace. casefold performs a stronger case-insensitive transformation than lower and is designed for caseless matching.',
 'Normalization is a policy, not a universal correction. Preserve the original spelling when displaying a name; use the normalized form only for the comparison that needs it.'
],'''entered = "  PYTHON "
normalized = entered.strip().casefold()
print(normalized)
print(normalized == "python")''','"  PYTHON "','"  Rust "','python\nTrue\n','rust\nFalse\n','Why can the starter match despite uppercase letters and spaces?','Normalize "  Hello  " with strip and casefold, then print whether it equals "hello".','text = "  Hello  "\nprint(text.strip().casefold() == "hello")','The comparison uses normalized text while the original string stays available.')
lesson('unicode-bytes','Distinguish characters from encoded bytes','Measure the same text as characters and UTF-8 bytes.',[
 'Python strings hold Unicode text. Encoding a string as UTF-8 produces bytes, the units written to a file or sent over a connection. Some characters need more than one UTF-8 byte.',
 'len(text) counts Unicode code points, not necessarily user-perceived symbols. len(text.encode("utf-8")) counts bytes. Neither number alone measures how wide the text appears on screen.'
],'''text = "café"
data = text.encode("utf-8")
print("characters", len(text))
print("bytes", len(data))
print(data.decode("utf-8"))''','text = "café"','text = "cafe"','characters 4\nbytes 5\ncafé\n','characters 4\nbytes 4\ncafe\n','Which count changes when é becomes e? Why does decoding recover text rather than a list of byte values?','For "é", print its string length and its UTF-8 byte length on separate lines.','text = "é"\nprint(len(text))\nprint(len(text.encode("utf-8")))','One Unicode code point uses two bytes in this UTF-8 encoding.',refs=[('Unicode HOWTO','https://docs.python.org/3/howto/unicode.html')])
lesson('regular-expressions','Find a pattern in text','Use a regular expression for a defined text pattern.',[
 'import re makes Python’s regular-expression tools available; re is part of the standard library and needs no extra installation. A regular expression describes a pattern to match in text.',
 'The raw string r"\\d+" passes the backslash to the pattern engine. \\d matches a digit, and + requires one or more matches. findall returns matching strings; convert them before numeric arithmetic.'
],r'''import re
text = "item 12, item 7"
numbers = [int(part) for part in re.findall(r"\d+", text)]
print(numbers)
print(sum(numbers))''','"item 12, item 7"','"item 12, item 9"','[12, 7]\n19\n','[12, 9]\n21\n','Which text fragments match, and why are they converted with int?','Use re.findall with r"\\d+" to extract numbers from "x3 y14" and print their integer sum.','import re\nprint(sum(int(part) for part in re.findall(r"\\d+", "x3 y14")))','The digit strings 3 and 14 become integers before summing.',refs=[('re patterns','https://docs.python.org/3/library/re.html')])
lesson('csv-data','Read CSV fields that contain commas','Use the CSV parser rather than splitting every comma.',[
 'CSV uses quoting rules to distinguish separators from commas inside a field. import csv provides a parser that understands those rules.',
 'csv.reader returns rows containing strings. Convert numeric fields explicitly. The name "Ada, A." is one field because it is quoted in the prepared CSV text.'
],r'''import csv
text = 'name,score\n"Ada, A.",9\nLin,7'
rows = list(csv.reader(text.splitlines()))
print(rows[1][0])
print(sum(int(row[1]) for row in rows[1:]))''','Lin,7','Lin,8','Ada, A.\n16\n','Ada, A.\n17\n','Why would splitting the Ada row at every comma produce the wrong field count?','Parse "name,score\\nAda,4\\nLin,6" with csv.reader and print the sum of the score column, skipping the header.','import csv\nrows = list(csv.reader("name,score\\nAda,4\\nLin,6".splitlines()))\nprint(sum(int(row[1]) for row in rows[1:]))','The header is text, so skip it before converting scores.',refs=[('csv reader and writer','https://docs.python.org/3/library/csv.html')])
lesson('json-data','Decode JSON into Python values','Distinguish serialized JSON text from the decoded object.',[
 'JSON is a text format for exchanging structured data. json.loads decodes JSON text into Python values such as dictionaries and lists. json.dumps encodes Python values back into JSON text.',
 'Changing the decoded dictionary does not rewrite the original string. Encoding again produces a new string. sort_keys=True makes this small display predictable; it is not required for correct decoding.'
],'''import json
text = '{"name": "Ada", "score": 9}'
record = json.loads(text)
record["score"] = record["score"] + 1
print(record["score"])
print(json.dumps(record, sort_keys=True))''','+ 1','+ 2','10\n{"name": "Ada", "score": 10}\n','11\n{"name": "Ada", "score": 11}\n','Which value is a string, and which value supports dictionary lookup?','Decode {"values": [2, 3, 5]} from a JSON string and print the sum of values.','import json\nrecord = json.loads(\'{"values": [2, 3, 5]}\')\nprint(sum(record["values"]))','The decoded values field is a Python list.',refs=[('json','https://docs.python.org/3/library/json.html')])

module('files','Work with files and exact values','Read prepared files and export new results safely.')
lesson('paths','Represent and inspect a path','Distinguish a path’s name, suffix and contents.',[
 'A path identifies a file or directory. pathlib.Path provides operations for paths without manually joining directory separators. The prepared file data/readings.txt is copied into this run’s working directory automatically.',
 'Path.name and Path.suffix describe the filename; read_text reads its contents. The virtual working directory is fresh for each run. Generated files can be downloaded from the run’s file results.'
],'''from pathlib import Path
path = Path("data/readings.txt")
print(path.name)
print(path.suffix)
print(path.read_text(encoding="utf-8").strip())''','print(path.suffix)','print(path.parent.as_posix())','readings.txt\n.txt\n19 23\n','readings.txt\ndata\n19 23\n','Which output describes the path, and which output comes from opening the file?','Read data/readings.txt as UTF-8 text, split it into integer values and print their sum.','from pathlib import Path\nvalues = Path("data/readings.txt").read_text(encoding="utf-8").split()\nprint(sum(int(value) for value in values))','The file supplies 19 and 23; converting and summing produces 42.',fixtures={'data/readings.txt':'19 23\n'},refs=[('pathlib','https://docs.python.org/3/library/pathlib.html')])
lesson('write-files','Write a result and read it back','Verify the bytes your program saves as a text file.',[
 'write_text writes a string to a file, replacing existing contents. Passing encoding="utf-8" makes the text encoding explicit. It returns the number of characters written.',
 'This program creates report.txt in the run’s virtual directory. After Run code, expand Generated files to download that result. Rerunning starts with the prepared files again, so the old report is not an input to the next run.'
],r'''from pathlib import Path
path = Path("report.txt")
written = path.write_text("total: 42\n", encoding="utf-8")
print("written", written)
print(path.read_text(encoding="utf-8").strip())''','total: 42','total: 99','written 10\ntotal: 42\n','written 10\ntotal: 99\n','Inspect written and the read-back text, then download report.txt. Does the downloaded text match Console?','Create answer.txt containing 25 followed by a newline, then read it back and print the text without an extra blank line.','from pathlib import Path\npath = Path("answer.txt")\npath.write_text("25\\n", encoding="utf-8")\nprint(path.read_text(encoding="utf-8").strip())','Reading the file verifies the content rather than merely printing the variable that was written.',refs=[('Path.write_text','https://docs.python.org/3/library/pathlib.html#pathlib.Path.write_text')])
lesson('with-files','Close a file with a with block','Use a context manager to close a file after its block.',[
 'open returns a file object. A with statement manages that object for a block and closes it when the block ends, including when an exception leaves the block.',
 'The first print reads one line. The second print is outside the with block and checks file.closed. Keep the second print unindented so it observes the closed file.'
],'''with open("names.txt", encoding="utf-8") as file:
    print(file.readline().strip())
print("closed", file.closed)''','file.readline().strip()','file.read().strip().replace("\\n", ",")','Ada\nclosed True\n','Ada,Lin\nclosed True\n','Which print runs while the file is open, and which checks the state after closing?','Open names.txt with a with statement, count its lines and print the count.','with open("names.txt", encoding="utf-8") as file:\n    print(len(file.readlines()))','The two prepared names occupy two lines.',fixtures={'names.txt':'Ada\nLin\n'},refs=[('Reading and writing files','https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files')])
lesson('file-errors','Handle a missing input file','Catch the specific missing-file exception and choose a fallback.',[
 'An exception reports that an operation could not complete normally. open raises FileNotFoundError when its path does not exist. A try block identifies the operation whose failure you expect.',
 'except FileNotFoundError handles that specific failure. Catching every exception could also hide a programming error. The starter’s missing.txt is intentionally absent from the prepared files.'
],'''from pathlib import Path
try:
    text = Path("missing.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    text = "no saved reading"
print(text.strip())''','"missing.txt"','"reading.txt"','no saved reading\n','42\n','Which run takes the except block? Why is the successful read not replaced by the fallback?','Try to read absent.txt. If it is missing, print no file; do not create the file.','from pathlib import Path\ntry:\n    print(Path("absent.txt").read_text(encoding="utf-8"))\nexcept FileNotFoundError:\n    print("no file")','The fallback applies only to the specific operation and exception.',fixtures={'reading.txt':'42\n'},refs=[('Handling exceptions','https://docs.python.org/3/tutorial/errors.html#handling-exceptions')])
lesson('dates','Calculate a difference between dates','Use date values rather than subtracting date text.',[
 'datetime.date represents a calendar date. fromisoformat parses a year-month-day string. Subtracting two dates returns a timedelta, whose days field gives the day difference.',
 'These dates have no time of day or time zone. They are suitable for this calendar-day calculation, not for measuring elapsed time across time-zone or clock changes.'
],'''from datetime import date
start = date.fromisoformat("2026-11-01")
end = date.fromisoformat("2026-11-04")
print("days", (end - start).days)''','2026-11-04','2026-11-08','days 3\n','days 7\n','Why does the four-day date number difference produce three elapsed days?','Calculate and print the days from 2026-01-01 to 2026-01-11.','from datetime import date\nprint((date(2026, 1, 11) - date(2026, 1, 1)).days)','Subtracting the date objects gives a ten-day timedelta.',refs=[('date and timedelta','https://docs.python.org/3/library/datetime.html')])
lesson('decimal','Choose exact decimal arithmetic','Construct Decimal values from text for a decimal calculation.',[
 'Binary floating-point cannot represent every decimal fraction exactly. The decimal module provides decimal arithmetic with a configurable precision.',
 'Construct Decimal from strings when the decimal spelling is the intended value. Constructing from an existing float carries that float’s approximation into the decimal value.'
],'''from decimal import Decimal
print(0.1 + 0.2 == 0.3)
total = Decimal("0.1") + Decimal("0.2")
print(total)
print(total == Decimal("0.3"))''','Decimal("0.2")','Decimal("0.4")','False\n0.3\nTrue\n','False\n0.5\nFalse\n','Compare the two equality checks. What representation changed, and which values were supplied as decimal text?','Use Decimal strings to calculate 3 times 0.10 and print the result.','from decimal import Decimal\nprint(3 * Decimal("0.10"))','The decimal result is exactly 0.30 at the configured precision.',refs=[('decimal','https://docs.python.org/3/library/decimal.html')])

module('reliability','Find errors and test behaviour','Separate execution failures, expected cases and understanding checks.')
lesson('tracebacks','Read the exception and its source line','Use a traceback to locate an undefined name.',[
 'The starter intentionally raises NameError. Run code unchanged and inspect the exception name, the filename main.py and the source line in the traceback. This is a program error, not a failed runtime download.',
 'The variable is named total, but the print statement uses totla. Correcting that one name makes the same prepared program run. Do not reload the course to fix a Python name error.'
],'''total = 19 + 23
print(totla)''','print(totla)','print(total)',None,'42\n','After the edit, confirm that Console prints 42 rather than a traceback. Which misspelled name caused the error?','Fix this practice program by printing total rather than totla.','total = 19 + 23\nprint(total)','Read the final exception line, then locate the corresponding source line.',error='NameError',refs=[('Errors and exceptions','https://docs.python.org/3/tutorial/errors.html')])
lesson('try-except','Recover from a failed conversion','Keep the risky conversion inside a narrow try block.',[
 'int("twelve") raises ValueError because the text is not an integer spelling. except ValueError handles that conversion failure and chooses a defined alternative.',
 'Keep unrelated code outside the try block so its errors are not mistaken for conversion failures. The starter prints the chosen value after either the successful or fallback path.'
],'''text = "twelve"
try:
    value = int(text)
except ValueError:
    value = 0
print(value)''','"twelve"','"12"','0\n','12\n','Which input reaches the fallback? Why does the successful conversion bypass except?','Define parse_or_none(text), returning int(text) or None on ValueError. Print results for "7" and "bad".','def parse_or_none(text):\n    try:\n        return int(text)\n    except ValueError:\n        return None\n\nprint(parse_or_none("7"))\nprint(parse_or_none("bad"))','A failed conversion is a defined None result, distinct from a valid zero.')
lesson('raise','Reject an invalid argument','Use ValueError to enforce an explicit input contract.',[
 'raise reports an exception deliberately. The positive_count function accepts values greater than zero and raises ValueError otherwise.',
 'An exception message should name the violated condition. The caller catches the expected ValueError here to display the message; a caller that cannot recover should let the error reach its boundary.'
],'''def positive_count(value):
    if value <= 0:
        raise ValueError("count must be positive")
    return value

try:
    print(positive_count(0))
except ValueError as error:
    print(error)''','positive_count(0)','positive_count(3)','count must be positive\n','3\n','Explain why the invalid call does not return zero.','Define nonnegative(value), raising ValueError for a negative number and returning other values. Print nonnegative(0).','def nonnegative(value):\n    if value < 0:\n        raise ValueError("value must be nonnegative")\n    return value\n\nprint(nonnegative(0))','The contract accepts the boundary zero but rejects negative values.')
lesson('error-boundaries','Choose where an error becomes a message','Keep validation separate from the user-facing boundary.',[
 'A calculation function can raise an informative exception without deciding how a user should see it. A boundary such as a command-line entry function can catch that exception and print a concise message.',
 'Do not return a success-shaped value after an unexpected failure. Here, only ValueError from the documented count validation is translated into a user-facing rejection.'
],'''def divide(total, count):
    if count <= 0:
        raise ValueError("count must be greater than zero")
    return total / count

try:
    print(divide(12, 0))
except ValueError as error:
    print(f"Cannot calculate average: {error}")''','divide(12, 0)','divide(12, 3)','Cannot calculate average: count must be greater than zero\n','4.0\n','Which function defines valid input, and which statement decides how rejection is displayed?','Define safe_average(values), raising ValueError("empty") for an empty list. Catch that error for [] and print its message.','def safe_average(values):\n    if not values:\n        raise ValueError("empty")\n    return sum(values) / len(values)\n\ntry:\n    print(safe_average([]))\nexcept ValueError as error:\n    print(error)','Validation defines the contract; the outer handler chooses the presentation.')
lesson('assertions','Check an assumption with an assertion','Use assertions as checks rather than user-input validation.',[
 'assert condition raises AssertionError when the condition is false. A message after a comma can explain the expected behaviour.',
 'Assertions are useful for tests and internal assumptions. Python can remove them under optimization, so do not rely on assert to validate untrusted input or enforce a security boundary.'
],'''def add(left, right):
    return left + right

assert add(2, 3) == 5, "addition must return the sum"
print("check passed")''','return left + right','return left - right','check passed\n',None,'After the edit, inspect AssertionError and its message. Restore the addition before moving on.','Define square(value) and assert that square(3) is 9 and square(-2) is 4. Print checks passed afterward.','def square(value):\n    return value * value\n\nassert square(3) == 9\nassert square(-2) == 4\nprint("checks passed")','The negative case checks behaviour that one positive example alone would miss.',refs=[('The assert statement','https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement')])
lessons[-1]['changedError']='AssertionError'
lesson('unittest','Run a repeatable test suite','Read a suite result separately from program output.',[
 'unittest is Python’s standard-library test framework. FunctionTestCase adapts an ordinary test function into a test case, and TestSuite groups cases for a runner.',
 'TextTestRunner writes a test report to the message stream. The final passed field is printed by this program and states whether the suite succeeded. A test failure is evidence about the code, not an unavailable Python runtime.'
],'''import unittest

def double(value):
    return value * 2

def test_double():
    assert double(3) == 6
    assert double(0) == 0

suite = unittest.TestSuite([unittest.FunctionTestCase(test_double)])
result = unittest.TextTestRunner(verbosity=0).run(suite)
print("passed", result.wasSuccessful())''','return value * 2','return value + 2','passed True\n','passed False\n','Find passed in Console and inspect Test messages. Which assertion detects the edited implementation?','Use unittest.FunctionTestCase to check that len([1, 2]) is 2. Print result.wasSuccessful().','import unittest\n\ndef test_length():\n    assert len([1, 2]) == 2\n\nsuite = unittest.TestSuite([unittest.FunctionTestCase(test_length)])\nresult = unittest.TextTestRunner(verbosity=0).run(suite)\nprint(result.wasSuccessful())','The suite provides a repeatable check and a separate success value.',refs=[('unittest','https://docs.python.org/3/library/unittest.html')])

module('modules','Organise and run a project','Split code into files and distinguish browser work from desktop tools.')
lesson('local-modules','Import your own module','Edit a helper file and rerun the importing program.',[
 'A module is a Python file that can be imported. The editor has two editable tabs: main.py runs first, and totals.py supplies add. Both files are prepared automatically for each run.',
 'from totals import add makes that function available to main.py. Select totals.py before making the requested edit. The runner reloads local modules for each run, so an earlier import does not hide your change.'
],'''from totals import add
print(add(19, 23))''','return left + right','return left * right','42\n','437\n','Which file contains the calculation, and which file calls it?','In the practice editor, write a single-file function add(left, right) returning their sum. Print add(6, 8).','def add(left, right):\n    return left + right\n\nprint(add(6, 8))','Imports separate reusable calculations from the entry program.',files={'main.py':'from totals import add\nprint(add(19, 23))\n','totals.py':'def add(left, right):\n    return left + right\n'},refs=[('Modules','https://docs.python.org/3/tutorial/modules.html')])
lesson('main-guard','Choose an entry point without running on import','Use __name__ to separate definition from script execution.',[
 'Python sets __name__ to "__main__" for the entry script. When another file imports a module, __name__ is that module’s import name instead.',
 'A main guard lets imports obtain functions without also running the script’s demonstration or command-line workflow. main() is an ordinary function name; the guard is what controls the call.'
],'''def main():
    print("entry program")

if __name__ == "__main__":
    main()
print(__name__)''','entry program','running main','entry program\n__main__\n','running main\n__main__\n','Which value of __name__ allows main() to run in this editor?','Define main() to print ready. Call it under an if __name__ == "__main__" guard.','def main():\n    print("ready")\n\nif __name__ == "__main__":\n    main()','The guard permits script execution while keeping imported definitions reusable.',refs=[('__main__','https://docs.python.org/3/library/__main__.html')])
lesson('arguments-cli','Parse command-line arguments','Use argparse to name and validate a program option.',[
 'argparse is a standard-library parser for command-line arguments. The Arguments field is already prepared as ["--count", "3"]. The browser passes those two strings after the entry filename in sys.argv.',
 'type=int asks argparse to convert the option’s value. This editor models command-line arguments; it does not start a host terminal or install a program on your device.'
],'''import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--count", type=int, default=1)
options = parser.parse_args()
print("count", options.count)
print("double", options.count * 2)''','options.count * 2','options.count * 3','count 3\ndouble 6\n','count 3\ndouble 9\n','With Arguments unchanged, explain which value argparse converted and which arithmetic expression changed.','Using argparse with the prepared --count 3 arguments, print the square of count.','import argparse\nparser = argparse.ArgumentParser()\nparser.add_argument("--count", type=int, default=1)\noptions = parser.parse_args()\nprint(options.count ** 2)','The argument controls the data; the program chooses the calculation.',args=['--count','3'],terminal={'title':'Run the exported program on your computer','text':'Install Python 3.14 on your computer, then run these commands in a terminal in the downloaded project directory. These commands are instructions for your own terminal, not Python code for the browser editor.','code':'python main.py --count 3\npython main.py --help'},refs=[('argparse','https://docs.python.org/3/library/argparse.html')])
lesson('environments','Identify the Python environment','Explain why a virtual environment belongs to a desktop workflow.',[
 'An environment combines a Python interpreter with the packages available to it. sys.prefix identifies the current environment; sys.base_prefix identifies the base installation used to create a desktop virtual environment.',
 'The browser uses a prepared WebAssembly build of Python, not a desktop virtual environment. The editable program inspects that environment. The separate terminal commands below create a virtual environment on your computer; do not paste them into the Python editor.'
],'''import sys
print("Python", sys.version_info.major)
print("has prefix", bool(sys.prefix))
print("is venv", sys.prefix != sys.base_prefix)''','sys.version_info.major','sys.version_info.major + 1','Python 3\nhas prefix True\nis venv False\n','Python 4\nhas prefix True\nis venv False\n','The edited label is an arithmetic expression, not evidence that the interpreter changed. Which two prefix values determine the venv comparison?','Import sys and print whether the running Python major version is at least 3.','import sys\nprint(sys.version_info.major >= 3)','Inspecting a value does not replace or upgrade the interpreter.',terminal={'title':'Create an isolated desktop environment','text':'These commands require a desktop terminal and an installed Python. The browser runtime is already prepared. Activation is optional when you invoke the environment’s interpreter directly.','code':'python -m venv .venv\n# macOS/Linux:\n.venv/bin/python -m pip --version\n# Windows:\n.venv\\Scripts\\python.exe -m pip --version'},refs=[('venv','https://docs.python.org/3/library/venv.html'),('Installing packages','https://packaging.python.org/en/latest/tutorials/installing-packages/')])
lesson('project-metadata','Read project metadata from TOML','Separate package metadata from Python import names.',[
 'A pyproject.toml file can describe a distribution: the project installed by a packaging tool. An import name identifies a Python module. A distribution’s name and its import name do not have to be identical.',
 'The prepared pyproject.toml is read-only setup for this example. tomllib, included in modern Python, reads the TOML text. Building and installing the project are desktop steps shown separately; Run code only inspects the metadata.'
],'''import tomllib
from pathlib import Path
metadata = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
print(metadata["project"]["name"])
print(metadata["project"]["requires-python"])''','["name"]','["version"]','foundry-demo\n>=3.11\n','0.1.0\n>=3.11\n','Which field describes the distribution, and which field states an interpreter requirement?','Read pyproject.toml with tomllib and print the project version.','import tomllib\nfrom pathlib import Path\nmetadata = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))\nprint(metadata["project"]["version"])','Metadata describes a project; reading it does not install it.',fixtures={'pyproject.toml':'[build-system]\nrequires = ["setuptools>=68"]\nbuild-backend = "setuptools.build_meta"\n[project]\nname = "foundry-demo"\nversion = "0.1.0"\nrequires-python = ">=3.11"\n'},terminal={'title':'Build a distribution on your computer','text':'Use a desktop environment containing a complete project. Building may download dependencies, so these commands need network access the first time. Do not run them in this browser editor.','code':'python -m pip install build\npython -m build\npython -m pip install .'},refs=[('Packaging projects','https://packaging.python.org/en/latest/tutorials/packaging-projects/'),('tomllib','https://docs.python.org/3/library/tomllib.html')])
lesson('type-hints','Describe a function’s input and output types','Distinguish annotations from runtime enforcement.',[
 'Type annotations document expected types and help external type-checking tools. list[int] describes a list whose items are integers, and -> int describes an integer return value.',
 'Python does not generally enforce these annotations at runtime. A type checker is a separate tool. Keep runtime validation when an input contract needs to be enforced while the program runs.'
],'''def total(values: list[int]) -> int:
    return sum(values)

print(total([2, 3]))
print(total.__annotations__["return"] is int)''','[2, 3]','[2, 3, 5]','5\nTrue\n','10\nTrue\n','Which statement computes the total, and which statement inspects the annotation?','Define length(text: str) -> int returning len(text). Print length("Ada").','def length(text: str) -> int:\n    return len(text)\n\nprint(length("Ada"))','The annotation communicates the contract; len performs the operation.',refs=[('Type hints','https://docs.python.org/3/library/typing.html')])

module('objects','Model related data and behaviour','Use objects when named state and operations belong together.')
lesson('classes','Create two independent objects','Read self as the instance supplied to a method call.',[
 'A class defines how to create objects with related data and behaviour. __init__ initializes a new instance. self refers to the instance receiving the method call.',
 'Assignments to self.name store data on that instance. Two Person objects can share the same class definition while keeping different names.'
],'''class Person:
    def __init__(self, name):
        self.name = name

    def greeting(self):
        return f"Hello, {self.name}"

first = Person("Ada")
second = Person("Lin")
print(first.greeting())
print(second.greeting())''','Person("Ada")','Person("Sam")','Hello, Ada\nHello, Lin\n','Hello, Sam\nHello, Lin\n','Why does changing first’s constructor argument leave second’s greeting unchanged?','Define a Box class storing value on self. Create Box(7) and print its value.','class Box:\n    def __init__(self, value):\n        self.value = value\n\nbox = Box(7)\nprint(box.value)','Each instance holds its own value attribute.',refs=[('Classes','https://docs.python.org/3/tutorial/classes.html')])
lesson('dataclasses','Declare a small data record','Use a dataclass to generate routine record methods.',[
 'A dataclass describes a record with named fields. The @dataclass decorator asks Python to generate methods such as initialization, a readable representation and value-based equality.',
 'The field annotations describe the record; they do not automatically validate every assigned value. Use a frozen dataclass when rebinding fields should be disallowed, while remembering that nested mutable values need their own design.'
],'''from dataclasses import dataclass

@dataclass
class Reading:
    location: str
    value: int

first = Reading("north", 18)
second = Reading("north", 18)
print(first)
print(first == second)''','second = Reading("north", 18)','second = Reading("north", 22)',"Reading(location='north', value=18)\nTrue\n","Reading(location='north', value=18)\nFalse\n",'Which field difference changes equality? Did you write an __eq__ method?','Create a dataclass Point with integer x and y fields. Print Point(2, 3).','from dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: int\n    y: int\n\nprint(Point(2, 3))','The generated representation names both fields.',refs=[('dataclasses','https://docs.python.org/3/library/dataclasses.html')])
lesson('methods','Keep an invariant inside a method','Make a state-changing operation responsible for validation.',[
 'An invariant is a condition that an object is intended to maintain. The Counter method rejects a negative amount before changing the stored value. self.value += amount adds amount to the current value and stores the result on the same attribute.',
 'A method can combine validation with mutation so callers use one operation. Python’s ordinary attributes are still accessible; this example teaches a convention and a contract, not an impenetrable security boundary.'
],'''class Counter:
    def __init__(self):
        self.value = 0

    def add(self, amount):
        if amount < 0:
            raise ValueError("amount must be nonnegative")
        self.value += amount

counter = Counter()
counter.add(3)
counter.add(2)
print(counter.value)''','counter.add(2)','counter.add(5)','5\n','8\n','Which method controls valid updates, and when does the stored state change?','Define Counter with value initially 0 and an increment method adding 1. Call increment twice and print value.','class Counter:\n    def __init__(self):\n        self.value = 0\n\n    def increment(self):\n        self.value += 1\n\ncounter = Counter()\ncounter.increment()\ncounter.increment()\nprint(counter.value)','Both calls update the same instance’s stored value.')
lesson('properties','Calculate an attribute from stored state','Keep a derived value consistent with its inputs.',[
 'A property lets a method be read using attribute syntax. The area property computes width * height each time it is read.',
 'Because area is derived rather than stored separately, changing width cannot leave an old saved area behind. Properties are useful for a stable interface; avoid hiding unexpectedly expensive work in a simple-looking attribute.'
],'''class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

shape = Rectangle(3, 4)
print(shape.area)
shape.width = 5
print(shape.area)''','shape.width = 5','shape.width = 2','12\n20\n','12\n8\n','Why does the second area use the updated width without assigning shape.area?','Define Square with a side attribute and an area property. Print Square(5).area.','class Square:\n    def __init__(self, side):\n        self.side = side\n\n    @property\n    def area(self):\n        return self.side * self.side\n\nprint(Square(5).area)','The property computes 25 from the stored side.')
lesson('composition','Build behaviour by combining objects','Pass a collaborator instead of creating a fixed dependency.',[
 'Composition means an object uses another object to do part of its work. Reporter receives a formatter, so its report method does not need to hard-code one formatting policy.',
 'Passing the collaborator at construction makes alternatives easy to test. Inheritance can also share or specialize behaviour, but an is-a relationship should fit the model before choosing a class hierarchy.'
],'''class Formatter:
    def format(self, value):
        return f"value={value}"

class Reporter:
    def __init__(self, formatter):
        self.formatter = formatter

    def report(self, value):
        return self.formatter.format(value)

print(Reporter(Formatter()).report(7))''','report(7)','report(9)','value=7\n','value=9\n','Which object decides the output format, and which object delegates the call?','Define a Printer that receives a prefix string and has format(value) returning prefix plus str(value). Print Printer("n=").format(8).','class Printer:\n    def __init__(self, prefix):\n        self.prefix = prefix\n\n    def format(self, value):\n        return self.prefix + str(value)\n\nprint(Printer("n=").format(8))','The instance’s configuration and the call’s value combine into one result.')
lesson('protocols','Describe behaviour without requiring a base class','Explain structural typing with a small protocol.',[
 'A typing.Protocol describes the operations a caller needs. A type checker can accept an object that supplies those operations even when its class does not inherit from the protocol.',
 'This is structural typing: compatibility depends on the available shape of the interface. The program still runs ordinary Python method calls; annotations do not install runtime checks automatically.'
],'''from typing import Protocol

class Named(Protocol):
    def name(self) -> str: ...

class Person:
    def name(self) -> str:
        return "Ada"

def label(value: Named) -> str:
    return value.name().upper()

print(label(Person()))''','return "Ada"','return "Lin"','ADA\n','LIN\n','Which method does label require? Does Person explicitly inherit from Named?','Define an object with a read() method returning 42 and a function consume(value) returning value.read(). Print consume on that object.','class Source:\n    def read(self):\n        return 42\n\ndef consume(value):\n    return value.read()\n\nprint(consume(Source()))','The consumer relies on a behaviour, not a particular concrete class.',refs=[('Protocols','https://docs.python.org/3/library/typing.html#typing.Protocol')])

module('language-patterns','Use Python’s language patterns','Extend small interfaces and express common transformations clearly.')
lesson('inheritance','Override behaviour in a subclass','Call a base initializer and specialize one method.',[
 'A subclass inherits attributes and methods from a base class. Override a method when the new type should provide a different implementation of that operation.',
 'super().__init__(name) calls the next initializer in the method-resolution order. In this single-base example it initializes Person’s name. Prefer composition when the relationship is uses-a rather than is-a.'
],'''class Person:
    def __init__(self, name):
        self.name = name

    def label(self):
        return self.name

class Member(Person):
    def __init__(self, name):
        super().__init__(name)

    def label(self):
        return "member: " + self.name

print(Person("Ada").label())
print(Member("Lin").label())''','Member("Lin")','Member("Sam")','Ada\nmember: Lin\n','Ada\nmember: Sam\n','Which implementation of label is used for each object? Which initializer supplies self.name?','Define Animal with speak returning "sound" and Cat inheriting Animal with speak returning "meow". Print Cat().speak().','class Animal:\n    def speak(self):\n        return "sound"\n\nclass Cat(Animal):\n    def speak(self):\n        return "meow"\n\nprint(Cat().speak())','The subclass overrides speak without changing Animal’s implementation.',refs=[('Inheritance','https://docs.python.org/3/tutorial/classes.html#inheritance')])
lesson('custom-exceptions','Give a domain failure its own exception type','Catch a meaningful exception without catching unrelated errors.',[
 'An application can define its own exception class by inheriting from Exception or a suitable built-in exception. A dedicated type lets a caller distinguish that failure from other errors.',
 'InsufficientStock inherits ValueError here. The caller catches InsufficientStock specifically, so a different programming error is not silently translated into an out-of-stock message.'
],'''class InsufficientStock(ValueError):
    pass

def reserve(available, requested):
    if requested > available:
        raise InsufficientStock("not enough units")
    return available - requested

try:
    print(reserve(3, 5))
except InsufficientStock as error:
    print(error)''','reserve(3, 5)','reserve(3, 2)','not enough units\n','1\n','Why is the failure’s type useful beyond the wording of its message?','Define InvalidName as a ValueError subclass. Raise it with message "empty name", catch InvalidName and print the message.','class InvalidName(ValueError):\n    pass\n\ntry:\n    raise InvalidName("empty name")\nexcept InvalidName as error:\n    print(error)','The caller selects the domain-specific failure by its type.',refs=[('User-defined exceptions','https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions')])
lesson('special-methods','Implement the len protocol','Connect an ordinary built-in to a special method.',[
 'Python’s built-ins use documented protocols. len(value) asks an object for its length through __len__. Defining that method lets a custom collection support the same operation.',
 'Special methods should obey their protocol’s contract. __len__ must return a nonnegative integer. Do not add unrelated work merely because a caller asks for a length.'
],'''class Batch:
    def __init__(self, values):
        self.values = list(values)

    def __len__(self):
        return len(self.values)

batch = Batch([2, 4, 6])
print(len(batch))''','[2, 4, 6]','[2, 4]','3\n','2\n','Which built-in call reaches Batch.__len__, and what collection supplies the count?','Define Word with a text attribute and __len__ returning len(self.text). Print len(Word("Ada")).','class Word:\n    def __init__(self, text):\n        self.text = text\n\n    def __len__(self):\n        return len(self.text)\n\nprint(len(Word("Ada")))','The custom object exposes its string’s length through the protocol.',refs=[('Special method names','https://docs.python.org/3/reference/datamodel.html#special-method-names')])
lesson('lambda','Choose a small function as a sort key','Use a lambda when a short expression is clearer than a separate definition.',[
 'A lambda creates a function from one expression. In lambda row: row[1], row is the parameter and row[1] is the returned value.',
 'The sort key controls comparison, not the shape of the returned records. A named def is usually clearer when the calculation needs several steps, validation or documentation.'
],'''rows = [("Ada", 9), ("Lin", 7), ("Sam", 8)]
print(sorted(rows, key=lambda row: row[1]))''','row[1]','row[0]',"[('Lin', 7), ('Sam', 8), ('Ada', 9)]\n","[('Ada', 9), ('Lin', 7), ('Sam', 8)]\n",'Which tuple field determines each ordering, and which fields remain in the output?','Sort [("a", 3), ("b", 1)] by the numeric second field and print the resulting list.','rows = [("a", 3), ("b", 1)]\nprint(sorted(rows, key=lambda row: row[1]))','The lambda extracts the numeric comparison key.',refs=[('Lambda expressions','https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions')])
lesson('dictionary-comprehensions','Transform dictionary entries into a new mapping','Use items to obtain each key and value together.',[
 'dictionary.items() produces key-value pairs for iteration. A dictionary comprehension builds a new mapping using a key expression and a value expression separated by a colon.',
 'The source mapping remains unchanged. Each generated key must be hashable, and a repeated generated key replaces an earlier value; do not assume a transformation preserves distinct keys unless the rule ensures it.'
],'''counts = {"red": 2, "blue": 3}
doubled = {name: count * 2 for name, count in counts.items()}
print(doubled)
print(counts)''','count * 2','count * 3',"{'red': 4, 'blue': 6}\n{'red': 2, 'blue': 3}\n","{'red': 6, 'blue': 9}\n{'red': 2, 'blue': 3}\n",'Which expressions choose the output keys and values? Why is counts unchanged?','Build a dictionary mapping each of ["Ada", "Lin"] to its length, and print it.','print({name: len(name) for name in ["Ada", "Lin"]})','The key is the name and the value expression computes its length.')
lesson('unpacking','Collect and expand positional arguments','Distinguish a starred parameter from a starred call argument.',[
 'In a function definition, *values collects extra positional arguments into a tuple. In a call, *numbers expands a sequence into separate positional arguments.',
 'These are related but opposite operations. The function below receives the same three values whether the caller writes them separately or expands one list.'
],'''def total(*values):
    return sum(values)

numbers = [2, 3, 5]
print(total(2, 3, 5))
print(total(*numbers))''','numbers = [2, 3, 5]','numbers = [2, 3, 8]','10\n10\n','10\n13\n','Which star collects values, and which star expands a collection?','Define total(*values) returning their sum. Print total(*[4, 6]).','def total(*values):\n    return sum(values)\n\nprint(total(*[4, 6]))','The call expands two arguments; the parameter collects them into a tuple.',refs=[('Arbitrary argument lists','https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists')])
lesson('pattern-matching','Match the structure of a command','Use match for a small set of structural cases.',[
 'match compares a value with case patterns. The tuple pattern ("add", value) requires two items, the first equal to "add", and binds the second item to value.',
 'The wildcard _ catches remaining shapes. Patterns can bind names, so a bare name is not a general constant comparison. Use literal strings or qualified constants when a case must match a fixed value.'
],'''command = ("add", 7)
match command:
    case ("add", value):
        print("adding", value)
    case ("remove", value):
        print("removing", value)
    case _:
        print("unknown command")''','command = ("add", 7)','command = ("remove", 7)','adding 7\n','removing 7\n','Which parts of the tuple select the case, and which part becomes a bound value?','Match command = ("show", 3). For the pattern ("show", number), print number; otherwise print unknown.','command = ("show", 3)\nmatch command:\n    case ("show", number):\n        print(number)\n    case _:\n        print("unknown")','Both the shape and the fixed literal must match before number is bound.',refs=[('match statements','https://docs.python.org/3/tutorial/controlflow.html#match-statements')])

module('deeper','Follow values through Python','Understand references, lazy iteration and reusable wrappers.')
lesson('copying','Distinguish a shared object from a shallow copy','Predict which list changes after mutation.',[
 'Assigning one list name to another does not copy the list. Both names refer to the same mutable object. list.copy creates a new outer list.',
 'A shallow copy still shares nested objects. Use a deliberately nested example when deciding whether copy.deepcopy is needed; copying every object can also be expensive or inappropriate.'
],'''original = [1, 2]
alias = original
copy = original.copy()
alias.append(3)
print(original)
print(copy)
print(alias is original)''','alias.append(3)','copy.append(3)','[1, 2, 3]\n[1, 2]\nTrue\n','[1, 2]\n[1, 2, 3]\nTrue\n','Which name refers to the mutated object in each run? What does is compare?','Make a copy of [1, 2], append 9 to the copy and print the unchanged original followed by the copy.','original = [1, 2]\ncopy = original.copy()\ncopy.append(9)\nprint(original)\nprint(copy)','Two distinct outer lists can be changed independently.',diagram={'kind':'references','question':'Why does changing alias affect original?','parts':['original ─┐','alias ────┴→ list [1, 2]','copy ──────→ new list [1, 2]']})
lesson('mutable-defaults','Avoid sharing a default list between calls','Create a fresh collection inside each call.',[
 'Default expressions are evaluated once when a function is defined. A list used as a default can therefore accumulate changes across otherwise separate calls.',
 'Use None as a sentinel and create a new list inside the function when no list was supplied. The test prints two call results so accidental sharing is visible.'
],'''def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(add_item("a"))
print(add_item("b"))''','items = []','items = ["start"]',"['a']\n['b']\n","['start', 'a']\n['start', 'b']\n",'Why does the second call not contain a? Which line creates the list for each call?','Define collect(value, values=None) to return a fresh list containing value when no list is supplied. Print collect(1) and collect(2).','def collect(value, values=None):\n    if values is None:\n        values = []\n    values.append(value)\n    return values\n\nprint(collect(1))\nprint(collect(2))','Each omitted argument causes a new list to be created.')
lesson('iterators','Consume an iterator one item at a time','Explain why an exhausted iterator does not restart.',[
 'iter creates an iterator over an iterable, and next asks that iterator for its next item. An iterator keeps a position as it is consumed.',
 'list(iterator) consumes all remaining items. Applying list to the same exhausted iterator again produces an empty list. To start over, obtain a new iterator from the original collection.'
],'''values = [2, 4, 6]
iterator = iter(values)
print(next(iterator))
print(list(iterator))
print(list(iterator))''','print(next(iterator))','print(next(iterator))\nprint(next(iterator))','2\n[4, 6]\n[]\n','2\n4\n[6]\n[]\n','Which items remain after each next call? Why is the final list empty?','Create an iterator over [7, 8]. Print next(iterator), then list(iterator).','iterator = iter([7, 8])\nprint(next(iterator))\nprint(list(iterator))','The first item is consumed before the remaining items are collected.',refs=[('Iterator types','https://docs.python.org/3/library/stdtypes.html#iterator-types')])
lesson('generators','Yield values without building the whole result','Trace when a generator body resumes.',[
 'A function containing yield creates a generator iterator. Calling the function does not run its entire body immediately. Each next request resumes the body until its next yield.',
 'A generator can process inputs incrementally instead of storing every output at once. It can still retain its inputs or other large state, so laziness alone does not prove low memory use.'
],'''def squares(values):
    for value in values:
        yield value * value

result = squares([2, 3, 4])
print(next(result))
print(list(result))''','[2, 3, 4]','[3, 4, 5]','4\n[9, 16]\n','9\n[16, 25]\n','Which value is yielded first, and which values remain for list to consume?','Define evens(values) yielding only even values. value % 2 == 0 tests whether division by 2 has zero remainder. Print list(evens([1, 2, 3, 4])).','def evens(values):\n    for value in values:\n        if value % 2 == 0:\n            yield value\n\nprint(list(evens([1, 2, 3, 4])))','The generator filters items as its caller requests them.',refs=[('Generators','https://docs.python.org/3/tutorial/classes.html#generators')])
lesson('decorators','Wrap a function while preserving its result','Follow a call through a decorator and its wrapped function.',[
 'A decorator receives a function and returns the callable used in its place. The @trace syntax applies trace when the decorated function is defined.',
 'The wrapper below prints before calling the original function, then returns its result. functools.wraps copies useful metadata such as the original function’s name for inspection and debugging.'
],'''from functools import wraps

def trace(function):
    @wraps(function)
    def wrapped(value):
        print("calling", function.__name__)
        return function(value)
    return wrapped

@trace
def double(value):
    return value * 2

print(double(3))''','double(3)','double(5)','calling double\n6\n','calling double\n10\n','Why does calling double appear before the numeric result?','Define a decorator twice that calls its wrapped no-argument function twice. Decorate a function printing hi and call it once.','def twice(function):\n    def wrapped():\n        function()\n        function()\n    return wrapped\n\n@twice\ndef greet():\n    print("hi")\n\ngreet()','One wrapper call deliberately invokes the original callable twice.',refs=[('functools.wraps','https://docs.python.org/3/library/functools.html#functools.wraps')])
lesson('context-managers','Guarantee cleanup with a context manager','Use try/finally around a yielded resource.',[
 'contextlib.contextmanager turns a generator function into a context manager for with. Code before yield prepares the resource; the yielded value becomes the as target.',
 'A finally block runs when the with body finishes or raises. The example prints the event order so you can distinguish resource preparation, use and cleanup.'
],'''from contextlib import contextmanager

@contextmanager
def resource():
    print("open")
    try:
        yield "ready"
    finally:
        print("close")

with resource() as value:
    print(value)''','yield "ready"','yield "available"','open\nready\nclose\n','open\navailable\nclose\n','Which output comes from the with body, and which comes from cleanup?','Create a context manager yielding 7 and printing done in finally. Inside with, print the yielded value.','from contextlib import contextmanager\n\n@contextmanager\ndef value():\n    try:\n        yield 7\n    finally:\n        print("done")\n\nwith value() as number:\n    print(number)','Cleanup runs after the body uses the yielded value.',refs=[('contextlib.contextmanager','https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager')])

module('applications','Build programs around real data','Configure, query and test small programs with the standard library.')
lesson('logging','Separate diagnostic messages from returned values','Choose a logging threshold and inspect the message stream.',[
 'Logging records diagnostic events with severity levels. DEBUG is more detailed than INFO; a configured threshold filters lower-severity messages.',
 'The program’s result is printed to Console. Logging is sent to Test and diagnostic messages so you can inspect it separately. force=True makes this run’s configuration explicit rather than relying on earlier runtime state.'
],'''import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", force=True)
logging.debug("detail")
logging.info("loaded 3 records")
print("total", 42)''','level=logging.INFO','level=logging.DEBUG','total 42\n','total 42\n','Open Test and diagnostic messages. Which extra message appears at DEBUG even though the printed total stays the same?','Configure logging at WARNING, emit an INFO message and a WARNING message, then print ready.','import logging\nlogging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s", force=True)\nlogging.info("hidden")\nlogging.warning("visible")\nprint("ready")','The threshold changes diagnostics, not the program’s returned data.',refs=[('Logging HOWTO','https://docs.python.org/3/howto/logging.html')])
lesson('configuration','Combine defaults with a configuration file','State which value takes precedence when a key is repeated.',[
 'Configuration separates a program’s policy from its code. The prepared config.json overrides the default limit while leaving unspecified defaults in place.',
 'The dictionary union operator | creates a new dictionary. For a repeated key, the right-hand dictionary wins. This explicit order is easier to inspect than scattered assignments throughout a program.'
],'''import json
from pathlib import Path
defaults = {"limit": 5, "format": "text"}
configured = json.loads(Path("config.json").read_text(encoding="utf-8"))
settings = defaults | configured
print(settings["limit"])
print(settings["format"])''','defaults | configured','configured | defaults','10\ntext\n','5\ntext\n','Which side wins for limit? Why is format still present in both runs?','Merge defaults {"colour": "blue", "count": 2} with overrides {"count": 4}, keeping the override. Print the resulting count.','defaults = {"colour": "blue", "count": 2}\noverrides = {"count": 4}\nprint((defaults | overrides)["count"])','The right-hand override replaces only the repeated key.',fixtures={'config.json':'{"limit": 10}\n'})
lesson('sqlite-queries','Query records with SQLite','Distinguish a SQL table from a Python result list.',[
 'sqlite3 is Python’s interface to the SQLite database engine. This example opens an in-memory database, creates a table and inserts two rows automatically on every run.',
 'execute runs a SQL statement. fetchall returns matching rows as a Python list of tuples. ORDER BY gives a defined result order; without it, do not treat a returned order as a sorting guarantee.'
],'''import sqlite3
connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE scores(name TEXT, score INTEGER)")
connection.executemany("INSERT INTO scores VALUES (?, ?)", [("Ada", 9), ("Lin", 7)])
rows = connection.execute("SELECT name, score FROM scores WHERE score >= ? ORDER BY name", (8,)).fetchall()
print(rows)
connection.close()''','(8,)).fetchall()','(7,)).fetchall()',"[('Ada', 9)]\n","[('Ada', 9), ('Lin', 7)]\n",'Which row is admitted by changing the threshold? What prepares the table before the query?','Create an in-memory SQLite connection and print the result of SELECT 2 + 3 using fetchone()[0].','import sqlite3\nconnection = sqlite3.connect(":memory:")\nprint(connection.execute("SELECT 2 + 3").fetchone()[0])\nconnection.close()','SQLite evaluates the SQL expression; fetchone returns its result tuple.',refs=[('sqlite3','https://docs.python.org/3/library/sqlite3.html')])
lesson('sql-parameters','Pass query values as parameters','Keep data separate from SQL syntax.',[
 'A ? placeholder marks a value supplied separately to SQLite. The tuple of parameters contains the user’s data; it is not pasted into the SQL statement.',
 'Parameter binding handles quotes as data. Constructing SQL by joining untrusted text can change the query’s meaning. Placeholders bind values, not table or column names; choose identifiers from an allowed set when a program needs them.'
],'''import sqlite3
connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE people(name TEXT)")
connection.executemany("INSERT INTO people VALUES (?)", [("Ada",), ("O'Neil",)])
name = "O'Neil"
rows = connection.execute("SELECT name FROM people WHERE name = ?", (name,)).fetchall()
print(rows)
connection.close()''','name = "O\'Neil"','name = "Ada"',"[(\"O'Neil\",)]\n","[('Ada',)]\n",'Why does the apostrophe remain part of the name instead of terminating the SQL value?','Use SQLite parameter binding to evaluate SELECT ? + ? with parameters 4 and 7. Print the scalar result.','import sqlite3\nconnection = sqlite3.connect(":memory:")\nprint(connection.execute("SELECT ? + ?", (4, 7)).fetchone()[0])\nconnection.close()','The query syntax stays fixed while the two values are bound separately.',refs=[('Using placeholders','https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries')])
lesson('transactions','Commit or roll back a group of changes','Check row count after a transaction fails.',[
 'A transaction groups database changes. The sqlite3 connection context manager commits on a successful exit and rolls back when an exception leaves its block.',
 'The connection’s context manager does not close the connection. This example closes it explicitly after inspecting the result. Each run prepares a new in-memory database, so a rollback does not affect another lesson’s data.'
],'''import sqlite3
connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE values_table(value INTEGER)")
try:
    with connection:
        connection.execute("INSERT INTO values_table VALUES (7)")
        raise ValueError("cancel transaction")
except ValueError:
    print("rolled back")
print("rows", connection.execute("SELECT COUNT(*) FROM values_table").fetchone()[0])
connection.close()''','raise ValueError("cancel transaction")','print("allow commit")','rolled back\nrows 0\n','allow commit\nrows 1\n','Which block boundary decides commit or rollback? Why is the count zero after the exception?','Create an in-memory table items(value INTEGER), insert 5 inside with connection, then print its committed row count.','import sqlite3\nconnection = sqlite3.connect(":memory:")\nconnection.execute("CREATE TABLE items(value INTEGER)")\nwith connection:\n    connection.execute("INSERT INTO items VALUES (5)")\nprint(connection.execute("SELECT COUNT(*) FROM items").fetchone()[0])\nconnection.close()','Successful exit commits the insert before the count is read.',diagram={'kind':'branch','question':'Which path makes the inserted row visible afterward?','parts':['insert inside transaction','normal exit → commit','exception → rollback','query final row count']},refs=[('Transaction control','https://docs.python.org/3/library/sqlite3.html#transaction-control')])
lesson('test-doubles','Replace a collaborator in a test','Make a dependency’s response predictable without a live service.',[
 'A test double supplies controlled behaviour in place of a dependency. unittest.mock.Mock can return a known value and record how it was called.',
 'The example passes a loader into total instead of contacting a network service. This makes the test repeatable offline and checks both the returned total and whether the collaborator was used.'
],'''from unittest.mock import Mock

def total(loader):
    return sum(loader())

loader = Mock(return_value=[2, 3])
print(total(loader))
print("calls", loader.call_count)''','return_value=[2, 3]','return_value=[2, 8]','5\ncalls 1\n','10\ncalls 1\n','What does the fake control, and what does call_count observe?','Create a Mock returning 7. Call it twice and print its call_count.','from unittest.mock import Mock\nsource = Mock(return_value=7)\nsource()\nsource()\nprint(source.call_count)','The count observes two calls independently of the chosen return value.',refs=[('unittest.mock','https://docs.python.org/3/library/unittest.mock.html')])

module('async-performance','Coordinate and measure work','Separate concurrency, algorithmic cost and measured time.')
lesson('async-await','Suspend and resume a coroutine','Identify the await point that permits other work to run.',[
 'async def defines a coroutine function. Calling it creates a coroutine; awaiting that coroutine executes it and obtains its result. await can suspend the current coroutine while another operation makes progress.',
 'The browser editor supports the final top-level await shown here. Export project creates a desktop main.py that calls asyncio.run(main()) instead. A notebook also supports top-level await. The zero-second sleep yields control; it is not a measurement of network or CPU performance.'
],'''import asyncio

async def main():
    print("before")
    await asyncio.sleep(0)
    print("after")

await main()''','print("after")','print("resumed")','before\nafter\n','before\nresumed\n','Which statement is the suspension point? Does defining main by itself print either line?','Write async main() that awaits asyncio.sleep(0) and then prints ready. End the browser program with await main().','import asyncio\n\nasync def main():\n    await asyncio.sleep(0)\n    print("ready")\n\nawait main()','Awaiting main executes its body; sleep yields before the final print.',async_code=True,refs=[('Coroutines and tasks','https://docs.python.org/3/library/asyncio-task.html')])
lesson('async-gather','Coordinate two async operations','Distinguish concurrent scheduling from CPU parallelism.',[
 'asyncio.gather schedules awaitable operations together and returns their results in argument order. The trace below records starts and finishes around a suspension point.',
 'These tasks share one event loop. Their interleaving is concurrency, not proof that Python computations ran on separate CPU cores. Threads and processes have different execution and platform constraints; this browser workbench does not launch desktop processes.'
],'''import asyncio

async def read(label):
    print("start", label)
    await asyncio.sleep(0)
    print("finish", label)
    return label.upper()

async def main():
    results = await asyncio.gather(read("a"), read("b"))
    print(results)

await main()''','read("b")','read("c")',"start a\nstart b\nfinish a\nfinish b\n['A', 'B']\n","start a\nstart c\nfinish a\nfinish c\n['A', 'C']\n",'Find both start lines before the finish lines. Which order does the result list preserve?','Use gather to await two coroutines returning 2 and 3. Print the sum of the gathered results.','import asyncio\n\nasync def value(number):\n    await asyncio.sleep(0)\n    return number\n\nasync def main():\n    results = await asyncio.gather(value(2), value(3))\n    print(sum(results))\n\nawait main()','The operations yield cooperatively, and gather collects both results.',async_code=True,diagram={'kind':'flow','question':'Where can the second operation start before the first finishes?','parts':['task a: start → await','task b: start → await','event loop resumes a and b','gather: results in input order']},refs=[('asyncio.gather','https://docs.python.org/3/library/asyncio-task.html#asyncio.gather')])
lesson('async-cancel','Cancel a task and observe cleanup','Handle cancellation without pretending the task succeeded.',[
 'create_task schedules a coroutine. cancel requests cancellation, delivered at an await point. A finally block still provides cleanup when the task has begun executing.',
 'The first sleep in main lets work reach its await before cancellation. main then awaits the cancelled task and catches CancelledError, keeping cancellation distinct from successful completion.'
],'''import asyncio

async def work():
    try:
        await asyncio.sleep(10)
    finally:
        print("cleanup")

async def main():
    task = asyncio.create_task(work())
    await asyncio.sleep(0)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("cancelled")

await main()''','print("cleanup")','print("resource released")','cleanup\ncancelled\n','resource released\ncancelled\n','Why must main await the cancelled task? Which message comes from finally rather than the caller?','Create async main() that prints start, awaits sleep(0), then prints done. End with await main().','import asyncio\n\nasync def main():\n    print("start")\n    await asyncio.sleep(0)\n    print("done")\n\nawait main()','This practice checks the coroutine lifecycle before adding cancellation paths.',async_code=True,refs=[('Task cancellation','https://docs.python.org/3/library/asyncio-task.html#task-cancellation')])
lesson('algorithmic-cost','Count work before comparing speed','Compare an operation count rather than inventing a timing result.',[
 'An operation count can explain how a chosen algorithm scales with input size. This example counts pairs examined by two nested loops; it does not measure elapsed time.',
 'Doubling the list length multiplies the pair count by four. That relationship describes this algorithm’s counted work. Real execution time also depends on implementation, device and other activity.'
],'''values = [1, 2, 3]
comparisons = 0
for left in values:
    for right in values:
        comparisons += 1
print("items", len(values))
print("pairs examined", comparisons)''','[1, 2, 3]','[1, 2, 3, 4, 5, 6]','items 3\npairs examined 9\n','items 6\npairs examined 36\n','Calculate the ratio of input sizes and the ratio of pair counts. Are the ratios equal?','Count and print the number of pairs generated by two nested loops over range(4).','count = 0\nfor left in range(4):\n    for right in range(4):\n        count += 1\nprint(count)','Four choices in each loop produce 4 × 4 = 16 counted pairs.')
lesson('timing','Measure elapsed time without a speed claim','Keep the computed answer separate from timing evidence.',[
 'time.perf_counter reads a clock suitable for elapsed-time intervals. Subtract the start reading from the end reading around the operation you intend to measure.',
 'This program prints whether the elapsed interval is nonnegative, not a fixed timing target. A single run cannot establish that one implementation is faster. For a real comparison, use repeated runs with the same inputs and inspect variability; timeit automates repeated timing.'
],'''from time import perf_counter
start = perf_counter()
answer = sum(range(1000))
elapsed = perf_counter() - start
print("answer", answer)
print("elapsed nonnegative", elapsed >= 0)''','range(1000)','range(2000)','answer 499500\nelapsed nonnegative True\n','answer 1999000\nelapsed nonnegative True\n','Which printed quantity is deterministic for the input, and why is an exact elapsed time not used as the correctness check?','Use perf_counter before and after sum([2, 3]). Print the sum, then whether the elapsed duration is at least zero.','from time import perf_counter\nstart = perf_counter()\nanswer = sum([2, 3])\nelapsed = perf_counter() - start\nprint(answer)\nprint(elapsed >= 0)','The numeric result is a correctness observation; the clock interval is a measurement.',refs=[('time.perf_counter','https://docs.python.org/3/library/time.html#time.perf_counter'),('timeit','https://docs.python.org/3/library/timeit.html')])
lesson('caching','Reuse a result for the same arguments','Inspect cache hits while stating the purity assumption.',[
 'functools.lru_cache saves return values by argument. A later call with the same arguments can return the saved value without executing the function body again.',
 'Caching is appropriate when equal arguments should produce a reusable result and the saved objects are suitable to share. It can give stale or incorrect behaviour when a function depends on changing external state or returns mutable objects that callers alter.'
],'''from functools import lru_cache

@lru_cache(maxsize=8)
def square(value):
    print("calculate", value)
    return value * value

print(square(3))
print(square(3))
print("hits", square.cache_info().hits)''','print(square(3))\nprint(square(3))','print(square(3))\nprint(square(4))','calculate 3\n9\n9\nhits 1\n','calculate 3\n9\ncalculate 4\n16\nhits 0\n','Why is calculate printed once for repeated arguments, and what does the hit count measure?','Use lru_cache on double(value). Call double(4) twice, then print the cache hit count.','from functools import lru_cache\n\n@lru_cache(maxsize=8)\ndef double(value):\n    return value * 2\n\ndouble(4)\ndouble(4)\nprint(double.cache_info().hits)','The second call uses the stored result for argument 4.',refs=[('lru_cache','https://docs.python.org/3/library/functools.html#functools.lru_cache')])

module('projects','Bring the pieces together','Build and test small tools with explicit inputs and exported results.')
lesson('project-text','Project: count words in a prepared file','Combine file reading, normalization and aggregation.',[
 'The page prepares notes.txt automatically. The program normalizes each whitespace-separated word, counts occurrences and prints keys in sorted order. Punctuation is deliberately outside this small tokenizer’s contract.',
 'The output file summary.json records the same counts. Use Generated files to inspect or download it. A new run starts again from notes.txt, so changing the code cannot silently reuse an earlier summary.'
],'''from collections import Counter
from pathlib import Path
import json

words = Path("notes.txt").read_text(encoding="utf-8").casefold().split()
counts = Counter(words)
for word in sorted(counts):
    print(word, counts[word])
Path("summary.json").write_text(json.dumps(dict(counts), sort_keys=True), encoding="utf-8")''','.casefold().split()','.split()','blue 2\nred 2\n','Red 1\nblue 2\nred 1\n','Which keys merge under casefold, and how can the JSON file confirm the printed counts?','Read notes.txt, normalize with casefold and print the total number of words followed by the number of distinct words.','from pathlib import Path\nwords = Path("notes.txt").read_text(encoding="utf-8").casefold().split()\nprint(len(words))\nprint(len(set(words)))','The file contains four words and two distinct normalized words.',fixtures={'notes.txt':'Red blue red blue\n'},refs=[('collections.Counter','https://docs.python.org/3/library/collections.html#collections.Counter')])
lesson('project-ledger','Project: total a CSV ledger exactly','Parse decimal amounts and export a reproducible report.',[
 'The prepared sales.csv has a header and three decimal amounts. csv.DictReader names each field; Decimal parses each amount from its decimal text.',
 'The starter totals all rows and writes ledger.txt. Changing the filter changes which records contribute. Keep the header handling and the Decimal conversion rather than treating this file as a list of plain numbers.'
],r'''import csv
from decimal import Decimal
from pathlib import Path

with open("sales.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))
amounts = [Decimal(row["amount"]) for row in rows if row["kind"] == "sale"]
total = sum(amounts, Decimal("0"))
print(f"total {total:.2f}")
Path("ledger.txt").write_text(f"{total:.2f}\n", encoding="utf-8")''','row["kind"] == "sale"','row["kind"] != "refund"','total 3.30\n','total 3.30\n','Both filters happen to select the same rows in this fixture. Does that prove the rules are equivalent for a file containing other kinds?','Parse sales.csv and print the Decimal sum of all three amount fields, without filtering.','import csv\nfrom decimal import Decimal\n\nwith open("sales.csv", newline="", encoding="utf-8") as file:\n    total = sum((Decimal(row["amount"]) for row in csv.DictReader(file)), Decimal("0"))\nprint(f"{total:.2f}")','Including the refund row’s signed amount produces 2.80. Equal observations on one fixture do not prove two rules equivalent.',fixtures={'sales.csv':'kind,amount\nsale,1.10\nsale,2.20\nrefund,-0.50\n'},refs=[('csv.DictReader','https://docs.python.org/3/library/csv.html#csv.DictReader'),('decimal','https://docs.python.org/3/library/decimal.html')])
lesson('project-inventory','Project: separate an inventory model from its entry file','Edit and test a multi-file program without stale imports.',[
 'The editor prepares main.py and inventory.py as editable files, plus stock.json as read-only input. main.py loads the records; inventory.py validates and totals them. any(condition for record in records) tests records one at a time and returns True if any condition is true; here it rejects a negative count.',
 'Select inventory.py to edit the return expression below, then return to main.py if you want to trace the caller. Run code always starts at main.py and reloads both editable files.'
],'''import json
from pathlib import Path
from inventory import total_units
records = json.loads(Path("stock.json").read_text(encoding="utf-8"))
print("units", total_units(records))''','sum(record["count"] for record in records)','len(records)','units 7\n','units 2\n','Why does len(records) count products rather than units?','Define total_units(records) to sum count fields. Print its result for [{"count": 2}, {"count": 6}].','def total_units(records):\n    return sum(record["count"] for record in records)\n\nprint(total_units([{"count": 2}, {"count": 6}]))','Record count and the sum of quantities answer different questions.',files={'main.py':'import json\nfrom pathlib import Path\nfrom inventory import total_units\nrecords = json.loads(Path("stock.json").read_text(encoding="utf-8"))\nprint("units", total_units(records))\n','inventory.py':'def total_units(records):\n    if any(record["count"] < 0 for record in records):\n        raise ValueError("counts must be nonnegative")\n    return sum(record["count"] for record in records)\n'},fixtures={'stock.json':'[{"name":"pen","count":3},{"name":"book","count":4}]\n'})
lesson('project-cli','Project: build a small command-line report','Keep argument parsing, transformation and file output separate.',[
 'The prepared arguments name readings.json and report.txt. The entry file parses those options, loads the prepared readings and calls the summary function from report.py.',
 'The program prints the report and saves the same text to its output file. Export project downloads both source files and the fixture. Its README gives the equivalent desktop command.'
],r'''import argparse
import json
from pathlib import Path
from report import summary

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--output", required=True)
options = parser.parse_args()
values = json.loads(Path(options.input).read_text(encoding="utf-8"))
text = summary(values)
Path(options.output).write_text(text + "\n", encoding="utf-8")
print(text)''','return f"count={len(values)} total={sum(values)}"','return f"count={len(values)} maximum={max(values)}"','count=3 total=42\n','count=3 maximum=23\n','Which module transforms the data, and which module handles command-line and file operations?','Define summary(values) returning "empty" for [] and otherwise "total=" followed by the numeric sum. Print summary([2, 3]) and summary([]).','def summary(values):\n    if not values:\n        return "empty"\n    return f"total={sum(values)}"\n\nprint(summary([2, 3]))\nprint(summary([]))','The empty case is explicit, and the transformation can be tested without argparse.',files={'main.py':'import argparse\nimport json\nfrom pathlib import Path\nfrom report import summary\nparser = argparse.ArgumentParser()\nparser.add_argument("input")\nparser.add_argument("--output", required=True)\noptions = parser.parse_args()\nvalues = json.loads(Path(options.input).read_text(encoding="utf-8"))\ntext = summary(values)\nPath(options.output).write_text(text + "\\n", encoding="utf-8")\nprint(text)\n','report.py':'def summary(values):\n    return f"count={len(values)} total={sum(values)}"\n'},fixtures={'readings.json':'[7, 12, 23]\n'},args=['readings.json','--output','report.txt'])
lesson('project-sqlite','Project: query a catalog and export matching rows','Combine parameterized SQL with a JSON result file.',[
 'The example creates a small SQLite catalog automatically for each run. It queries records costing no more than a parameterized limit, orders them by name and exports the result as JSON.',
 'The example uses an in-memory database, while catalog.json is a downloadable output file. For a desktop application that must retain database changes between runs, use a file-backed connection and define its transaction and backup policy.'
],'''import json
import sqlite3
from pathlib import Path

connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE products(name TEXT, price INTEGER)")
connection.executemany("INSERT INTO products VALUES (?, ?)", [("pen", 2), ("book", 8), ("bag", 20)])
rows = connection.execute("SELECT name, price FROM products WHERE price <= ? ORDER BY name", (10,)).fetchall()
print(rows)
Path("catalog.json").write_text(json.dumps(rows), encoding="utf-8")
connection.close()''','(10,)).fetchall()','(5,)).fetchall()',"[('book', 8), ('pen', 2)]\n","[('pen', 2)]\n",'Which record crosses the changed limit? Does the JSON file represent every table row or only the query’s result?','Create an in-memory table items(value INTEGER), insert 3 and 7 with parameters, then print SELECT SUM(value).','import sqlite3\nconnection = sqlite3.connect(":memory:")\nconnection.execute("CREATE TABLE items(value INTEGER)")\nconnection.executemany("INSERT INTO items VALUES (?)", [(3,), (7,)])\nprint(connection.execute("SELECT SUM(value) FROM items").fetchone()[0])\nconnection.close()','The database aggregates two stored values into the scalar 10.',refs=[('sqlite3','https://docs.python.org/3/library/sqlite3.html'),('json','https://docs.python.org/3/library/json.html')])
lesson('project-async','Project: coordinate independent data transformations','Test concurrent orchestration without relying on a live network.',[
 'The prepared inputs are three integers. Each coroutine yields control once and then returns its square; gather collects the results and the program sums them. The star before the generator expression expands its coroutines into separate gather arguments; it does not multiply them.',
 'These are controlled local tasks, not HTTP requests or CPU-parallel workers. Replacing the small transformation with real I/O would require a dependency with async support, bounded concurrency, timeouts and a defined error policy.'
],'''import asyncio

async def transform(value):
    await asyncio.sleep(0)
    return value * value

async def main():
    values = [2, 3, 4]
    results = await asyncio.gather(*(transform(value) for value in values))
    print("results", results)
    print("total", sum(results))

await main()''','values = [2, 3, 4]','values = [2, 3, 5]','results [4, 9, 16]\ntotal 29\n','results [4, 9, 25]\ntotal 38\n','Which result changes, and why does gather preserve the input order even when tasks could finish in a different order?','Write async main() that gathers coroutines doubling 3 and 5, then prints the resulting list. End with await main().','import asyncio\n\nasync def double(value):\n    await asyncio.sleep(0)\n    return value * 2\n\nasync def main():\n    print(await asyncio.gather(double(3), double(5)))\n\nawait main()','The resulting list is [6, 10]. Scheduling concurrency does not claim CPU parallelism.',async_code=True,refs=[('Asyncio task groups and gather','https://docs.python.org/3/library/asyncio-task.html')])

from algorithms import populate as add_algorithms
from database_lessons import populate as add_database
add_algorithms(module, lesson)
add_database(module, lesson)

# Explicit behavioural cases check reusable practice functions beyond printed examples.
case_specs={
 'dsa-linear-search':('find_index',[([[],3],None),([[0,2,0],0],0),([[8,3,8],8],0)]),
 'dsa-binary-search':('lower_bound',[([[],3],0),([[1,3,3,7],3],1),([[1,3],9],2),([[1,3],0],0)]),
 'return-values':('double',[([0],0),([5],10),([-3],-6)]),
 'arguments':('difference',[([8,3],5),([0,2],-2)]),
 'defaults':('multiply',[([4],8),([4,3],12)]),
 'scope':('increment',[([0],1),([-2],-1)]),
 'function-boundaries':('first_or_none',[([[]],None),([[0,2]],0)]),
 'recursion':('factorial',[([0],1),([1],1),([5],120)]),
 'try-except':('parse_or_none',[(['12'],12),(['bad'],None)]),
 'assertions':('square',[([0],0),([-3],9),([5],25)]),
 'type-hints':('length',[([''],0),(['Python'],6)]),
 'project-inventory':('total_units',[([[]],0),([[{'count':2},{'count':5}]],7)]),
 'project-cli':('summary',[([[]],'empty'),([[4,8]],'total=12')]),
}
for item in lessons:
    if item['id'] in case_specs:
        function,cases=case_specs[item['id']]
        item['practiceCases']={'function':function,'cases':[{'args':args,'expected':value} for args,value in cases]}
    item['focusFile']=next((name for name,source in item['files'].items() if item['focus'] in source),item['entry'])
    item['prepared']='The page prepares the complete starter program. Each run uses a fresh working directory and fresh Python names.'
    if item['fixtures']:
        item['prepared']+=' Prepared input files: '+', '.join(item['fixtures'])+'.'
    if item['stdin']:
        item['prepared']+=' Program input is already filled; edit that field to supply different lines.'
    if item['args']:
        item['prepared']+=' Arguments is already filled with the command-line strings used by this example.'
    item['changeInstruction']=f'In {item["focusFile"]}, replace the code under Find with the code under Replace with. Choose Run code again.'
if __name__=='__main__':
    print(json.dumps({'modules':modules,'lessons':lessons},ensure_ascii=False))
