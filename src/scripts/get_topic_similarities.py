import pandas as pd
import swifter # Looks unused but actually is through Monkey Patching -- don't delete
import matplotlib.pyplot as plt
import re
import geopandas as gpd
from src.utils.data_utils import *
from src.utils.general_utils import *
from tqdm import tqdm
from prettytable import PrettyTable
from ipywidgets import interact
from gensim.models import LdaMulticore
import pickle as pkl
import numpy as np
import gensim.downloader as api
from itertools import chain
from functools import cache
from tqdm import tqdm
from multiprocessing import Pool
from sklearn.metrics.pairwise import cosine_similarity

pd.options.mode.copy_on_write = True

RAW_DATA_FOLDER = "data/raw/"
CMU_MOVIES_DS = ProjectDataset(RAW_DATA_FOLDER+"movie.metadata.tsv",
                               "CMU Movies",
                               "Base dataset for ADA. Contains ~80K movies and their metadata.",
                               {
                                    "wikipedia_id": "A UID for the movie on Wikipedia.",
                                    "freebase_id": "A UID for the movie in Freebase (https://freebase.toolforge.org/)",
                                    "title": "The title of the movie.",
                                    "release_date": "The date the movie was officially released. (<YEAR>, or <YYYY-MM-DD>)",
                                    "box_office_revenue": "The total revenue of the movie",
                                    "runtime": "The duration of the movie, minutes (float).",
                                    "languages": "The languages spoken in the movie. Dict[<Freebase Language Identifier String>:<Language>]",
                                    "countries": "The countries where the movie was produced or primarily associated. Dict[<Freebase Country Identifier String>:<Country>]",
                                    "genres": "Movie genre(s), such as action, drama, comedy, ..."
                                }
)
CMU_PLOTS_DS = ProjectDataset(RAW_DATA_FOLDER+"plot_summaries.txt",
                              "CMU plots",
                              "Base dataset for ADA. Contains a plot summary for each of the movie in the CMU Movies dataset",
                              {
                                  "wikipedia_id":"The UID corresponding to the movie",
                                  "plot": "The (summarized) plot of the movie"
                              })

embedding_model = api.load("glove-wiki-gigaword-100")
@cache
def get_embedding(word_s):
    try:
        return embedding_model[word_s]
    except KeyError:
        return np.zeros((100,))
def embed_lst(lst):
    return [get_embedding(e) for e in lst]
@cache
def get_distance(e1,e2):
    return np.dot(e1, e2)/(np.linalg.norm(e1)*np.linalg.norm(e2))



def find_closest_topic(e_topics,compared_lst):
    for (kw, weight) in compared_lst:
        weighted_vectors = []
        weights = []
        # Embed the topic in the tuple
        embedded_topic = get_embedding(kw)
        
        # Compute cosine similarity with all main topics
        similarities = cosine_similarity([embedded_topic], e_topics)[0]

        # Store weighted similarity and weights
        weighted_vectors.append(similarities * weight)
        weights.append(weight)
    similarities = np.sum(weighted_vectors, axis=0) / np.sum(weights)
    return similarities



# Wrapper function for parallel processing
def find_closest_wrapper(args):
    e_sc_topics, kw_plot = args
    return find_closest_topic(e_sc_topics, kw_plot)

# Parallelized version using Pool.imap
def parallel_find_closest(e_sc_topics, cmu_kw):
    num_processes = 10  # Adjust based on your system
    
    with Pool(num_processes) as pool:
        # Use imap for efficient parallel processing with tqdm for progress
        args = [(e_sc_topics, kw_plot) for kw_plot in cmu_kw]
        out_similarities = np.array(list(tqdm(pool.imap(find_closest_wrapper, args), total=len(cmu_kw))))

    print("Finished computing similarities, aggregating")
    N = len(cmu_kw)
    # out_similarities is a N,len(e_sc_topics) array
    assert tuple(out_similarities.shape) == (N,len(e_sc_topics))
    per_topic_mean = out_similarities.mean(axis=0)
    assert per_topic_mean.shape[0] == len(e_sc_topics)
    out_similarities = (out_similarities - per_topic_mean)
    out_idcs = np.argmax(out_similarities,axis=1) 
    assert len(out_idcs) == N

    return out_idcs


if __name__ == "__main__":
    with open("cmu_concepts.pkl","rb") as f:
        cmu_kw = pkl.load(f)
    socio_cultural_topics = [
        "identity",
        "migration",
        "gender",
        "race",
        "class",
        "faith",
        "trauma",
        "family",
        "tradition",
        "freedom",
        "justice",
        "power",
        "oppression",
        "conflict",
        "diversity",
        "activism",
        "colonialism",
        "privilege",
        "community",
        "globalization",
        "alienation",
        "memory",
        "violence",
        "resistance",
        "humanity"
    ]
    e_sc_topics = embed_lst(socio_cultural_topics)
    out = parallel_find_closest(e_sc_topics, cmu_kw)

    comedy_topics = [
        "love",
        "marriage",
        "family",
        "friendship",
        "dating",
        "workplace",
        "money",
        "politics",
        "fame",
        "identity",
        "rivalry",
        "embarrassment",
        "miscommunication",
        "luck",
        "parenting",
        "travel",
        "school",
        "aging",
        "crime",
        "revenge",
        "popculture",
        "jealousy",
        "superstition",
        "fantasies",
        "awkwardness"
    ]
    e_ct_topics = embed_lst(comedy_topics)
    out_ct = parallel_find_closest(e_ct_topics, cmu_kw)
    historical_events = [
        "revolution",
        "war",
        "genocide",
        "colonization",
        "independence",
        "migration",
        "industrialization",
        "civilization",
        "uprising",
        "exploration",
        "partition",
        "dictatorship",
        "holocaust",
        "prohibition",
        "renaissance",
        "depression",
        "unionization",
        "expansion",
        "reformation",
        "imperialism",
        "abolition",
        "enlightenment",
        "assassination",
        "annexation",
        "reconstruction"
    ]
    e_he = embed_lst(historical_events)
    out_he = parallel_find_closest(e_he, cmu_kw)
    mixed_topics = [
        "society",     # Ethical dilemmas: likely handled very differently in comedies
        "war",          # War: often a source of both comedy and serious commentary
        "gender",       # Gender roles and relationships: evolved significantly over time
        "justice",      # How comedies vs dramas handle fairness and revenge
        "technology",   # Society's relationship with tech: different approaches
        "money",     # Keep this one as it's fundamental but handled differently by genre
        "love",
        "revolution",
    ]
    e_mt = embed_lst(mixed_topics)
    out_mt = parallel_find_closest(e_mt, cmu_kw)
    CMU_MOVIES_DS.df.loc[62836,"release_date"] = "2010-12-02"
    CMU_MOVIES_DS.df.loc[:,"year"] =  pd.to_datetime(CMU_MOVIES_DS.df.release_date,format="mixed").apply(lambda x:x.year)
    CMU_PLOTS_DS.df.loc[:,"cSC"] =  out
    CMU_PLOTS_DS.df.loc[:,"cCT"] =  out_ct
    CMU_PLOTS_DS.df.loc[:,"cHE"] =  out_he
    CMU_PLOTS_DS.df.loc[:,"cMT"] =  out_mt
    merged = CMU_PLOTS_DS.df.merge(CMU_MOVIES_DS.df,on="wikipedia_id",how="inner",validate="1:1")
    merged["genres"] = merged["genres"].apply(ast.literal_eval).apply(lambda d: set(d.values()))
    merged.to_csv("cmu_topic_similarities.csv")
