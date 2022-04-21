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

## overview
### Used Libraries
* xml.etree.ElementTree as et


* html as html


* tkinter import *


* tkinter import messagebox


* tkcalendar import DateEntry


* os


* datetime


* word


* docx


* docx.shared import Pt


* docx.enum.text import WD_ALIGN_PARAGRAPH


* threading
 * Stuff

### GrantDownloader.py
sdfsd

### GrantParserXML.py
*Imported Libraries*
* xml.etree.ElementTree as et
* html as html
* tkinter import *
* tkinter import messagebox
* tkcalendar import DateEntry
* os
* datetime
* word
* docx
* docx.shared import Pt
* docx.enum.text import WD_ALIGN_PARAGRAPH
* threading

*Agency Storage*
* Agencies are stored within a dictionary that uses agency code as a key (Line 15 - Line 48)
* If new agencies are ever added, or an agency does not fit within this dictionary, they will be placed within the N/A - Other Agencies field until this new agency is added to the dictionary.
* Line 50 - 53 defines a variable that just automates the begining of the link for each opportunity

*DEF*
* Line 55 - 150, stores most of our used methods
* dateConversion converts our dates into a proper format for the printed report
* dateStringVersion converts our dates into a word based format for the printed report
* addCommasAndDollarSign converts monetary amounts to have commas
* dateHierarchyForm converts dates into a YYYMMDD format so earlier dates are smaller numbers for use in the UI output
* generateAgencyName takes an agency code and gets the name of the agency from our dictionary
* generateLink generates a link to the grant from Grants.gov using the grantID
* wordLimiter allows you to limit the amount of words within the description of the grant report
* tableOfContents creates a table of agencies for use in the printed grant report
* getOpportunityInfo returns an attribute of interest from a given opportunity

*MAIN Object*
* Defines class Grant and init as well as all printed parameters in the grant report (IE Agency Code, Agency Name, etc)

*MAIN Functions*
* Defines the parameters printed in each individual grant report
* Defines grantDictionaryAdd that creates a dictionary using the distinctAgency as a key and the grants as values

*Driver_Code*
* Calls to the GrantDownloader.py for it to begin downloading and parsing of the zipped XML. More information of the GrantDownloader.py can be found above in the GrantDownloader.py section.

*UI Begin*
* 

*Misc*
* Stuff

### word.py
sdfsd
