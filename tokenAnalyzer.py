import json
import re
import simplemma
import argparse
from datetime import datetime
import pandas as pd

def get_token_counts(partyDict:dict, monthFrom:int, yearFrom:int, monthTo:int, yearTo:int) -> dict:
    tokenCounts = { party: {} for party in partyDict.values() }
    wordCounts = { party: 0 for party in partyDict.values() }
    for partyName in partyDict.values():
        start = datetime.now()
        docDict = dict()
        with open(f"party-texts/{partyName}_from_{monthFrom}_{yearFrom}_to_{monthTo}_{yearTo}.txt", encoding='UTF-8') as f: 
            partyFile = f.read()
            partyLines = partyFile.split("\n\n")
            for line in partyLines:
                linetoks = re.split(r'[^a-zA-Zа-яА-Я0-9]+', line)
                for token in linetoks:
                    if token != '':
                        lemma = simplemma.lemmatize(token, lang='bg')
                        docDict[lemma] = docDict.get(lemma, 0) + 1

        tokenCounts[partyName] = docDict

        # with open(f"party-texts/{partyName}.pickle", 'wb') as file:
        #         pickle.dump(docSet, file, protocol=pickle.HIGHEST_PROTOCOL)
        # print(f"Party {partyName} done in {datetime.now() - start}")
    return tokenCounts

def save_vocabulary_lengths(token_counts:dict, monthFrom:int, yearFrom:int, monthTo:int, yearTo:int) -> None:
    speech_data = pd.read_csv(f'party-texts/speech_counts_from_{monthFrom}_{yearFrom}_to_{monthTo}_{yearTo}.csv', delimiter='\t')
    with open(f'party-texts/vocab_lens_from_{monthFrom}_{yearFrom}_to_{monthTo}_{yearTo}.csv', 'w', encoding = 'utf-8') as writeFile:
        writeFile.write("party\tvocab_len\tword_count\ttotal_speeches\tratio\n")
        for party, counts in token_counts.items():
            total_speeches = speech_data.loc[speech_data['party'] == party, 'all_speeches'].item() # type: ignore
            vocab_len = len(counts.keys())
            word_count = sum(counts.values())
            ratio = vocab_len / word_count # Very skewy - TODO: Implement different lexical diversity measures
            writeFile.write(f"{party}\t{vocab_len}\t{word_count}\t{total_speeches}\t{ratio}\n")

if __name__ == "__main__":
    # example: python .\tokenAnalyzer.py - defaults to whole current year
    # example: python .\tokenAnalyzer.py -mF 1 -yF 2024 -mT 12 -yT 2024 - arguments: monthFrom, yearFrom, monthTo, yearTo
    # simplemma.lemmatize(token, lang='bg')

    parser = argparse.ArgumentParser()
    parser.add_argument("-mF", "--monthFrom", help="starting month", type=int, default=1)
    parser.add_argument("-yF", "--yearFrom", help="starting year", type=int, default=datetime.now().year)
    parser.add_argument("-mT", "--monthTo", help="ending month", type=int, default=datetime.now().month)
    parser.add_argument("-yT", "--yearTo", help="ending year", type=int, default=datetime.now().year)
    args = parser.parse_args()



    # reading the party data 
    with open('partyFileNameDict.json', encoding='UTF-8') as f: 
        partyData = f.read() 

    # reconstructing the data as a dictionary 
    partyDict = json.loads(partyData)

    token_counts = get_token_counts(partyDict, args.monthFrom, args.yearFrom, args.monthTo, args.yearTo)
    save_vocabulary_lengths(token_counts, args.monthFrom, args.yearFrom, args.monthTo, args.yearTo)
