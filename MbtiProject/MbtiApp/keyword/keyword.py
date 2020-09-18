import pandas as pd
from soynlp.noun import LRNounExtractor

def get_keyword(characters):
    df = pd.read_csv("./MbtiApp/keyword/roles.csv")
    stopwords = pd.read_csv("./MbtiApp/keyword/stopwords.csv")["stopwords"]
    sentences = df.iloc[:,2]
    sentences = list(sentences) + list(characters["feature_total"])
    # 명사 추출
    noun_extractor = LRNounExtractor()
    nouns = noun_extractor.train_extract(sentences)
    nouns = sorted(nouns, key = lambda x: len(x), reverse=True)

    # stopwords 제거
    for sw in stopwords:
        if sw in nouns:
            nouns.remove(sw)
    
    personal = []
    for i, row in characters.iterrows():
        noun_sen = ""
        for noun in nouns:
            if noun in row["feature_total"]:
                noun_sen = noun_sen  + " #" + noun
        personal.append(noun_sen)
    characters["personal"] = personal
    return characters
        