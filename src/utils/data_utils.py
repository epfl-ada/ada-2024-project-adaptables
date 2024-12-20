import swifter
from dataclasses import dataclass
from functools import cached_property
import pandas as pd
from pathlib import Path
import ast
from ..data.project_dataset import ProjectDataset
from .general_utils import all_valid,normalize_sa,zscore
from pathlib import Path

def prepro_cmu_movies(movies_df: pd.DataFrame) -> pd.DataFrame:
    new_df = movies_df.copy()
    new_df["languages"] = new_df["languages"].swifter.apply(lambda lang_dict_as_str: list(ast.literal_eval(lang_dict_as_str).values()))
    new_df["countries"] = new_df["countries"].swifter.apply(lambda lang_dict_as_str: list(ast.literal_eval(lang_dict_as_str).values()))
    new_df["genres"] = new_df["genres"].swifter.apply(lambda lang_dict_as_str: list(ast.literal_eval(lang_dict_as_str).values()))
    def parse_release_date(release_date_str):
        # The release date is :
        #       either empty
        #       or YYYY
        #       or YYYY-MM-DD
        # --> since we're simply inetrested in the year, we can just take the first 4 characters  
        if isinstance(release_date_str,float):
            return release_date_str
        return release_date_str.strip()[:4]
    new_df["release_date"] = pd.to_numeric(new_df["release_date"].swifter.apply(parse_release_date), errors="coerce",downcast="unsigned") # this will set a NaN wherever we don't have a date
    return new_df

# ============
# Functions used to preprocess Massive Rotten Tomatoes reviews dataset
# ============

def mrt_standardize_score(note):
    if isinstance(note, str) and '/' in note:
        try:
            numerator, denominator = map(float, note.split('/'))
            if denominator == 0:  
                return None
            if (numerator / denominator)<=1 :
                return numerator / denominator
        except (ValueError, TypeError): 
            return None
    else:
        return None
    
def mrt_preprocess_df(df, col1, col2, merge_col, expert, comedy_ids:pd.Series, comedy: bool, use_zscore= False):
    # Preprocesses the MRT df to get the standardized score only (z-score, or simply bounded between 0-1),
    df = df[df['isTopCritic'] == expert].copy()
    if comedy:
        df = df[df[merge_col].isin(comedy_ids)]
    else:
        df = df[~df[merge_col].isin(comedy_ids)]

    df[col1] = df[col1].apply(mrt_standardize_score)
    df[col2] = zscore(df[col2]) if use_zscore else df[col2].apply(normalize_sa)
        
    df1 = df.groupby(merge_col)[col1].mean().reset_index()
    df2 = df.groupby(merge_col)[col2].mean().reset_index()
    df1 = df1.dropna()
    df2 = df2.dropna()

    return df1, df2 


# =
# Other
# = 

PREPROCESSED_DATA_DIR = "data/processed/"

class ExtraDatasetInfo:
    # This class will hold any additional information we infer from our base datasets
    # Some of this took time (and resources) to compute, which is why we have cached it in the `data/processed` directory.
    # If you wish to re-compute everything from scratch, set `preload` to false (NOT RECOMMENDED!) 
    def __init__(self, mrt_movies_ds: ProjectDataset,preload=True):
        all_valid(mrt_movies_ds)

        if preload:
            # The comedy ids in the massive rottent tomatoes dataset \inter CMU, where experts have given their opinions  
            mrtexp_fpath = Path(PREPROCESSED_DATA_DIR+"ratings_expert.csv") 
            assert mrtexp_fpath.exists() and mrtexp_fpath.is_file()
            self.mrt_cmu_expertrevd_comedy_ids = pd.read_csv(mrtexp_fpath.absolute().as_posix())["id"]
        
            # The massive RT dataset, extended with a sentiment analysis score for the entries with a review (~1.3M out of the 1.4M reviews):
            mrtsa_fpath = Path(PREPROCESSED_DATA_DIR+"reviews_with_compound.csv") 
            assert mrtsa_fpath.exists() and mrtsa_fpath.is_file()
            self.mrtrev_sa_df = pd.read_csv(mrtsa_fpath.absolute().as_posix())
        else:
            raise ValueError("See ./data/preprocessed/README.md for an indication on how to recreate the preloaded data")


