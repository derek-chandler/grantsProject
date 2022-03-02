import xml.etree.ElementTree as et
import html as html
import bs4_filegrabtest

# dictionary of agencies using agency code as key
# these were all the agencies in the search function for Grants.gov
# I added 'N/A' to the list to make sure that if we did not have a match, we would still have a key for it
agencyDictionary = {'USAID': 'Agency for International Development',
                    'AC': 'AmeriCorps',
                    'USDA': 'Department of Agriculture',
                    'DOC': 'Department of Commerce',
                    'DOE': 'Department of Energy',
                    'DOD': 'Department of Defense',
                    'ED': 'Department of Education',
                    'PAMS': 'Department of Health and Human Services',
                    'HHS': 'Department of Health and Human Services',
                    'DHS': 'Department of Homeland Security',
                    'HUD': 'Department of Housing and Urban Development',
                    'USDOJ': 'Department of Justice',
                    'DOL': 'Department of Labor',
                    'DOS': 'Department of State',
                    'DOI': 'Department of the Interior',
                    'USDOT': 'Department of the Treasury',
                    'DOT': 'Department of Transportation',
                    'VA': 'Department of Veterans Affairs',
                    'EPA': 'Environmental Protection Agency',
                    'GCERC': 'Gulf Coast Ecosystem Restoration Council',
                    'IMLS': 'Institute of Museum and Library Services',
                    'MCC': 'Millennium Challenge Corportation',
                    'NASA': 'National Aeronautics and Space Administration',
                    'NARA': 'National Archives and Records Administration',
                    'NEA': 'National Endowment for the Arts',
                    'NEH': 'National Endowment for the Humanities',
                    'NSF': 'National Science Foundation',
                    'NRC': 'National Resource Conservation Council',
                    'SBA': 'Small Business Administration',
                    'SSA': 'Social Security Administration',
                    'N/A': 'Other Agencies'}

# String that saves the http portion of the XML tags so that we don't have to keep typing it out,
# e.g. referencing the tag '{http://apply.grants.gov/system/OpportunityDetail-V1.0}OpportunityTitle'
# becomes just linkString+'OpportunityTitle'
linkString = '{http://apply.grants.gov/system/OpportunityDetail-V1.0}'

# ********************************************DEF*****************************************************************

# Convert our dates into a better looking format with slashes, MM/DD/YYYY


def dateConversion(date):
    newDate = date[:2] + "/" + date[2:4] + "/" + date[4:]
    return newDate

# Convert our dates to format similar to January 01, 2021


def dateStringVersion(date):
    newDate = ''
    if (date != 'N/A'):

        str(date)
        monthList = ['January ', 'February ', 'March ', 'April ', 'May ', 'June ',
                     'July ', 'August ', 'September ', 'October ', 'November ', 'December ']
        monthNum = int(date[:2])
        temp = monthList[monthNum - 1]
        newDate = temp + date[2:4] + ", " + date[4:]
    else:
        newDate = 'N/A'
    return newDate


# input a string to add commas
# example input : 10000000
# example output: 10,000,000
def addCommas(amountStr):
    # check if string is a number, if not return the string back
    if not amountStr.isnumeric():
        return amountStr
    # reverse string
    reverse = amountStr[::-1]
    newAmount = ""
    for i in range(0, len(reverse)):
        # if it's already been 3 characters, add a comma
        if i % 3 == 0 and i != 0:
            newAmount += ","
        # then add the number it's currently on
        newAmount += reverse[i]
    # return reverse of newAmount, aka the new string
    return newAmount[::-1]


# convert our dates into a year, month, day hierarchy so that earlier dates are natrually smaller numbers (strings in this case) than later dates
def dateHierarchyForm(date):
    newDate = date[4:] + date[:4]
    return newDate


# this function takes an agency code and returns the name of the agency
def generateAgencyName(agencyCode):
    # agency codes have dashes to separate the information.
    if '-' in agencyCode:
        # we only want the first part of the agency code which identifies the agency itself
        agencyCode = agencyCode.split('-')[0]

    # if the agency is in the list of agencies, we can use the agency code to get the name
    if agencyCode in agencyDictionary:
        agencyCode = agencyDictionary[agencyCode]   # of the agency

    else:
        # if the agency is not in the list of agencies, we will use the string 'Other Agencies'
        agencyCode = 'Other Agencies'

    return agencyCode


# create table of unique agencies (want to improve this, lot of redudancies related
# to multiple instances of the same agency with additional information)
def tableOfContents(listA, agency):

    if agency in listA:                     # if the agency is already in the list, we don't need to add it again
        return listA
    else:
        # if the agency is not in the list, we add it to the list
        listA.append(agency)

    return listA


# function to return an attribute of interest from a given opportunity
def getOpportunityInfo(opportunity, attribute):
    #
    # Store each text of an attribute as a string, or store as 'N/A' if none exist
    myInfo = getattr(opportunity.find(linkString + attribute), 'text', 'N/A')
    # at given attribute location
    return myInfo


# ********************************************MAIN Object*****************************************************************
class Grant:

    def __init__(self, agencyCode, agencyName, opportunityTitle, postDate, dueDate, numAwards,
                 totalFunding, awardCeiling, awardFloor, oppNumber, description, eligApplicants='N/A'):

        self.agencyCode = agencyCode
        self.distinctAgency = generateAgencyName(agencyCode)
        self.agencyName = agencyName
        self.opportunityTitle = opportunityTitle
        self.postDate = postDate
        self.dueDate = dueDate
        self.numAwards = numAwards
        self.totalFunding = totalFunding
        self.awardCeiling = awardCeiling
        self.awardFloor = awardFloor
        self.oppNumber = oppNumber
        self.description = description
        self.eligApplicants = eligApplicants

    '''
    # would like to find a way to implement this idea, need to study objects in python further

    def __init__(self, listA, opportunity, agencyCode, agencyName, opportunityTitle, postDate, dueDate, numAwards, 
        totalFunding, awardCeiling, awardFloor, oppNumber, description, eligApplicants = 'N/A'):
        
        self.agencyCode = getattr(opportunity.find(linkString + 'AgencyCode'), 'text', 'N/A')
        self.distinctAgency = generateAgencyName(self.agencyCode)
        self.agencyName = getattr(opportunity.find(linkString + 'AgencyName'), 'text', 'N/A')
        self.opportunityTitle = getattr(opportunity.find(linkString + 'OpportunityTitle'), 'text', 'N/A')
        self.postDate = getattr(opportunity.find(linkString + 'PostDate'), 'text', 'N/A')
        self.dueDate = getattr(opportunity.find(linkString + 'DueDate'), 'text', 'N/A')
        self.numAwards = getattr(opportunity.find(linkString + 'NumberOfAwards'), 'text', 'N/A')
        self.totalFunding = getattr(opportunity.find(linkString + 'TotalFunding'), 'text', 'N/A')
        self.awardCeiling = getattr(opportunity.find(linkString + 'AwardCeiling'), 'text', 'N/A')
        self.awardFloor = getattr(opportunity.find(linkString + 'AwardFloor'), 'text', 'N/A')
        self.oppNumber = getattr(opportunity.find(linkString + 'OpportunityNumber'), 'text', 'N/A')
        self.description = getattr(opportunity.find(linkString + 'Description'), 'text', 'N/A')
        self.eligApplicants = getattr(opportunity.find(linkString + 'EligibleApplicants'), 'text', 'N/A')

        tableOfContents(listA, self.agencyCode)
    '''
# ********************************************MAIN FUNCTIONS*****************************************************************


def printGrant(grant):
    print("Agency name:                     " + grant.agencyName)
    print("Opportunity title:               " + grant.opportunityTitle)
    print("Post date:                       " +
          dateStringVersion(grant.postDate))
    print("Due date:                        " +
          dateStringVersion(grant.dueDate))
    print("Expected Number of awards:       " + grant.numAwards)
    print("Estimated total program funding: $" + addCommas(grant.totalFunding))
    print("Award Ceiling:                   $" + addCommas(grant.awardCeiling))
    print("Award floor:                     $" + addCommas(grant.awardFloor))
    print("Funding opportunity number:      " + grant.oppNumber)
    print()
    print("Purpose: " + grant.description)
    print()
    print("Eligible applicants: " + grant.eligApplicants)

    print()


# function to create a dictionary using the distinctAgency as a key and the grants as values
def grantDictionaryAdd(grantDictionary, grant):
    grantDictionary.setdefault(grant.distinctAgency, []).append(grant)
    return grantDictionary

# ********************************DRIVER_CODE****************************************************************************


'''
Trying to look into more efficient parsing, this site seems to have a better, space efficient parsing method I need to explore:
https://newbedev.com/efficient-way-to-iterate-through-xml-elements
'''

# Parse our file and store it in a tree
mytree = et.parse(bs4_filegrabtest.get())

# Store the root element of this file
myroot = mytree.getroot()

# Count the number of grants that we have chosen to print,
count = 0

# Declare our list to store agency names
agencyList = []
grantDictionary = {}

# Check each grant opportunity in our tree
for opportunity in myroot:

    # Get the postdate first
    # getattr(opportunity.find(linkString + 'PostDate'), 'text', 'N/A')
    postDate = getOpportunityInfo(opportunity, 'PostDate')
    # Set the desired earliest date
    # change the string at the right of the operator to change the beginning date
    if (dateHierarchyForm(postDate) >= '20220215'):

        # print('************************************************************************************************************************')
        # print()

        # Store each text of qualifying grants as a string, or store as 'N/A' if none exist
        grant = Grant(
            agencyCode=getOpportunityInfo(opportunity, 'AgencyCode'),
            agencyName=getOpportunityInfo(opportunity, 'AgencyName'),
            opportunityTitle=html.unescape(
                getOpportunityInfo(opportunity, 'OpportunityTitle')),
            postDate=getOpportunityInfo(opportunity, 'PostDate'),
            dueDate=getOpportunityInfo(opportunity, 'DueDate'),
            numAwards=getOpportunityInfo(opportunity, 'NumberOfAwards'),
            totalFunding=getOpportunityInfo(opportunity, 'TotalFunding'),
            awardCeiling=getOpportunityInfo(opportunity, 'AwardCeiling'),
            awardFloor=getOpportunityInfo(opportunity, 'AwardFloor'),
            oppNumber=getOpportunityInfo(opportunity, 'OpportunityNumber'),
            description=html.unescape(
                getOpportunityInfo(opportunity, 'Description')),
            eligApplicants=getOpportunityInfo(
                opportunity, 'EligibleApplicants')
        )
        tableOfContents(agencyList, grant.distinctAgency)
        # Create a grant object
        grantDictionary = grantDictionaryAdd(grantDictionary, grant)
        # printGrant(grant)

        # Count the selected grant
        count += 1

print('**********************************************************************************************************')
# Print out the number of grants that qualified. I used this to check to make sure pruning was happening
print("Number of grants", count)

# sort the list of agencies
print()
agencyList.sort()

# print the list of agencies
print('Table of Contents')
print('----------------------------------------------------------------------')
for x in agencyList:
    print(x)

# Using the grantDictionary, print out each grant for Department of Education key
print('----------------------------------------------------------------------')
print()
print('ALL DEPARTMENT OF EDUCATION GRANTS')
print()
for gr in grantDictionary['Department of Education']:
    print('**********************************************************************************************************')
    printGrant(gr)
