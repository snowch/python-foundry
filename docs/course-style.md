# Course presentation

The [canonical shared course design guide](https://github.com/snowch/cuda-python-lab/blob/main/docs/course-design-guide.md) defines the preferred style. Python Foundry uses its header order (Code runner, App status, theme), locally bundled Plex typography, Material Symbols, inline course outline with combined breadcrumbs, explicit completion and adjacent-lesson cards.

The homepage states no programming prerequisites and shows a compact original names → values → calculation → printed-result illustration beside the introduction above 900 pixels and below it on smaller screens. The bare URL opens the homepage; `?lesson=<stable-id>` opens a lesson. The outline filters by chapter without recreating editors and remains ordinary links rather than a floating menu.

Lesson prose is readable at 17 pixels. CodeMirror provides Python syntax, line numbers, keyboard editing and a blue font mark for the exact excerpt discussed on the page. Editors grow to fit short programs and scroll for long ones. Source files use actual tabs and a visible entry-file note. File inputs, generated outputs and diagnostic inspection have distinct labels. Program input and argument controls are always available; a lesson requiring them keeps the section open.

Essential instructions and result interpretation remain visible. The independent practice editor has its own status, result and checks; it does not alter an example’s successful-execution status. Resource rows contain official Material SVGs and descriptive reference topics. Completion is reversible, and the navigation cards name the destination lessons. All assets needed for these components are part of the offline contract.

The Foundry uses [numbered parts containing chapters and lessons](lab-series.md), with scoped progress and stable lesson links.


## Foundry navigation

Use Course → Part → Chapter → Lesson. See the [navigation review](navigation-review.md)
for reading order, learner actions, compatibility and verification.
