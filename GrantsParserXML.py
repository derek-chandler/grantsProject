import xml.etree.ElementTree as et

'''
TO DO:

Better parsing method/bottom up parsing. (I don't think bottom up parsing is possible from the hierarchical structure)


'''

#********************************************DEF*****************************************************************

# Convert our dates into a better looking format with slashes, MM/DD/YYYY
def dateConversion(date):
    newDate = date[:2] + "/" + date[2:4] + "/" + date[4:]
    return newDate

# Convert our dates to format similar to January 01, 2021
def dateStringVersion(date):
    newDate = ''
    if (date!='N/A'):

        str(date)
        monthList =['January ', 'February ', 'March ', 'April ', 'May ', 'June ',
         'July ', 'August ', 'September ', 'October ', 'November ', 'December ']
        monthNum = int(date[:2])
        temp = monthList[monthNum -1]
        newDate = temp + date[2:4] + ", " + date[4:]
    else:
        newDate = 'N/A'
    return newDate
S
#convert our dates into a year, month, day hierarchy so that earlier dates are natrually smaller numbers (strings in this case) than later dates
def dateHierarchyForm(date):
    newDate = date[4:] + date[:4]
    return newDate

#create table of unique agencies (want to improve this, lot of redudancies related
# to multiple instances of the same agency with additional information)
def tableOfContents(listA, agency):
    
    if agency in listA:
        return
    else:
        listA.append(agency)
    return 0

# ********************************DRIVER_CODE****************************************************************************

'''
Trying to look into more efficient parsing, this site seems to have a better, space efficient parsing method I need to explore:
https://newbedev.com/efficient-way-to-iterate-through-xml-elements
'''

# Parse our file and store it in a tree
mytree = et.parse(r'C:\SSUsers\Derek\Documents\Data Project\GrantsDBExtract20220118v2\GrantsDBExtract20220118v2.xml')

# Store the root element of this file
myroot = mytree.getroot()

# Learning some functions of xml and exploring the tree data structure
'''
#Print out the root element
print(myroot)
print("root: ", myroot.tag)
print("first child: ", myroot[0].tag)
print("first child text: ", myroot[0].text)
print("Second Child: ", myroot[1].tag)
print("Second child's text: ", myroot[1].text)
print ("Second Child's child: ", myroot[1][0].tag)
print("stuff: ", myroot[1][0].text)
    
print()
'''

'''
print("Welcome to Grant Finder! ")
startDate = input("Please enter the earliest date, in MMDDYYYY form, for which you would like to see grant opportunities: ")
startDate = str(startDate)
print("Thank you for your submission, searching for grants... ")
'''
# Count the number of grants that we have chosen to print,
count = 0

# Declare our list to store agency names
agencyList = []

# Check each grant opportunity in our tree
for opportunity in myroot:
    
    # Get the postdate first
    postDate = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}PostDate'), 'text', 'N/A')
    # Set the desired earliest date
    if (dateHierarchyForm(postDate) >= '20211201'): # change the string at the right of the operator to change the beginning date
        
        print('************************************************************************************************************************')
        print()
        #Store each text of qualifying grants as a string, or store as 'N/A' if none
        agencyName = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}AgencyName'), 'text', 'N/A')
        opportunityTitle = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}OpportunityTitle'), 'text', 'N/A')
        dueDate = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}CloseDate'), 'text', 'N/A')
        numAwards = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}ExpectedNumberOfAwards'), 'text', 'N/A')
        totalFunding = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}EstimatedTotalProgramFunding'), 'text', 'N/A')
        awardCeiling = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}AwardCeiling'), 'text', 'N/A')
        awardFloor = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}AwardFloor'), 'text', 'N/A')
        oppNumber = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}OpportunityNumber'), 'text', 'N/A')
        description = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}Description'), 'text', 'N/A')
        eligApplicants = getattr(opportunity.find('{http://apply.grants.gov/system/OpportunityDetail-V1.0}EligibleApplicants'), 'text', 'N/A')

        #Print the grant out in the desired format
        print("Agency name:                     " + agencyName)
        tableOfContents(agencyList, agencyName)
        print("Opportunity title:               " + opportunityTitle)
        print("Post date:                       " + dateStringVersion(postDate))
        print("Due date:                        " + dateStringVersion(dueDate))
        print("Expected Number of awards:       " + numAwards)
        print("Estimated total program funding: $" + totalFunding)
        print("Award Ceiling:                   $" + awardCeiling) 
        print("Award floor:                     $" + awardFloor)
        print("Funding opportunity number:      " + oppNumber)
        print()
        print("Purpose: " + description)
        print()
        print("Eligible applicants: " + eligApplicants)

        print()
        # Count the selected grant
        count +=1
   
print('**********************************************************************************************************')
# Print out the number of grants that qualified. I used this to check to make sure pruning was happening
print("Number of grants", count)

#sort the list of agencies
print()
agencyList.sort()

#print the list of agencies
print('Table of Contents')
print('----------------------------------------------------------------------')
for x in agencyList:
    print(x)

