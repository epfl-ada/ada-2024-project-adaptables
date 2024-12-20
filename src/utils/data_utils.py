import swifter
from dataclasses import dataclass
from functools import cached_property
import pandas as pd
from pathlib import Path
import ast
from ..data.project_dataset import ProjectDataset
from .general_utils import all_valid,normalize_sa,zscore
from pathlib import Path

# ============ ============ ============ ============ ============ ============
# Functions used to preprocess Massive Rotten Tomatoes reviews dataset
# ============ ============ ============ ============ ============ ============

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




# ============ ============ ============ ============ ============ ============
# Functions used to preprocess movie awards dataset (oscars)
# ============ ============ ============ ============ ============ ============
def rename_oscars_cols(oscars_df): #renamed_oscars
    return oscars_df.rename(columns={'film':'title', 'year_film':'release_date'})


def prepare_award_comparison_data(movies_awards_df):
    """
    Prepares the data for comparing total award-winning movies and award-winning comedies by country.
    
    Args:
        movies_awards_df (DataFrame): DataFrame containing award data with 'winner', 'genres', and 'countries'.
    
    Returns:
        DataFrame: A DataFrame with 'countries', total winning movies, and winning comedies.
    """
    winning_movies = movies_awards_df[movies_awards_df['winner'] == True]
    winning_movies = winning_movies.explode('countries')
    
    total_award_winning = winning_movies.groupby('countries').size().reset_index(name='Winning_Movies_Total')
    
    winning_comedies = winning_movies[winning_movies['genres'].apply(lambda genres: 'Comedy' in genres)]
    comedy_award_winning = winning_comedies.groupby('countries').size().reset_index(name='Winning_Comedies')
    
    country_comparison = total_award_winning.merge(comedy_award_winning, on='countries', how='outer').fillna(0)
    
    country_comparison['Winning_Movies_Total'] = country_comparison['Winning_Movies_Total'].astype(int)
    country_comparison['Winning_Comedies'] = country_comparison['Winning_Comedies'].astype(int)
    
    country_comparison['Comedy_Percentage'] = (country_comparison['Winning_Comedies'] / country_comparison['Winning_Movies_Total']) * 100
    country_comparison['Comedy_Percentage'] = country_comparison['Comedy_Percentage'].fillna(0)

    country_comparison = country_comparison.sort_values(by='Comedy_Percentage', ascending=False)
    country_comparison = country_comparison.sort_values(by='Winning_Movies_Total', ascending=False)
    
    return country_comparison



# ============ ============ ============ ============ ============ ============
# Functions used to preprocess CMU
# ============ ============ ============ ============ ============ ============

def prepro_cmu_movies(cmu_movies_df: pd.DataFrame) -> pd.DataFrame: # cmu_cleaned_movies
    new_df = cmu_movies_df.copy()
    new_df["languages"] = new_df["languages"].apply(lambda lang_dict_as_str: list(ast.literal_eval(lang_dict_as_str).values()))
    new_df["countries"] = new_df["countries"].apply(lambda lang_dict_as_str: list(ast.literal_eval(lang_dict_as_str).values()))
    new_df["genres"] = new_df["genres"].apply(lambda lang_dict_as_str: list(ast.literal_eval(lang_dict_as_str).values()))
    # def parse_release_date(release_date_str):
    #     # The release date is :
    #     #       either empty
    #     #       or YYYY
    #     #       or YYYY-MM-DD
    #     # --> since we're simply inetrested in the year, we can just take the first 4 characters  
    #     if isinstance(release_date_str,float):
    #         return release_date_str
    #     return release_date_str.strip()[:4]
    # new_df["release_date"] = pd.to_numeric(new_df["release_date"].swifter.apply(parse_release_date), errors="coerce",downcast="unsigned") # this will set a NaN wherever we don't have a date
    new_df.loc[62836,"release_date"] = "2010-12-02"
    new_df.loc[:,"release_date"] = pd.to_datetime(new_df.release_date,format="mixed").apply(lambda x:x.year)
    return new_df

def prepare_revenue_comparison_data(cmu_cleaned_movies):
    """
    Prepares the data for comparing total box office revenue and comedy box office revenue by country.
    
    Args:
        cmu_cleaned_movies (DataFrame): DataFrame containing movie data with 'box_office_revenue', 'genres', and 'countries'.
    
    Returns:
        DataFrame: A DataFrame with 'countries', total revenue, and comedy revenue.
    """
    movies_with_revenue = cmu_cleaned_movies[cmu_cleaned_movies['box_office_revenue'].notna()]
    movies_with_revenue = movies_with_revenue.explode('countries')

    total_revenue = (movies_with_revenue.groupby('countries')['box_office_revenue']
                    .sum()
                    .reset_index(name='Total_Revenue'))

    comedy_movies = movies_with_revenue[
        movies_with_revenue['genres'].apply(lambda genres: 'Comedy' in genres)
    ]
    comedy_revenue = (comedy_movies.groupby('countries')['box_office_revenue']
                     .sum()
                     .reset_index(name='Comedy_Revenue'))

    country_comparison = total_revenue.merge(comedy_revenue, on='countries', how='outer').fillna(0)

    country_comparison['Comedy_Percentage'] = (
        country_comparison['Comedy_Revenue'] / country_comparison['Total_Revenue'] * 100
    )
    country_comparison['Comedy_Percentage'] = country_comparison['Comedy_Percentage'].fillna(0)

    country_comparison = country_comparison.sort_values(by='Total_Revenue', ascending=False)

    country_comparison['Total_Revenue_M'] = country_comparison['Total_Revenue'] / 1e6
    country_comparison['Comedy_Revenue_M'] = country_comparison['Comedy_Revenue'] / 1e6
    
    return country_comparison

def get_comedies_mask(cmu_cleaned_movies): # cmu_comedies
    # Returns the (boolean) comedy mask for the given df
    # The `df` has to be of similar format as `prepro_cmu_movies(CMU_MOVIES_DS.df)`
    return cmu_cleaned_movies["genres"].apply(lambda genre_list: "Comedy" in genre_list or "comedy" in genre_list)

def explode_and_filter_comedy_genres(cmu_comedies): # comedy_genres
    movies_exploded_genres = cmu_comedies.explode('genres')
    comedy_genres = movies_exploded_genres[movies_exploded_genres['genres'].str.contains('Comedy', na=False)]
    return comedy_genres

def count_comedy_genres_by_release_and_genre(comedy_genres):
    comedy_genres_count = comedy_genres.groupby(['release_date', 'genres']).size().reset_index(name='count')
    return comedy_genres_count

def assign_decade_to_genres(comedy_genres_count):
    comedy_genres_count['decade'] = (comedy_genres_count['release_date'] // 10) * 10
    return comedy_genres_count

def count_genres_by_decade(comedy_genres_count):
    decade_genre_counts = comedy_genres_count.groupby(['decade', 'genres'])['count'].sum().reset_index()
    return decade_genre_counts

def pivot_genre_data_by_decade(decade_genre_counts):
    decade_genre_pivot = decade_genre_counts.pivot(index='decade', columns='genres', values='count').fillna(0)
    if 'Comedy' in decade_genre_pivot.columns:
        decade_genre_pivot = decade_genre_pivot.drop(columns='Comedy')
    return decade_genre_pivot

def calculate_genre_proportions(decade_genre_pivot): # decade_proportion
    decade_proportion = decade_genre_pivot.div(decade_genre_pivot.sum(axis=1), axis=0)
    return decade_proportion

# ============ ============ ============ ============ ============ ============
# Functions used to preprocess ..
# ============ ============ ============ ============ ============ ============

# ============ ============ ============ ============ ============ ============
# Functions used to preprocess ..
# ============ ============ ============ ============ ============ ============


# ============ ============ ============ ============ ============ ============
# Mergers
# ============ ============ ============ ============ ============ ============

def merge_ccmu_rosc(cleaned_cmu,renamed_oscars): # movie_awards
    movies_awards = cleaned_cmu.merge(renamed_oscars, on=['title']).drop(columns=['release_date_x'])
    return movies_awards.rename(columns={'release_date_y':'release_date'})



# ============ ============ ============ ============ ============ ============
# ExtraDatasetInfo (parsing the processed data)
# ============ ============ ============ ============ ============ ============

PROCESSED_DATA_DIR = "data/processed/"

class ExtraDatasetInfo:
    # This class will hold any additional information we infer from our base datasets
    # Some of this took time (and resources) to compute, which is why we have cached it in the `data/processed` directory.
    # If you wish to re-compute everything from scratch, set `preload` to false (NOT RECOMMENDED!) 
    def __init__(self, mrt_movies_ds: ProjectDataset,preload=True):
        all_valid(mrt_movies_ds)

        if preload:
            # The comedy ids in the massive rottent tomatoes dataset \inter CMU, where experts have given their opinions  
            mrtexp_fpath = Path(PROCESSED_DATA_DIR+"ratings_expert.csv") 
            assert mrtexp_fpath.exists() and mrtexp_fpath.is_file()
            self.mrt_cmu_expertrevd_comedy_ids = pd.read_csv(mrtexp_fpath.absolute().as_posix())["id"]
        
            # The massive RT dataset, extended with a sentiment analysis score for the entries with a review (~1.3M out of the 1.4M reviews):
            mrtsa_fpath = Path(PROCESSED_DATA_DIR+"reviews_with_compound.csv") 
            assert mrtsa_fpath.exists() and mrtsa_fpath.is_file()
            self.mrtrev_sa_df = pd.read_csv(mrtsa_fpath.absolute().as_posix())
        else:
            raise ValueError("See ./data/preprocessed/README.md for an indication on how to recreate the preloaded data")


