# Due to lack of time, this file contains severa functions which were not modularized in the same way

import pandas as pd
from itertools import combinations
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import spacy
from collections import Counter
from sklearn.manifold import TSNE
from IPython.display import clear_output
import re

### ========================================================================================================================================

### TEAM COMPOSITION ANALYSIS
### ========================================================================================================================================

def filter_comedy_movies(df):
    # Filter for comedy genre
    df_comedy = df[df['genre'].str.contains('comedy', case=False, na=False)]
    
    df_comedy = df_comedy[df_comedy['title'].notna() & (df_comedy['title'].str.strip() != "")]

    return df_comedy


def merge_movie_and_character_datasets(movies_df, characters_df):
    movies_filtered = movies_df[["wikipedia_id", "title", "box_office_revenue", "genres"]]
    characters_filtered = characters_df[["wikipedia_id", "actor_name"]]
    merged_df = pd.merge(characters_filtered, movies_filtered, on="wikipedia_id")
    merged_df = merged_df[merged_df["box_office_revenue"].notnull()]
    merged_df["box_office_revenue"] = merged_df["box_office_revenue"].astype(float)
    comedies_merged_df = merged_df[merged_df["genres"].str.contains("Comedy", case=False, na=False)]
    return comedies_merged_df



def process_and_merge_datasets(df1, df2):
    cmu_characters_df = df1 #CMU_CHARACTER_DS.df
    cmu_movies_df = df2 #CMU_MOVIES_DS.df

    cmu_characters_df["wikipedia_id"] = cmu_characters_df["wikipedia_id"].astype(str)
    cmu_movies_df["wikipedia_id"] = cmu_movies_df["wikipedia_id"].astype(str)
    cmu_characters_df = cmu_characters_df[cmu_characters_df["actor_name"].apply(lambda x: isinstance(x, str) and x.strip() != "")]

    merged_df = merge_movie_and_character_datasets(cmu_movies_df, cmu_characters_df)

    merge_df_final = merged_df.copy()
    merge_df_final = merge_df_final.drop(columns=merge_df_final.columns[-1])
    merge_df_final = merge_df_final.drop_duplicates(subset=["wikipedia_id", "actor_name"])

    return merge_df_final



def analyze_actor_associations(df, aggregation="mean"):
    """
    Analyze actor associations to find the most successful ones.

    """
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()

    # Group by movie to get actors, revenue, and title
    grouped = df_copy.groupby("wikipedia_id").agg({
        "actor_name": lambda x: list(x),
        "box_office_revenue": "first",
        "title": "first"
    }).reset_index()

    # Generate actor pairs for each movie
    actor_pairs = []
    for _, row in grouped.iterrows():
        actors = row["actor_name"]
        revenue = row["box_office_revenue"]
        title = row["title"]
        if len(actors) > 1:
            pairs = list(combinations(sorted(actors), 2))
            actor_pairs.extend([(pair[0], pair[1], revenue, title) for pair in pairs])

    # Create a DataFrame of pairs
    pairs_df = pd.DataFrame(actor_pairs, columns=["Actor1", "Actor2", "BoxOfficeRevenue", "Title"])

    # Aggregate revenue, movies, and count collaborations by actor pairs
    pair_revenue = pairs_df.groupby(["Actor1", "Actor2"]).agg({
        "BoxOfficeRevenue": aggregation,
        "Title": lambda x: list(set(x)),  # List of unique movies
    }).reset_index()

    # Add collaboration count
    pair_revenue["CollaborationCount"] = pair_revenue["Title"].apply(len)

    # Rename columns and sort results
    pair_revenue = pair_revenue.rename(columns={"BoxOfficeRevenue": f"BoxOfficeRevenue_{aggregation}", "Title": "Movies"})
    pair_revenue = pair_revenue.sort_values(by=f"BoxOfficeRevenue_{aggregation}", ascending=False)

    return pair_revenue



def compute_actor_pair_revenue_with_titles(df):
    """
    Calculates the average box office revenue for actor pairs who collaborated in at least two movies,
    lists the movie titles, and ranks by the number of collaborations.
    """
    # Step 1: Group by title and create actor pairs
    actor_pairs = []
    for title, group in df.groupby("title"):
        actors = group["actor_name"].tolist()
        revenue = group["box_office_revenue"].iloc[0]
        for pair in combinations(sorted(actors), 2):
            actor_pairs.append({"Actor1": pair[0], "Actor2": pair[1], "Revenue": revenue, "Title": title})

    # Convert pairs into a DataFrame
    pairs_df = pd.DataFrame(actor_pairs)

    # Step 2: Group by pairs and calculate statistics
    grouped = pairs_df.groupby(["Actor1", "Actor2"], as_index=False).agg(
        CollaborationCount=("Title", "count"),
        AverageRevenue=("Revenue", "mean"),
        Titles=("Title", lambda x: list(x))  # List movie titles
    )

    # Step 3: Filter pairs with at least two collaborations
    filtered = grouped[grouped["CollaborationCount"] > 1]

    # Step 4: Sort by CollaborationCount (descending) and then by AverageRevenue (descending)
    sorted_df = filtered.sort_values(by=["CollaborationCount", "AverageRevenue"], ascending=[False, False])

    return sorted_df



def plot_actor_pair_revenue_tight(df, top_n=20):
    """
    Creates an interactive bar chart showing the average revenue for actor pairs with their names below the bars.
    Bars are tightly grouped and spaced.

    """
    # Limit to top N for readability
    top_pairs = df.head(top_n)

    # Create a combined column for actor pairs
    top_pairs["ActorPair"] = top_pairs["Actor1"] + " & " + top_pairs["Actor2"]

    # Create the plot using Plotly Graph Objects
    fig = go.Figure()

    # Add a bar for each pair
    for _, row in top_pairs.iterrows():
        fig.add_trace(go.Bar(
            x=[row["ActorPair"]],  # Show the pair as a category
            y=[row["AverageRevenue"]],
            text=f"{row['CollaborationCount']} collaborations",  # Text displayed above the bar
            textposition="outside",  # Position text above the bars
            hovertemplate=(
                f"<b>Actor Pair</b>: {row['ActorPair']}<br>"
                f"<b>Number of Collaborations</b>: {row['CollaborationCount']}<br>"
                f"<b>Average Revenue</b>: ${row['AverageRevenue']:.2f}<extra></extra>"
            ),
            name=row["ActorPair"]
        ))

    # Adjust labels and axes
    fig.update_layout(
        title="Average Revenue for Actor Pairs",
        xaxis=dict(
            title="Actor Pairs",
            tickmode="array",
            tickvals=top_pairs["ActorPair"],
            ticktext=top_pairs["ActorPair"],
            tickangle=-45  # Tilt labels to prevent overlap
        ),
        yaxis=dict(
            title="Average Revenue ($)"
        ),
        barmode="group",  # Group bars together
        template="plotly_white",
        showlegend=False,  # Hide the legend since names are on the bars
        height=700  # Increase the height of the chart
    )

    # Display the plot
    fig.show()



def plot_collaboration_vs_revenue_with_logscale(df):
    """
    Creates a scatter plot with a logarithmic scale for the number of collaborations
    and a jitter for low collaboration counts to improve visualization.

    Args:
        df (pd.DataFrame): DataFrame containing 'CollaborationCount' and 'AverageRevenue'.

    Returns:
        None: Displays the Plotly chart.
    """
    # Add jitter for low collaboration counts
    df["CollaborationCountJittered"] = df["CollaborationCount"] + np.random.uniform(-0.3, 0.3, size=len(df))

    # Create scatter plot
    fig = px.scatter(
        df,
        x="CollaborationCountJittered",  # Use jittered values for the x-axis
        y="AverageRevenue",
        size="CollaborationCount",  # Bubble size depends on the number of collaborations
        color="AverageRevenue",  # Color represents the revenue
        hover_data={  # Customize hover data
            "Actor1": True,
            "Actor2": True,
            "CollaborationCount": True,  # Show the original integer collaboration count
            "AverageRevenue": ":.2f",
            "CollaborationCountJittered": False  # Hide the jittered values in the hover
        },
        labels={
            "CollaborationCountJittered": "Number of Collaborations (Log Scale)",
            "AverageRevenue": "Average Box Office Revenue ($)"
        },
        title="Relationship Between Number of Collaborations and Average Box Office Revenue (Log Scale)"
    )

    # Customize the layout
    fig.update_traces(
        marker=dict(opacity=0.7, line=dict(width=1, color="DarkSlateGrey"))  # Marker styling
    )
    fig.update_layout(
        template="plotly_white",
        xaxis=dict(
            title="Number of Collaborations (Log Scale)",
            type="log",  # Apply logarithmic scale
            tickvals=[1, 2, 5, 10, 20, 50, 100],  # Custom ticks for better readability
        ),
        yaxis=dict(title="Average Box Office Revenue ($)"),
        height=600,  # Adjust the chart height
    )

    # Show the chart
    fig.show()





def data_for_best_2_collaboration(df1, df2):
    merge_df_final = process_and_merge_datasets(df1, df2)
    actor_revenue_stats_with_titles = compute_actor_pair_revenue_with_titles(merge_df_final)
    collaboration_df= actor_revenue_stats_with_titles[actor_revenue_stats_with_titles['CollaborationCount'] == 2]
    return collaboration_df




### ========================================================================================================================================


### TITLE COMPOSITION ANALYSIS

### ========================================================================================================================================




def process_titles_and_visualize(df):
    # Load an NLP model to obtain word embeddings

    df = filter_comedy_movies(df)
    nlp = spacy.load("en_core_web_sm")

    # Clean titles: remove punctuation, stopwords, and tokenize
    def preprocess_title(title):
        if not isinstance(title, str):  # Handle non-string values
            return []
        title = title.lower()  # Convert to lowercase
        doc = nlp(title)  # Process the title with spaCy
        tokens = [
            token.lemma_ for token in doc
            if not token.is_stop and not token.is_punct and token.is_alpha
        ]
        return tokens

    # Apply preprocessing
    df["cleaned_title"] = df["title"].fillna("").apply(preprocess_title)

    # Count words
    all_words = [word for tokens in df["cleaned_title"] for word in tokens]
    word_counts = Counter(all_words)

    # Filter words that appear at least 5 times
    filtered_words = {word: count for word, count in word_counts.items() if count >= 5}

    # Transform filtered words into vectors using Word2Vec (via spaCy)
    unique_words = list(filtered_words.keys())
    word_vectors = [nlp(word).vector for word in unique_words]

    # Convert word_vectors to a NumPy array
    word_vectors = np.array(word_vectors)

    # Dimensionality reduction using t-SNE
    tsne = TSNE(n_components=2, random_state=42, perplexity=50)  # Adjusted perplexity
    word_embeddings_2d = tsne.fit_transform(word_vectors)

    # Stretch y-axis
    word_embeddings_2d[:, 1] *= 2  # Stretch y-axis values

    # Create a DataFrame with the results
    embedding_df = pd.DataFrame({
        "word": unique_words,
        "x": word_embeddings_2d[:, 0],
        "y": word_embeddings_2d[:, 1],
        "frequency": [filtered_words[word] for word in unique_words]
    })

    # Interactive visualization with Plotly
    fig = px.scatter(
    embedding_df,
    x="x",
    y="y",
    size="frequency",
    hover_name="word",
    title="Word Map of Movie Titles",
    template="plotly",
    size_max=40
)
    fig.update_traces(marker=dict(opacity=0.8))
    fig.update_layout(
        height=800,  # Ajustez cette valeur pour augmenter la hauteur
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        hovermode="closest"
    )
    fig.show()

### ========================================================================================================================================


### SEQUEL ANALYSIS 
### ========================================================================================================================================



def filter_comedy_movies_sequels(df):
    """
    Filters comedy movies and their sequels based on specific conditions.
    
    Parameters:
        movie_df (pd.DataFrame): Input DataFrame with movie data.
        
    Returns:
        pd.DataFrame: Filtered DataFrame.
        set: Set of retained base IDs.
    """
    # Filter for comedy genre
    df_comedy = filter_comedy_movies(df)

    df_titles_ratings = df_comedy[['id', 'title', 'audienceScore', 'releaseDateStreaming']].copy()
    df_titles_ratings_sorted = (
        df_titles_ratings
        .sort_values(by='id', ascending=True)
        .reset_index(drop=True)
        .dropna(subset=['audienceScore'])
    )


    # Filter IDs ending with "_10" or "_[2-9]"
    df_ids_between_1_and_10 = df_titles_ratings_sorted[
        df_titles_ratings_sorted['id'].str.contains(r'_(10|[2-9])$', na=False)
    ]

    df_result = df_ids_between_1_and_10.copy()
    set_base = set()

    for full_id in df_ids_between_1_and_10['id']:
        if full_id.endswith("_2"):
            base_id_match = re.match(r'^(.*)_\d+$', full_id)
            if base_id_match:
                base_id = base_id_match.group(1)
                if not df_titles_ratings_sorted['id'].str.contains(f'^{base_id}$', na=False).any():
                    df_result = df_result[~df_result['id'].str.startswith(f'{base_id}_')]
                else:
                    if base_id in df_titles_ratings_sorted['id'].values:
                        set_base.add(base_id)
                        matching_record = df_titles_ratings_sorted[df_titles_ratings_sorted['id'] == base_id]
                        df_result = pd.concat([df_result, matching_record])

    set_base.discard('no_manches_frida')
    df_result = df_result.sort_values(by='id').reset_index(drop=True)

    return df_result, set_base




def filter_dataframe(df, initial_bases):
    indices_to_drop = []

    for i in df.index:
        full_id = df.loc[i, 'id']
        last_char = full_id[-1]
        before_last_char = full_id[-2] if len(full_id) > 1 else ""

        if last_char.isdigit() and before_last_char == "_":
            number = int(last_char)
            base = full_id[:-2]

            if number == 2 and base not in initial_bases:
                indices_to_drop.append(i)
                continue

            if number > 2:
                if base not in initial_bases:
                    indices_to_drop.append(i)
                    continue

                expected_previous_id = f"{base}_{number - 1}"
                if i == 0 or df.loc[i - 1, 'id'] != expected_previous_id:
                    indices_to_drop.append(i)
        else:
            if full_id not in initial_bases:
                indices_to_drop.append(i)

    df.drop(index=indices_to_drop, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df



def extract_base_and_sequel(id_str):
    if len(id_str) > 2 and id_str[-1].isdigit() and id_str[-2] == "_":
        base_id = id_str[:-2]
        sequel_number = int(id_str[-1])
    else:
        base_id = id_str
        sequel_number = 1
    return pd.Series([base_id, sequel_number], index=["base_id", "sequel_number"])




def data_part_1(mrt_df):
    df_result, set_base = filter_comedy_movies_sequels(mrt_df)
    
    final_df = filter_dataframe(df_result, set_base)
    df_with_sequels = final_df.copy()
    df_with_sequels[["base_id", "sequel_number"]] = df_with_sequels["id"].apply(extract_base_and_sequel)



    set_titles = set(final_df[final_df['id'].isin(set_base)]['title'])
    
    return df_with_sequels, set_titles



def plot_movie_suites(selected_title):
    # Clear previous output to avoid multiple graphs
    clear_output(wait=True)
    
    # Retrieve the base ID corresponding to the selected title
    base_row = final_df[final_df['title'] == selected_title]
    if base_row.empty:
        print(f"Movie title '{selected_title}' not found in the dataset.")
        return
    
    base_id = base_row.iloc[0]['base_id']  # Retrieve the base_id
    
    # Filter sequels based on the same base_id
    filtered_df = final_df[final_df['base_id'] == base_id].copy()
    if filtered_df.empty:
        print(f"No sequels found for '{selected_title}' in the dataset.")
        return
    
    # Sort by sequel_number to ensure logical order
    filtered_df = filtered_df.sort_values(by="sequel_number")
    
    # Add a "year" column extracted from "releaseDateStreaming"
    filtered_df['year'] = pd.to_datetime(filtered_df['releaseDateStreaming'], errors='coerce').dt.year
    
    # Check if valid years exist
    valid_filtered_df = filtered_df.dropna(subset=['year'])
    
    # Create the graph
    fig = go.Figure()
    if valid_filtered_df.empty:
        print(f"No valid release dates for '{selected_title}', but audience scores will be shown.")
    
    # Use years if available, otherwise use titles only
    x_labels = (
        valid_filtered_df['title'] + " (" + valid_filtered_df['year'].astype(int).astype(str) + ")"
        if not valid_filtered_df.empty
        else filtered_df['title']
    )
    
    fig.add_trace(go.Scatter(
        x=x_labels,
        y=filtered_df['audienceScore'],  # Audience scores
        mode='lines+markers',
        name=selected_title,
        line=dict(color='royalblue', width=3),
        marker=dict(size=10, color='orange', line=dict(width=2, color='darkblue'))
    ))
    
    # Add annotations for each score
    for i, row in filtered_df.iterrows():
        label = (
            row['title'] + f" ({int(row['year'])})" if pd.notna(row['year']) else row['title']
        )
        fig.add_annotation(
            x=label,
            y=row['audienceScore'],
            text=str(int(row['audienceScore'])),
            showarrow=False,
            font=dict(size=12, color="black"),
            bgcolor="lightyellow",
            bordercolor="black"
        )
    
    # Add labels and style
    fig.update_layout(
        title=dict(
            text=f"<b>Audience Scores for '{selected_title}' and Its Sequels</b>",
            font=dict(size=18, color="darkblue"),
            x=0.5
        ),
        xaxis=dict(
            title="Movie Titles (Release Year if available)",
            titlefont=dict(size=14, color="darkblue"),
            tickangle=45,
            tickfont=dict(size=12, color="black")
        ),
        yaxis=dict(
            title="Audience Score",
            titlefont=dict(size=14, color="darkblue"),
            tickfont=dict(size=12, color="black"),
            gridcolor="lightgrey"
        ),
        plot_bgcolor="whitesmoke",
        template="plotly_white"
    )
    
    # Display the graph
    display(fig)




from ipywidgets import interact

def plot_movie_suites(mrt_df,selected_title):
    if not selected_title:  # Ne rien afficher si aucun titre n'est sélectionné
        print("Please select a movie title.")
        return
    
    # Reste du code existant pour afficher le graphique
    # Clear previous output to avoid multiple graphs
    clear_output(wait=True)
    final_df = data_part_1(mrt_df)
    base_row = final_df[final_df['title'] == selected_title]
    if base_row.empty:
        print(f"Movie title '{selected_title}' not found in the dataset.")
        return
    
    base_id = base_row.iloc[0]['base_id']
    filtered_df = final_df[final_df['base_id'] == base_id].copy()
    if filtered_df.empty:
        print(f"No sequels found for '{selected_title}' in the dataset.")
        return
    
    filtered_df = filtered_df.sort_values(by="sequel_number")
    filtered_df['year'] = pd.to_datetime(filtered_df['releaseDateStreaming'], errors='coerce').dt.year
    valid_filtered_df = filtered_df.dropna(subset=['year'])
    fig = go.Figure()
    x_labels = (
        valid_filtered_df['title'] + " (" + valid_filtered_df['year'].astype(int).astype(str) + ")"
        if not valid_filtered_df.empty
        else filtered_df['title']
    )
    fig.add_trace(go.Scatter(
        x=x_labels,
        y=filtered_df['audienceScore'],
        mode='lines+markers',
        name=selected_title,
        line=dict(color='royalblue', width=3),
        marker=dict(size=10, color='orange', line=dict(width=2, color='darkblue'))
    ))
    for i, row in filtered_df.iterrows():
        label = row['title'] + f" ({int(row['year'])})" if pd.notna(row['year']) else row['title']
        fig.add_annotation(
            x=label,
            y=row['audienceScore'],
            text=str(int(row['audienceScore'])),
            showarrow=False,
            font=dict(size=12, color="black"),
            bgcolor="lightyellow",
            bordercolor="black"
        )
    fig.update_layout(
        title=dict(
            text=f"<b>Audience Scores for '{selected_title}' and Its Sequels</b>",
            font=dict(size=18, color="darkblue"),
            x=0.5
        ),
        xaxis=dict(
            title="Movie Titles (Release Year if available)",
            titlefont=dict(size=14, color="darkblue"),
            tickangle=45,
            tickfont=dict(size=12, color="black")
        ),
        yaxis=dict(
            title="Audience Score",
            titlefont=dict(size=14, color="darkblue"),
            tickfont=dict(size=12, color="black"),
            gridcolor="lightgrey"
        ),
        plot_bgcolor="whitesmoke",
        template="plotly_white"
    )
    display(fig)



def plot_sequel_ratings(df):
    """
    Produces a scatter plot showing the relationship between sequel number and average audience score.
    The size of the points reflects the number of movies in each sequel.

    Args:
        df (pd.DataFrame): DataFrame containing the columns 'sequel_number' and 'audienceScore'.
    """
    import matplotlib.pyplot as plt

    # Create a copy of the DataFrame
    df = df.copy()

    # Check if the required columns are present
    required_columns = {"sequel_number", "audienceScore"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"The DataFrame must contain the following columns: {required_columns}")

    # Group by sequel_number to calculate averages and counts
    grouped = df.groupby("sequel_number").agg(
        avg_audienceScore=("audienceScore", "mean"),
        film_count=("audienceScore", "size")
    ).reset_index()

    # Create the scatter plot
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        grouped["sequel_number"],
        grouped["avg_audienceScore"],
        s=grouped["film_count"] * 50,  # Adjust the multiplier for point size
        alpha=0.7,
        color="blue"
    )

    # Add labels for the number of movies
    for i in range(len(grouped)):
        plt.text(
            grouped["sequel_number"][i],
            grouped["avg_audienceScore"][i] + 1,  # Offset for readability
            f'{grouped["film_count"][i]} films',
            ha="center"
        )

    # Adjust x-axis and y-axis limits to avoid clipping
    x_min = grouped["sequel_number"].min() - 0.5  # Add margin on the left
    x_max = grouped["sequel_number"].max() + 0.5  # Add margin on the right
    y_min = grouped["avg_audienceScore"].min() - 5  # Add margin below
    y_max = grouped["avg_audienceScore"].max() + 5  # Add margin above
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    # Set integer ticks on the x-axis
    plt.xticks(ticks=range(grouped["sequel_number"].min(), grouped["sequel_number"].max() + 1))

    # Additional plot configurations
    plt.title("Relationship Between Sequel Number and Average Audience Score", fontsize=14)
    plt.xlabel("Sequel Number", fontsize=12)
    plt.ylabel("Average Audience Score", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()
