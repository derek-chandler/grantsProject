# grantsProject
CS490 Grants Project
## lines to edit to use filegrabtest with GrantsParserXML.py
* GrantsParserXML.py
  * add `import filegrabtest` at top
  * replace line 56 `mytree = ...` with `mytree = et.parse(filegrabtest.get())`
 * filegrabtest.py
   * remove `print(get())` on line 150 (at bottom of file) 