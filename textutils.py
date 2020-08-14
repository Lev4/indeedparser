import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from spacy.lang.en import English
from spacy.matcher import Matcher
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import random

# Исключаемые сущности для Spacy
stop_labels = [
    "GPE",
    "ORG",
    "DATE",
    "CARDINAL",
    "LOC",
    "ORDINAL",
    "PERSON",
    "TIME",
    "LANGUAGE",
    "NORP",  # Nationalities or religious or political groups.
    "FAC",  # Buildings, airports, highways, bridges, etc.
    "EVENT",  # Named hurricanes, battles, wars, sports events, etc.
    "PERCENT",  # Percentage, including ”%“.
    "MONEY",  # Monetary values, including unit.
    "QUANTITY",  # Measurements, as of weight or distance.
]



def requirements_extractor(doc, matcher=matcher):
    endpos = None
    matches = matcher(doc)

    if len(matches) > 0:
        startpos = matches[0][1]
        for el in doc[startpos:]:
            if len(el.text.split("\n")) > 2 and (el.i) < len(doc):
                #                 print(doc[el.i+1], el.i+1)
                endpos = el.i + 1
                break
    if endpos:
        return doc[startpos:endpos]
    else:
        return None


def get_enteties_list(vacs_desc, max_ents=None):
    stop_labels = [
        "GPE",
        "ORG",
        "DATE",
        "CARDINAL",
        "LOC",
        "ORDINAL",
        "PERSON",
        "TIME",
        "LANGUAGE",
        "NORP", # Nationalities or religious or political groups.
        "FAC", # Buildings, airports, highways, bridges, etc.
        "EVENT", #Named hurricanes, battles, wars, sports events, etc.
        "PERCENT", #Percentage, including ”%“.
        "MONEY", #Monetary values, including unit.
        "QUANTITY", #Measurements, as of weight or distance.
    ]
    entslist = []
    for s in tqdm(vacs_desc):
        doc = nlp(s)
        for ent in doc.ents:
            if ent.label_ not in stop_labels:
                entslist.append((ent.text.strip('\n'), ent))
    if max_ents:
        if len(entslist)> max_ents:
            entslist = random.sample(entslist,max_ents)
    return entslist


def get_enteties_dict(vtab, professions, max_ents=None):
    """ Создает словарь списков именованных сущностей """
    entsdict = {}
    for p in professions:
        term_prof = vtab.profession == p
        vacs_desc = vtab[term_prof]['description'].tolist()
        entslist = get_enteties_list(vacs_desc, max_ents=None)
        entsdict[p] = entslist

    return entsdict





def get_matrix(entslist):
    """ Собирает матрицу векторов именованных сущностей и их названий """

    entsmx_vectors = []
    entsmx_name = []
    for el in entslist:
        if el[0] not in entsmx_name and el[1].has_vector:
            entsmx_vectors.append(el[1].vector)
            entsmx_name.append(el[0])
    entsmx = np.vstack(entsmx_vectors)
    return entsmx, entsmx_name


def get_cs_df(entsmx, entsmx_name):
    """ Формирует датафрейм из косинусного сходства"""

    cs = cosine_similarity(entsmx)
    csdf = pd.DataFrame(cs, columns=entsmx_name)
    csdf['tag'] = entsmx_name
    csdf = csdf.set_index('tag')
    return csdf


def get_similiarities_from_df(csdf):
    """Создает словарь сходств сущностей """

    simsdict = {}
    for col in tqdm(csdf.columns):
        simsdict[col] = dict(zip(csdf.index.tolist(), csdf[col].tolist()))
    return simsdict


def get_similiarities(entslist):
    """ Тупо сравнивает сходство циклом в цикле """

    entslist2 = [x[1] for x in entslist]
    simsdict = {}
    for e1 in tqdm(entslist2):
        simtemp= {}
        if e1.has_vector:
            for e2 in entslist2:

                if e2.has_vector:
                    simtemp[e2.text] = e1.similarity(e2)
        simsdict[e1.text] = simtemp
    return simsdict

def get_duplicates(simsdict, min_sim_score=0.7):
    """Формирует словарь дубликатов из сущностей с высоким сходством """

    tags = list(simsdict.keys())
    duplicates = {}
    for t in tags:
        items_sorted = sorted(simsdict[t].items(), key=lambda x: x[1], reverse=True)
        duplicates[t] = [x[0] for x in items_sorted if x[1] > min_sim_score]
    return duplicates


def get_frequencies(entslist, duplicates):
    """ Добавляет к словарю дубликатов частоту их встречаемости """

    c = Counter([x[0] for x in entslist])
    list_of_sets = [set([k, *v]) for k, v in duplicates.items()]
    unique_sets = []
    for el in list_of_sets:
        if el not in unique_sets:
            unique_sets.append(el)

    unique_sets_with_frequency = []
    for el in unique_sets:
        new_list = list(el)
        new_tup_list = [(x, c[x]) for x in new_list]
        new_tup_list = sorted(new_tup_list, key=lambda x: x[1], reverse=True)
        unique_sets_with_frequency.append(new_tup_list)
    return unique_sets_with_frequency


def get_duplicate_tags_dict(unique_sets_with_frequency):
    """Формирует словарь дубликатов из наиболее часто встречающихся"""

    dtags_dict = {}
    for elset in unique_sets_with_frequency:
        taglabel = None
        tag_total_frequency = sum([x[1] for x in elset])
        for i, t in enumerate(elset):
            if i == 0:
                taglabel = t[0]
            if taglabel:
                dtags_dict[t[0]] = [taglabel, tag_total_frequency]
    return dtags_dict


def get_frame(dtags_dict, min_frequency=None, ):
    """Формирует датафрейм названий сущностей и частоты их встречаемости"""

    newtags = []
    for k, v in dtags_dict.items():
        if v not in newtags:
            if v[0] not in stops:
                newtags.append(v)

    ftab = pd.DataFrame(newtags, columns=['tag', 'freq'])
    gtab = ftab.groupby('tag')['freq'].sum().reset_index().sort_values(by='freq', ascending=False)

    if min_frequency:
        gtab = gtab[gtab.freq > min_frequency].copy()
    return gtab


# Визуализация результатов
def make_df(ed_stripped, keyword, n=30, stops=stops):
    tablist = ed_stripped[keyword]
    tablist = [x for x in tablist if x[0] not in stops]
    df = pd.DataFrame(tablist, columns=['name', 'frequency'])
    if n:
        df = df[df.frequency > n]
    return df


def make_barplot(df, keyword=""):
    sns.set(style="whitegrid")

    f, ax = plt.subplots(figsize=(6, 15))
    sns.set_color_codes("pastel")
    sns.barplot(x="frequency", y="name", data=df,
                label="frequency", color="b")

    #     sns.countplot(y="name",label="frequency", data=df)

    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(ylabel="",
           xlabel="Frequency", title=keyword)

    sns.despine(left=True, bottom=True)


def show_tags(ed_stripped, keyword, n=20):
    df = make_df(ed_stripped, keyword, n=n)
    make_barplot(df, keyword=keyword)


def get_skills_df(vacs_desc):
    reqs = get_requirements(vacs_desc)
    reqs_ent1 = get_enteties_list(reqs)
    entsmx, entsmx_name = get_matrix(reqs_ent)
    csdf1 = get_cs_df(entsmx, entsmx_name)
    simsdictac = get_similiarities_from_df(csdf1)
    duplicatesac = get_duplicates(simsdictac, min_sim_score=0.5)
    unique_sets_with_frequencyac = get_frequencies(reqs_ent1, duplicatesac)
    dtags_dictac = get_duplicate_tags_dict(unique_sets_with_frequencyac)
    dfac = get_frame(dtags_dictac, min_frequency=None)
    return dfac


def get_requirements(vacs_desc):
    reqs = []
    for s in tqdm(vacs_desc):
        doc = nlp(s)
        res = requirements_extractor(doc)
        if res:
            if len(res) > 4:
                reqs.append(res.text)
    return reqs
