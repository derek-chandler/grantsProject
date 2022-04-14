# grantsProject
## Description
This project is for generating grant reports based off the data downloaded off grants.gov. The user specifies the date-range of grants that they wish to browse though, then the program will generate word documents based off their preferences. 

## Requirements
 * [Python 3.10](https://www.python.org/downloads/) or above
 * All python packages in [requirements.txt](https://github.com/derek-chandler/grantsProject/blob/main/requirements.txt)

## Usage
 1. Install all requirements:
    * Windows: `python -m pip install -r requirements.txt`
    * Linux: `pip install -r requirements.txt`
 2. Execute the program: `python GrantsParserXML.py`.
    * This may take a few minutes depending on your download speed
 3. Choose the earliest date you want grants for from the calendar pop-up
 4. Click **Get Date**, then **Confirm**

Once the program finishes, **sample.docx** will be generated in the program's root directory

If you wish to generate another report, please rename or move **sample.docx** from the program's root directory

##overview
###GrantDownloader
###GrantParser
###GrantParserXML
###word.py