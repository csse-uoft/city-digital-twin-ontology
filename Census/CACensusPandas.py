# -*- coding: utf-8 -*-
"""
CACensus.py

Author: Anderson Wong

Date: January 26, 2025

Description: This is a Python program that generates RDF triples 
for Canadian Census data stored in CSV format.
    
"""

# Import modules
import rdflib
import pandas
import re
import json
import os
import time
import gc

from rdflib import Graph, Literal, XSD, RDF

# Assign prefixes for the Census, Toronto, RDFS, and ISO21972 namespaces
uoft = rdflib.Namespace('http://ontology.eil.utoronto.ca/tove/cacensus#')
toronto = rdflib.Namespace('http://ontology.eil.utoronto.ca/Toronto/Toronto#')
rdfs = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')
iso21972 = rdflib.Namespace('http://ontology.eil.utoronto.ca/ISO21972/iso21972#')
foaf = rdflib.Namespace('http://xmlns.com/foaf/0.1/')
time = rdflib.Namespace('http://www.w3.org/2006/time#')

start_time = time.time()

# Create a counter for showing the progress of the program
count = 0

# Creates a Graph g
g = Graph()
  
# Opening JSON file
f = open('census3.json')
  
# Returns JSON object as a dictionary
data = json.load(f)

# Creates a dictionary called thisdict
thisdict = {}
  
# Iterating through the JSON dictionary
for i in data["Collections"]:
    
    # Find the row number of an indicator
    var = re.findall("(?:hasTotalPopulation @D)(\d+)", i["rule"])
    
    # Add indicator_name : row_number to dictionary
    if len(var) != 0:
        thisdict[i["comment"]] = int(var[0])

# Closing file
f.close()

# Create a reversedict where the keys and values of thisdict are swapped
reversedict = dict((v,k) for k,v in thisdict.items())

# Iterating through each Census CSV file
for file in os.listdir(os.path.join(os.getcwd(), "CensusCSV")):
    print("File name is: " + file)
    # Run garbage collection to free up RAM
    gc.collect()
    # Function that reads CSV file
    df = pandas.read_csv(os.path.join(os.getcwd(), "CensusCSV", file), header=1, usecols=[1,3,5,7], encoding="latin1")
    
    # Finds the censustractnumber from the spreadsheet
    censustractnumber, _ = os.path.splitext(file)
    # Create a censustract variable with the following format where # represents a number: ct-#######-##
    censustract = "ct-" + censustractnumber[0:7] + "-" + censustractnumber[-2:]
    
    # Creates a censusTract instance and gives it a rdfs.comment and rdfs.label
    g.add((toronto[censustract], RDF.type, toronto.CensusTract))
    g.add((toronto[censustract], rdfs.comment, Literal(censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    g.add((toronto[censustract], rdfs.label, Literal(censustract)))
    
    # Creates a censusProfile instance and links it to the corresponding censusTract instance
    subj = censustract + "CensusProfile2016"
    g.add((uoft[subj], RDF.type, uoft.CensusProfile2016))
    g.add((toronto[censustract], uoft.hasCensusProfile, uoft[subj]))
    g.add((uoft[subj], uoft.hasLocation, toronto[censustract]))
    # Link the censusProfile to the DateTimeInterval
    g.add((uoft[subj], uoft.hasTime, uoft.censusProfile2016DateTimeInterval))
    # Creates a rdfs.comment for the censusProfile instance
    g.add((uoft[subj], rdfs.comment, Literal("Census Profile for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    
    # Creates a list of Census characteristic categories
    characteristiclist = ["AboriginalPopulation2016", "AdmissionCategoryAndApplicantType2016", "AgeAtImmigration2016", "AgeCharacteristics2016", "Citizenship2016", "ClassOfWorker2016", "CommutingDestination2016", "CommutingDuration2016", "EthnicOriginPopulation2016", "FamilyCharacteristics2016", "FirstOfficialLanguageSpoken2016", "GenerationStatus2016", "HighestCertificateDiplomaOrDegree2016", "HouseholdAndDwellingCharacteristics2016", "HouseholdCharacteristics2016", "HouseholdType2016", "ImmigrantsBySelectedPlaceOfBirth2016", "ImmigrantStatusAndPeriodOfImmigration2016", "IncomeOfEconomicFamilies2016", "IncomeOfHouseholds2016", "IncomeOfIndividuals2016", "Industry2016", "KnowledgeOfLanguages2016", "KnowledgeOfOfficialLanguages2016", "LabourForceStatus2016", "LanguageSpokenMostOftenAtHome2016", "LanguageUsedMostOftenAtWork2016", "LocationOfStudy2016", "LowIncome2016", "MainModeOfCommuting2016", "MajorFieldOfStudy2016", "MaritalStatus2016", "MobilityStatusPlaceOfResidence1YearAgo2016", "MobilityStatusPlaceOfResidence5YearsAgo2016", "MotherTongue2016", "Occupation2016", "OtherLanguageSpokenRegularlyAtHome2016", "OtherLanguageUsedRegularlyAtWork2016", "PlaceOfWorkStatus2016", "PopulationAndDwellings2016", "RecentImmigrantsBySelectedPlaceOfBirth2016", "TimeLeavingForWork2016", "VisibleMinorityPopulation2016", "WorkActivity2016"]
    # Create an instance for each category and link it to the censusProfile and censusTract instances
    for characteristic in characteristiclist:
        obje = censustract + characteristic
        g.add((uoft[subj], uoft.hasCharacteristic, uoft[obje]))
        g.add((uoft[obje], RDF.type, uoft[characteristic]))
        g.add((uoft[obje], uoft.hasLocation, toronto[censustract]))
    
    # Add a rdfs.comment for each census category
    subj = censustract + "PopulationAndDwellings2016"
    g.add((uoft[subj], rdfs.comment, Literal("Population and dwellings" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "AgeCharacteristics2016"
    g.add((uoft[subj], rdfs.comment, Literal("Age characteristics" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "HouseholdAndDwellingCharacteristics2016"
    g.add((uoft[subj], rdfs.comment, Literal("Household and dwelling characteristics" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "MaritalStatus2016"
    g.add((uoft[subj], rdfs.comment, Literal("Marital status" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "FamilyCharacteristics2016"
    g.add((uoft[subj], rdfs.comment, Literal("Family characteristics" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "HouseholdType2016"
    g.add((uoft[subj], rdfs.comment, Literal("Household type" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "KnowledgeOfOfficialLanguages2016"
    g.add((uoft[subj], rdfs.comment, Literal("Knowledge of official languages" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "FirstOfficialLanguageSpoken2016"
    g.add((uoft[subj], rdfs.comment, Literal("First official language spoken" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "MotherTongue2016"
    g.add((uoft[subj], rdfs.comment, Literal("Mother tongue" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "LanguageSpokenMostOftenAtHome2016"
    g.add((uoft[subj], rdfs.comment, Literal("Language spoken most often at home" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "OtherLanguageSpokenRegularlyAtHome2016"
    g.add((uoft[subj], rdfs.comment, Literal("Other language spoken regularly at home" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "IncomeOfIndividuals2016"
    g.add((uoft[subj], rdfs.comment, Literal("Income of individuals in 2015" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "IncomeOfHouseholds2016"
    g.add((uoft[subj], rdfs.comment, Literal("Income of households in 2015" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "IncomeOfEconomicFamilies2016"
    g.add((uoft[subj], rdfs.comment, Literal("Income of economic families in 2015" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "LowIncome2016"
    g.add((uoft[subj], rdfs.comment, Literal("Low income in 2015" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "KnowledgeOfLanguages2016"
    g.add((uoft[subj], rdfs.comment, Literal("Knowledge of languages" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "Citizenship2016"
    g.add((uoft[subj], rdfs.comment, Literal("Citizenship" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "ImmigrantStatusAndPeriodOfImmigration2016"
    g.add((uoft[subj], rdfs.comment, Literal("Immigrant status and period of immigration" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "AgeAtImmigration2016"
    g.add((uoft[subj], rdfs.comment, Literal("Age at immigration" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "ImmigrantsBySelectedPlaceOfBirth2016"
    g.add((uoft[subj], rdfs.comment, Literal("Immigrants by selected place of birth" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "RecentImmigrantsBySelectedPlaceOfBirth2016"
    g.add((uoft[subj], rdfs.comment, Literal("Recent immigrants by selected places of birth" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "GenerationStatus2016"
    g.add((uoft[subj], rdfs.comment, Literal("Generation status" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "AdmissionCategoryAndApplicantType2016"
    g.add((uoft[subj], rdfs.comment, Literal("Admission category and applicant type" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "AboriginalPopulation2016"
    g.add((uoft[subj], rdfs.comment, Literal("Aboriginal population" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "VisibleMinorityPopulation2016"
    g.add((uoft[subj], rdfs.comment, Literal("Visible minority population" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "EthnicOriginPopulation2016"
    g.add((uoft[subj], rdfs.comment, Literal("Ethnic origin population" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "HouseholdCharacteristics2016"
    g.add((uoft[subj], rdfs.comment, Literal("Household characteristics" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "HighestCertificateDiplomaOrDegree2016"
    g.add((uoft[subj], rdfs.comment, Literal("Highest certificate; diploma or degree" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "MajorFieldOfStudy2016"
    g.add((uoft[subj], rdfs.comment, Literal("Major field of study - Classification of Instructional Programs (CIP) 2016" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "LocationOfStudy2016"
    g.add((uoft[subj], rdfs.comment, Literal("Location of study compared with province or territory of residence with countries outside Canada" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "LabourForceStatus2016"
    g.add((uoft[subj], rdfs.comment, Literal("Labour force status" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "WorkActivity2016"
    g.add((uoft[subj], rdfs.comment, Literal("Work activity during the reference year" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "ClassOfWorker2016"
    g.add((uoft[subj], rdfs.comment, Literal("Class of worker" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "Occupation2016"
    g.add((uoft[subj], rdfs.comment, Literal("Occupation - National Occupational Classification (NOC) 2016" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "Industry2016"
    g.add((uoft[subj], rdfs.comment, Literal("Industry - North American Industry Classification System (NAICS) 2012" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "PlaceOfWorkStatus2016"
    g.add((uoft[subj], rdfs.comment, Literal("Place of work status" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "CommutingDestination2016"
    g.add((uoft[subj], rdfs.comment, Literal("Commuting destination" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "MainModeOfCommuting2016"
    g.add((uoft[subj], rdfs.comment, Literal("Main mode of commuting" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "CommutingDuration2016"
    g.add((uoft[subj], rdfs.comment, Literal("Commuting duration" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "TimeLeavingForWork2016"
    g.add((uoft[subj], rdfs.comment, Literal("Time leaving for work" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "LanguageUsedMostOftenAtWork2016"
    g.add((uoft[subj], rdfs.comment, Literal("Language used most often at work" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "OtherLanguageUsedRegularlyAtWork2016"
    g.add((uoft[subj], rdfs.comment, Literal("Other language used regularly at work" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "MobilityStatusPlaceOfResidence1YearAgo2016"
    g.add((uoft[subj], rdfs.comment, Literal("Mobility status - Place of residence 1 year ago" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    subj = censustract + "MobilityStatusPlaceOfResidence5YearsAgo2016"
    g.add((uoft[subj], rdfs.comment, Literal("Mobility status - Place of residence 5 years ago" +" for " + censustractnumber + " census tract (Toronto, Ontario)", lang="en")))
    
    # A function that figures out which category a given indicator belongs to and links the two instances using hasPart
    def charcategory(rowp, row):
        row = row + 2
        subj = ""
        obje = censustract + reversedict[row + 1]
        
        if row >= 3 and row <= 9:
            subj = censustract + "PopulationAndDwellings2016"
        elif row >= 10 and row <= 42:
            subj = censustract + "AgeCharacteristics2016"
        elif row >= 43 and row <= 60:
            subj = censustract + "HouseholdAndDwellingCharacteristics2016"
        elif row >= 61 and row <= 69:
            subj = censustract + "MaritalStatus2016"
        elif row >= 70 and row <= 93:
            subj = censustract + "FamilyCharacteristics2016"
        elif row >= 94 and row <= 101:
            subj = censustract + "HouseholdType2016"
        elif row >= 102 and row <= 106:
            subj = censustract + "KnowledgeOfOfficialLanguages2016"
        elif row >= 107 and row <= 113:
            subj = censustract + "FirstOfficialLanguageSpoken2016"
        elif row >= 114 and row <= 382:
            subj = censustract + "MotherTongue2016"
        elif row >= 383 and row <= 651:
            subj = censustract + "LanguageSpokenMostOftenAtHome2016"
        elif row >= 652 and row <= 662:
            subj = censustract + "OtherLanguageSpokenRegularlyAtHome2016"
        elif row >= 663 and row <= 742:
            subj = censustract + "IncomeOfIndividuals2016"
        elif row >= 743 and row <= 801:
            subj = censustract + "IncomeOfHouseholds2016"
        elif row >= 802 and row <= 848:
            subj = censustract + "IncomeOfEconomicFamilies2016"
        elif row >= 849 and row <= 873:
            subj = censustract + "LowIncome2016"
        elif row >= 874 and row <= 1136:
            subj = censustract + "KnowledgeOfLanguages2016"
        elif row >= 1137 and row <= 1141:
            subj = censustract + "Citizenship2016"
        elif row >= 1142 and row <= 1152:
            subj = censustract + "ImmigrantStatusAndPeriodOfImmigration2016"
        elif row >= 1153 and row <= 1158:
            subj = censustract + "AgeAtImmigration2016"
        elif row >= 1159 and row <= 1218:
            subj = censustract + "ImmigrantsBySelectedPlaceOfBirth2016"
        elif row >= 1219 and row <= 1279:
            subj = censustract + "RecentImmigrantsBySelectedPlaceOfBirth2016"
        elif row >= 1280 and row <= 1283:
            subj = censustract + "GenerationStatus2016"
        elif row >= 1284 and row <= 1290:
            subj = censustract + "AdmissionCategoryAndApplicantType2016"
        elif row >= 1291 and row <= 1324:
            subj = censustract + "AboriginalPopulation2016"
        elif row >= 1325 and row <= 1339:
            subj = censustract + "VisibleMinorityPopulation2016"
        elif row >= 1340 and row <= 1618:
            subj = censustract + "EthnicOriginPopulation2016"
        elif row >= 1619 and row <= 1684:
            subj = censustract + "HouseholdCharacteristics2016"
        elif row >= 1685 and row <= 1714:
            subj = censustract + "HighestCertificateDiplomaOrDegree2016"
        elif row >= 1715 and row <= 1838:
            subj = censustract + "MajorFieldOfStudy2016"
        elif row >= 1839 and row <= 1866:
            subj = censustract + "LocationOfStudy2016"
        elif row >= 1867 and row <= 1874:
            subj = censustract + "LabourForceStatus2016"
        elif row >= 1875 and row <= 1880:
            subj = censustract + "WorkActivity2016"
        elif row >= 1881 and row <= 1885:
            subj = censustract + "ClassOfWorker2016"
        elif row >= 1886 and row <= 1898:
            subj = censustract + "Occupation2016"
        elif row >= 1899 and row <= 1921:
            subj = censustract + "Industry2016"
        elif row >= 1922 and row <= 1926:
            subj = censustract + "PlaceOfWorkStatus2016"
        elif row >= 1927 and row <= 1931:
            subj = censustract + "CommutingDestination2016"
        elif row >= 1932 and row <= 1938:
            subj = censustract + "MainModeOfCommuting2016"
        elif row >= 1939 and row <= 1944:
            subj = censustract + "CommutingDuration2016"
        elif row >= 1945 and row <= 1951:
            subj = censustract + "TimeLeavingForWork2016"
        elif row >= 1952 and row <= 2220:
            subj = censustract + "LanguageUsedMostOftenAtWork2016"
        elif row >= 2221 and row <= 2231:
            subj = censustract + "OtherLanguageUsedRegularlyAtWork2016"
        elif row >= 2232 and row <= 2240:
            subj = censustract + "MobilityStatusPlaceOfResidence1YearAgo2016"
        elif row >= 2241 and row <= 2249:
            subj = censustract + "MobilityStatusPlaceOfResidence5YearsAgo2016"
            
        g.add((uoft[subj], uoft.hasPart, uoft[obje]))
        
        if rowp.Male != "":
            obje = censustract + reversedict[row + 1] + "Male"
            g.add((uoft[subj], uoft.hasPart, uoft[obje]))
            obje = censustract + reversedict[row + 1] + "Female"
            g.add((uoft[subj], uoft.hasPart, uoft[obje]))
        
    # A function that assigns the correct unit to a given Measure instance
    def add_unit(subj, row):
        row = row + 2
        if row == 5 or (row >= 36 and row <= 40) or (row >= 689 and row <= 692) or row == 696 or row == 713 or row == 729 or (row >= 859 and row <= 863) or (row >= 869 and row <= 873) or row == 1674 or row == 1675 or row == 1681 or row == 1682 or (row >= 1872 and row <= 1874):
            g.add((uoft[subj], iso21972.hasUnit, uoft.percentage))
        elif row == 6 or row == 7 or (row >= 36 and row <= 40) or (row >= 43 and row <= 52) or (row >= 1623 and row <= 1637) or (row >= 1645 and row <= 1655):
            g.add((uoft[subj], iso21972.hasUnit, iso21972.population_cardinality_unit))
        elif row == 9:
            g.add((uoft[subj], iso21972.hasUnit, uoft.population_density_per_square_kilometre))
        elif row == 10:
            g.add((uoft[subj], iso21972.hasUnit, uoft.square_kilometre))
        elif row == 41 or row == 42:
            g.add((uoft[subj], iso21972.hasUnit, time.unitYear))
        elif (row >= 53 and row <= 58) or (row >= 94 and row <= 101) or row == 743 or row == 746 or row == 749 or row == 752 or row == 755 or row == 758 or (row >= 761 and row <= 801) or (row >= 1619 and row <= 1622) or (row >= 1639 and row <= 1644) or row == 1680:
            g.add((uoft[subj], iso21972.hasUnit, iso21972.population_cardinality_unit))
        elif row == 60:
            g.add((uoft[subj], iso21972.hasUnit, uoft.average_household_size))
        elif (row >= 70 and row <= 74) or (row >= 76 and row <= 92) or row == 802 or row == 806 or row == 810 or row == 814 or row == 818 or row == 821 or row == 824 or row == 827 or (row >= 1656 and row <= 1673):
            g.add((uoft[subj], iso21972.hasUnit, iso21972.population_cardinality_unit))
        elif row == 75 or row == 805 or row == 809 or row == 813 or row == 817:
            g.add((uoft[subj], iso21972.hasUnit, uoft.average_family_size))
        elif row == 665 or row == 667 or row == 669 or row == 671 or row == 673 or row == 676 or row == 678 or row == 680 or row == 682 or row == 684 or row == 687 or row == 688 or row == 744 or row == 745 or row == 747 or row == 748 or row == 750 or row == 751 or row == 753 or row == 754 or row == 756 or row == 757 or row == 759 or row == 760 or row == 803 or row == 804 or row == 807 or row == 808 or row == 811 or row == 812 or row == 815 or row == 816 or row == 819 or row == 820 or row == 822 or row == 823 or row == 825 or row == 826 or row == 828 or row == 829 or row == 831 or row == 832 or row == 834 or row == 835 or (row >= 1676 and row <= 1679) or row == 1683 or row == 1684:
            g.add((uoft[subj], iso21972.hasUnit, uoft.CAD))
        elif row == 1638:
            g.add((uoft[subj], iso21972.hasUnit, uoft.average_number_of_rooms_per_dwelling))
        elif row == 1880:
            g.add((uoft[subj], iso21972.hasUnit, time.unitWeek))
        else:
            # Creates triple: censusTractIndicatorMeasure hasUnit populationCardinalityUnit
            g.add((uoft[subj], iso21972.hasUnit, iso21972.population_cardinality_unit))
    
    for i, row in enumerate(df.itertuples()):
        if i == 0:
            continue  # skip first row
        if i > 2247:
            break     # stop after row 2250

        indicator = reversedict[i + 3]
       
        # Creates triple: censusTractIndicator type Indicator
        subj = censustract + indicator
        g.add((uoft[subj], RDF.type, uoft[indicator]))
        # Creates triple: censusTractIndicator hasLocation censusTract
        g.add((uoft[subj], uoft.hasLocation, toronto[censustract]))
        
        # Creates Male and Female censusTractIndicator instances, if applicable and links them to the censusTract
        if row.Male != "":
            subj = censustract + indicator + "Male"
            g.add((uoft[subj], RDF.type, uoft[indicator]))
            g.add((uoft[subj], uoft.hasLocation, toronto[censustract]))
            subj = censustract + indicator + "Female"
            g.add((uoft[subj], RDF.type, uoft[indicator]))
            g.add((uoft[subj], uoft.hasLocation, toronto[censustract]))
            
        # Creates rdfs.comment for the Indicator, Measure, and Population instances.  Also does the same for the Male/Female versions of these instances, if applicable
        spaces = len(row.Characteristics) - len(row.Characteristics.lstrip())
        j = 1
        while i + j <= 2247 and spaces < len(str(df.iloc[i + j]["Characteristics"])) - len(str(df.iloc[i + j]["Characteristics"].lstrip())):
            if spaces == 0:
                subj = censustract + reversedict[i + j + 1]
                g.add((uoft[subj], rdfs.comment, Literal(row.Characteristics.lstrip() + " (" + df.iloc[i + j]["Characteristics"].lstrip() + ")" + " for " + censustractnumber + " census tract (Toronto, Ontario) total population", lang="en")))
                
                if row.Total != "":
                    subj = censustract + reversedict[i + j + 1] + "Measure"
                    g.add((uoft[subj], uoft.hasName, Literal(reversedict[i + j + 1])))
                    g.add((uoft[subj], rdfs.comment, Literal("Measure instance for " + row.Characteristics.lstrip() + " (" + df.iloc[i + j]["Characteristics"].lstrip() + ")" + " for " + censustractnumber + " census tract (Toronto, Ontario) total population", lang="en")))
                    subj = censustract + reversedict[i + j + 1] + "Population"
                    g.add((uoft[subj], rdfs.comment, Literal("Population instance for " + row.Characteristics.lstrip() + " (" + df.iloc[i + j]["Characteristics"].lstrip() + ")" + " for " + censustractnumber + " census tract (Toronto, Ontario) total population", lang="en")))
                
                if row.Male != "":
                    subj = censustract + reversedict[i + j + 1] + "Male"
                    g.add((uoft[subj], rdfs.comment, Literal(row.Characteristics.lstrip() + " (" + df.iloc[i + j]["Characteristics"].lstrip() + ")" + " for " + censustractnumber + " census tract (Toronto, Ontario) male population", lang="en")))
                    subj = censustract + reversedict[i + j + 1] + "Female"
                    g.add((uoft[subj], rdfs.comment, Literal(row.Characteristics.lstrip() + " (" + df.iloc[i + j]["Characteristics"].lstrip() + ")" + " for " + censustractnumber + " census tract (Toronto, Ontario) female population", lang="en")))
                    
                    subj = censustract + reversedict[i + j + 1] + "MaleMeasure"
                    g.add((uoft[subj], uoft.hasName, Literal(reversedict[i + j + 1] + "Male")))
                    g.add((uoft[subj], rdfs.comment, Literal("Measure instance for " + row.Characteristics.lstrip() + " (" + df.iloc[i + j]["Characteristics"].lstrip() + ")" + " for " + censustractnumber + " census tract (Toronto, Ontario) male population", lang="en")))
                    subj = censustract + reversedict[i + j + 1] + "MalePopulation"
                    g.add((uoft[subj], rdfs.comment, Literal("Population instance for " + row.Characteristics.lstrip() + " (" + df.iloc[i + j]["Characteristics"].lstrip() + ")" + " for " + censustractnumber + " census tract (Toronto, Ontario) male population", lang="en")))
                    
                    subj = censustract + reversedict[i + j + 1] + "FemaleMeasure"
                    g.add((uoft[subj], uoft.hasName, Literal(reversedict[i + j + 1] + "Female")))
                    g.add((uoft[subj], rdfs.comment, Literal("Measure instance for " + row.Characteristics.lstrip() + " (" + df.iloc[i + j]["Characteristics"].lstrip() + ")" + " for " + censustractnumber + " census tract (Toronto, Ontario) female population", lang="en")))
                    subj = censustract + reversedict[i + j + 1] + "FemalePopulation"
                    g.add((uoft[subj], rdfs.comment, Literal("Population instance for " + row.Characteristics.lstrip() + " (" + df.iloc[i + j]["Characteristics"].lstrip() + ")" + " for " + censustractnumber + " census tract (Toronto, Ontario) female population", lang="en")))
    
            # Creates hasPart hierarchies based on the spacing in the CSV file    
            if (len(df.iloc[i + j]["Characteristics"]) - len(df.iloc[i + j]["Characteristics"].lstrip())) - spaces == 2:
                subj = censustract + reversedict[i + 3]
                obje = censustract + reversedict[i + j + 1]
                g.add((uoft[subj], uoft.hasPart, uoft[obje]))
                
                if row.Male != "":
                    subj = censustract + reversedict[i + 3] + "Male"
                    obje = censustract + reversedict[i + j + 1] + "Male"
                    g.add((uoft[subj], uoft.hasPart, uoft[obje]))
                    
                    subj = censustract + reversedict[i + 3] + "Female"
                    obje = censustract + reversedict[i + j + 1] + "Female"
                    g.add((uoft[subj], uoft.hasPart, uoft[obje]))
            i += 1
        
        # Creates rdfs.comment for the Indicator, Measure, and Population instances.  Also does the same for the Male/Female versions of these instances, if applicable
        if spaces == 0:
            charcategory(row, i)
            
            subj = censustract + indicator
            g.add((uoft[subj], rdfs.comment, Literal(row.Characteristics.lstrip() + " for " + censustractnumber + " census tract (Toronto, Ontario) total population", lang="en")))
            
            if row.Total != "":
                subj = censustract + indicator + "Measure"
                g.add((uoft[subj], uoft.hasName, Literal(indicator)))
                g.add((uoft[subj], rdfs.comment, Literal("Measure instance for " + row.Characteristics.lstrip() + " for " + censustractnumber + " census tract (Toronto, Ontario) total population", lang="en")))
                subj = censustract + indicator + "Population"
                g.add((uoft[subj], rdfs.comment, Literal("Population instance for " + row.Characteristics.lstrip() + " for " + censustractnumber + " census tract (Toronto, Ontario) total population", lang="en")))
            
            if row.Male != "":
                subj = censustract + indicator + "Male"
                g.add((uoft[subj], rdfs.comment, Literal(row.Characteristics.lstrip() + " for " + censustractnumber + " census tract (Toronto, Ontario) male population", lang="en")))
                subj = censustract + indicator + "Female"
                g.add((uoft[subj], rdfs.comment, Literal(row.Characteristics.lstrip() + " for " + censustractnumber + " census tract (Toronto, Ontario) female population", lang="en")))
                
                subj = censustract + indicator + "MaleMeasure"
                g.add((uoft[subj], uoft.hasName, Literal(indicator + "Male")))
                g.add((uoft[subj], rdfs.comment, Literal("Measure instance for " + row.Characteristics.lstrip() + " for " + censustractnumber + " census tract (Toronto, Ontario) male population", lang="en")))
                subj = censustract + indicator + "MalePopulation"
                g.add((uoft[subj], rdfs.comment, Literal("Population instance for " + row.Characteristics.lstrip() + " for " + censustractnumber + " census tract (Toronto, Ontario) male population", lang="en")))
                
                subj = censustract + indicator + "FemaleMeasure"
                g.add((uoft[subj], uoft.hasName, Literal(indicator + "Female")))
                g.add((uoft[subj], rdfs.comment, Literal("Measure instance for " + row.Characteristics.lstrip() + " for " + censustractnumber + " census tract (Toronto, Ontario) female population", lang="en")))
                subj = censustract + indicator + "FemalePopulation"
                g.add((uoft[subj], rdfs.comment, Literal("Population instance for " + row.Characteristics.lstrip() + " for " + censustractnumber + " census tract (Toronto, Ontario) female population", lang="en")))
    

        # Creates triple: censusTractIndicator value censusTractIndicatorMeasure
        subj = censustract + indicator
        obje = censustract + indicator + "Measure"
        g.add((uoft[subj], iso21972.hasValue, uoft[obje]))
        # Creates triple: censusTractIndicatorMeasure forQuantity censusTractIndicator
        g.add((uoft[obje], uoft.forQuantity, uoft[subj]))
        
        # Creates triple: censusTractIndicatorMeasure numerical_value integer or decimal
        subj = censustract + indicator + "Measure"
        if pandas.isna(row.Total): 
            continue
        if "." in str(row.Total):
            g.add((uoft[subj], iso21972.hasNumericalValue, Literal(row.Total, datatype=XSD.decimal)))
        else:
            g.add((uoft[subj], iso21972.hasNumericalValue, Literal(row.Total, datatype=XSD.integer)))
        # Creates triple: censusTractIndicatorMeasure type Measure
        g.add((uoft[subj], RDF.type, iso21972.Measure))
        
        # Calls the add_unit function to assign an appropriate unit for the Indicator
        add_unit(subj, i)
        
        # If the Indicator hasUnit population_cardinality_unit, link it to the corresponding Population instance
        if (uoft[subj], iso21972.hasUnit, iso21972.population_cardinality_unit) in g:
            subj = censustract + indicator
            obje = subj + "Population"
            g.add((uoft[subj], iso21972.cardinality_of, uoft[obje]))
            
            subj = obje
            if indicator[:-4] == "Population":
                g.add((uoft[subj], RDF.type, iso21972.Population))
            else:
                obje = indicator[:-4] + "Population"
                g.add((uoft[obje], rdfs.subClassOf, iso21972.Population))
                g.add((uoft[subj], RDF.type, uoft[obje]))
                obje2 = "Person" + indicator
                g.add((uoft[obje], iso21972.defined_by, uoft[obje2]))
                g.add((uoft[obje2], rdfs.subClassOf, foaf.Person))
            
            g.add((uoft[subj], iso21972.located_in, toronto[censustract]))
            g.add((uoft[subj], uoft.hasTime, uoft.censusProfile2016DateTimeInterval))
        else:
            subj = censustract + indicator + "Population"
            g.remove((uoft[subj], None, None))
        
        # Creates MaleMeasure and FemaleMeasure if available
        if pandas.isna(row.Male): 
            continue
        # Creates triple: censusTractIndicatorMaleMeasure numerical_value integer or decimal
        subj = censustract + indicator + "MaleMeasure"
    
        if "." in str(row.Male):
            g.add((uoft[subj], iso21972.hasNumericalValue, Literal(row.Male, datatype=XSD.decimal)))
        else:
            g.add((uoft[subj], iso21972.hasNumericalValue, Literal(row.Male, datatype=XSD.integer)))
        # Creates triple: censusTractIndicatorMaleMeasure type Measure
        g.add((uoft[subj], RDF.type, iso21972.Measure))
        
        # Calls the add_unit function to assign an appropriate unit for the Indicator
        add_unit(subj, i)
        
        # If the Indicator hasUnit population_cardinality_unit, link it to the corresponding Population instance
        if (uoft[subj], iso21972.hasUnit, iso21972.population_cardinality_unit) in g:
            subj = censustract + indicator + "Male"
            obje = subj + "Population"
            g.add((uoft[subj], iso21972.cardinality_of, uoft[obje]))
            
            subj = obje
            if indicator[:-4] == "Population":
                g.add((uoft[subj], RDF.type, uoft.MalePopulation))
                g.add((uoft.MalePopulation, iso21972.defined_by, uoft.Male))
                g.add((uoft.Male, rdfs.subClassOf, foaf.Person))
            else:
                obje = indicator[:-4] + "MalePopulation"
                g.add((uoft[subj], RDF.type, uoft[obje]))
                g.add((uoft[obje], rdfs.subClassOf, iso21972.Population))
                obje2 = "Male" + indicator
                g.add((uoft[obje], iso21972.defined_by, uoft[obje2]))
                g.add((uoft[obje2], rdfs.subClassOf, foaf.Person))
                
            g.add((uoft[subj], iso21972.located_in, toronto[censustract]))
            g.add((uoft[subj], uoft.hasTime, uoft.censusProfile2016DateTimeInterval))
        else:
            subj = censustract + indicator + "MalePopulation"
            g.remove((uoft[subj], None, None))
        
        # Creates triple: censusTractIndicatorFemaleMeasure numerical_value integer or decimal
        subj = censustract + indicator + "FemaleMeasure"
        if "." in str(row.Female):
            g.add((uoft[subj], iso21972.hasNumericalValue, Literal(row.Female, datatype=XSD.decimal)))
        else:
            g.add((uoft[subj], iso21972.hasNumericalValue, Literal(row.Female, datatype=XSD.integer)))
        # Creates triple: censusTractIndicatorFemaleMeasure type Measure
        g.add((uoft[subj], RDF.type, iso21972.Measure))
        
        # Calls the add_unit function to assign an appropriate unit for the Indicator
        add_unit(subj, i)
        # If the Indicator hasUnit population_cardinality_unit, link it to the corresponding Population instance
        if (uoft[subj], iso21972.hasUnit, iso21972.population_cardinality_unit) in g:
            subj = censustract + indicator + "Female"
            obje = subj + "Population"
            g.add((uoft[subj], iso21972.cardinality_of, uoft[obje]))
            
            subj = obje
            if indicator[:-4] == "Population":
                g.add((uoft[subj], RDF.type, iso21972.FemalePopulation))
                g.add((uoft.FemalePopulation, iso21972.defined_by, uoft.Female))
                g.add((uoft.Female, rdfs.subClassOf, foaf.Person))
            else:
                obje = indicator[:-4] + "FemalePopulation"
                g.add((uoft[subj], RDF.type, uoft[obje]))
                g.add((uoft[obje], rdfs.subClassOf, iso21972.Population))
                obje2 = "Female" + indicator
                g.add((uoft[obje], iso21972.defined_by, uoft[obje2]))
                g.add((uoft[obje2], rdfs.subClassOf, foaf.Person))
                
            g.add((uoft[subj], iso21972.located_in, toronto[censustract]))
            g.add((uoft[subj], uoft.hasTime, uoft.censusProfile2016DateTimeInterval))
        else:
            subj = censustract + indicator + "FemalePopulation"
            g.remove((uoft[subj], None, None))
            
        # Creates triple: censusTractIndicatorMale value censusTractIndicatorMaleMeasure
        subj = censustract + indicator + "Male"
        obje = censustract + indicator + "MaleMeasure"
        g.add((uoft[subj], RDF.type, uoft[indicator]))
        g.add((uoft[subj], iso21972.hasValue, uoft[obje]))
        # Creates triple: censusTractIndicatorMaleMeasure forQuantity censusTractIndicatorMale
        g.add((uoft[obje], uoft.forQuantity, uoft[subj]))
        # Links the Male Indicator to the CensusTract using hasLocation
        obje = censustract
        g.add((uoft[subj], uoft.hasLocation, toronto[obje]))
        # Creates triple: censusTractIndicatorFemale value censusTractIndicatorFemaleMeasure
        subj = censustract + indicator + "Female"
        obje = censustract + indicator + "FemaleMeasure"
        g.add((uoft[subj], RDF.type, uoft[indicator]))
        g.add((uoft[subj], iso21972.hasValue, uoft[obje]))
        # Creates triple: censusTractIndicatorFemaleMeasure forQuantity censusTractIndicatorFemale
        g.add((uoft[obje], uoft.forQuantity, uoft[subj]))
        # Links the Female Indicator to the CensusTract using hasLocation
        obje = censustract
        g.add((uoft[subj], uoft.hasLocation, toronto[obje]))

    count += 1
        
    # Prints progress of the program
    print("Completed " + str(count) + "/572", end="\r")
    
    # Saves the graph as a turtle file 
    if count % 10 == 0 or count == 572:
        filename = "CensusSample" + str(count) + ".ttl"
        g.serialize(destination=filename, format="turtle")
        del g
        g = Graph()
    
      
# Print time needed to execute the program
print("--- %s seconds ---" % (time.time() - start_time))
print("\nDone")



