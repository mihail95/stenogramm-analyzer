import sys
import os
from datetime import datetime
import re
import json
from Levenshtein import distance

def GetFileNames(yearToQuery, monthToQuery):
    files = []
    directory = f'{yearToQuery}'
    for subdir in os.listdir(directory):
        if (int(subdir) >= int(monthToQuery)):
            subDirectory = os.path.join(directory, subdir)
            for filename in os.listdir(subDirectory):
                f = os.path.join(subDirectory, filename)
                # checking if it is a file
                if os.path.isfile(f):
                    files.append(f)
    return files

def PartyTextExtractorMain(yearToQuery, monthToQuery):
    # reading the data from the file 
    with open('partyFileNameDict.json', encoding='UTF-8') as f: 
        partyData = f.read() 

    # reconstructing the data as a dictionary 
    partyDict = json.loads(partyData)

    fileNames = GetFileNames(yearToQuery, monthToQuery)
    for fileName in fileNames:
        with open(fileName, encoding = 'utf-8') as file:
            # Find a speech made from a party
            # Regex: "^([А-Я\s]+)(\(.*\))*:([\S\s]*?)(?=^([А-Я\s]+)(\(.*\))*:|\Z)"gm
            for party in re.findall(r"^([А-Я\s]+)(\(.*\))*:([\S\s]*?)(?=^([А-Я\s]+)(\(.*\))*:|\Z)", file.read(), re.M):
                partyFolder = None
                partyNamePattern = r'^\(([А-Яа-я -]+),*.*\)$'
                partyNameMatch = re.search(partyNamePattern, party[1])
                # Use levenstein to try and find a matching party name
                if (partyNameMatch != None and partyNameMatch[1].upper() not in partyDict.keys()):
                    cutoff = 2
                    partyNameDistanceDict = {partyName : distance(partyNameMatch[1].upper(), partyName, score_cutoff=cutoff, weights=(0,1,5)) for partyName in partyDict}
                    minimum = min(partyNameDistanceDict.items(), key=lambda x: x[1])
                    if minimum[1] < cutoff + 1: partyFolder = partyDict[minimum[0]]                    
                elif (partyNameMatch != None and partyNameMatch[1].upper() in partyDict.keys()):
                    partyFolder = partyDict[partyNameMatch[1].upper()]

                # If a match is found, write the text to the corresponding file
                if partyFolder != None: 
                    with open(f'party-texts/{partyFolder}.txt', 'a+', encoding = 'utf-8') as writeFile:
                        writeFile.write(party[2].replace("<br>", "").strip() + '\n\n')

                


if __name__ == "__main__":
    # Usage: python .\PartyTextExtractor.py yearToQuery monthToQuery - either parameter defaults to datetime.now()
    # example: python .\PartyTextExtractor.py 2024 5
    yearToQuery = sys.argv[1] if len(sys.argv)>1 else datetime.now().year
    monthToQuery = sys.argv[2] if len(sys.argv)>2 else 1
    PartyTextExtractorMain(yearToQuery, monthToQuery)