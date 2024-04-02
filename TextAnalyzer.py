from nltk.util import ngrams
from nltk.probability import FreqDist
import os
import json

def CalculateNGrams(partyDict):
    for partyText in os.listdir('party-texts'):
        if partyText == 'VUZRAZHDANE.txt':
            with open(f'party-texts/{partyText}', 'r', encoding='utf-8') as readFile:
                # Tokenize the text 
                partyTokens = readFile.read()\
                                        .replace("\n","").replace(".", " ").replace("?", " ").replace("!", " ").replace(",", " ").replace("  ", " ")\
                                        .split(' ')

                wordsToRemove = ["Уважаеми", "Уважаема", "уважаеми", "уважаема", "Господин", "Госпожо", "господин", "госпожо", "председател", "Председател",
                "господа", "Господа", "народни", "Народни", "представители", "Против", "За", ""]
                
                partyTokens = list(filter(lambda word: word not in wordsToRemove, partyTokens))

                ngramList = list(ngrams(partyTokens,3))
                freqDist = FreqDist(ngramList)

                print(freqDist.most_common()[:200])
                



if __name__ == "__main__":
    # example: python .\TextAnalyzer.py

    # reading the party data 
    with open('partyFileNameDict.json', encoding='UTF-8') as f: 
        partyData = f.read() 

    # reconstructing the data as a dictionary 
    partyDict = json.loads(partyData)

    CalculateNGrams(partyDict)
