# grantsProject
CS490 Grants Project
## lines to edit to use filegrabtest/bs4_filegrabtest with GrantsParserXML.py
* GrantsParserXML.py
  * add `import filegrabtest` or `import bs4_filegrabtest` at top
  * replace line 56 `mytree = ...` with `mytree = et.parse(filegrabtest.get())` or `mytree = et.parse(bs4_filegrabtest.get())`
 * filegrabtest.py/bs4_filegrabtest.py
   * remove `print(get())` at bottom of file
