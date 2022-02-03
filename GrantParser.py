import xml.etree.ElementTree as ET

# convert our dates into a better looking format with slashes, MM/DD/YYYY
def dateConversion(date):
    date = date[:2] + "/" + date[2:4] + "/" + date[4:]
    return date

# convert our dates to format similar to January 01, 2021
def dateStringVersion(date):
    if (date!='N/A'):

        str(date)
        monthList =['January ', 'February ', 'March ', 'April ', 'May ', 'June ',
         'July ', 'August ', 'September ', 'October ', 'November ', 'December ']
        monthNum = int(date[:2])
        temp = monthList[monthNum -1]
        date = temp + date[2:4] + ", " + date[4:]
    return date

#convert our dates into a year, month, day hierarchy so that earlier dates are natrually smaller numbers (strings in this case) than later dates
def dateHierarchyForm(date):
    date = date[4:] + date[:4]
    return date

parser = ET.XMLPullParser(['start', 'end'])