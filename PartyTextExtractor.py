import sys
import os
from datetime import datetime
import re

def GetFileNames(yearToQuery):
    files = []
    directory = f'{yearToQuery}'
    for subdir in os.listdir(directory):
        subDirectory = os.path.join(directory, subdir)
        for filename in os.listdir(subDirectory):
            f = os.path.join(subDirectory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                files.append(f)
    return files

def PartyTextExtractorMain(yearToQuery):
    partyDict = {"български възход": "bulgarski_vuzhod", 
                "бсп за българия": "BSP",
                "възраждане": "vuzrazhdane",
                "герб-сдс": "GERB-SDS",
                "да българия": "DB",
                "дб": "DB",
                "дпс": "DPS",
                "итн": "ITN",
                "продължаваме промяната": "PP",
                "пп": "PP",
                "пп-дб": "PP-DB"}

    fileNames = GetFileNames(yearToQuery)
    for fileName in fileNames:
        with open(fileName, encoding = 'utf-8') as file:
            # Regex: [А-Яа-я ]*\(([А-Яа-я -]*),*.*\):([\w\W]*?)(?:ПРЕДСЕДАТЕЛ|ИСКРА) - change ИСКРА to something that matches any name
            for party in re.findall(r"[А-Яа-я ]*\(([А-Яа-я -]*),*.*\):", file.read()):
                party = party.strip()
                if "," in party.lower():
                    party = party.replace(",", "")
                if "от място" in party.lower():
                    party = party.replace("от място", "")
                if "встрани от микрофоните" in party.lower():
                    party = party.replace("встрани от микрофоните", "")
                if "реплика от" in party.lower():
                    party = party.replace("Реплика от", "")

                if party.lower() in partyDict.keys():
                    print(f"HIT: {party}")
                else:
                    print(f"MISS: {party}")
    
    

if __name__ == "__main__":
    yearToQuery = sys.argv[1] if len(sys.argv)>1 else datetime.now().year
    PartyTextExtractorMain(yearToQuery)