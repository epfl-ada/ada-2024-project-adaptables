import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ..utils.constants import NOTEBOOK_RUNCONFIG as cfg
from ..utils.constants import COLOR_PALETTE
from ..utils.data_utils import *
import matplotlib.pyplot as plt

if cfg.USE_MATPLOTLIB:
    def plot_genre_proportions(decade_proportion_df, color_palette):
        f = plt.figure(figsize=(15, 8))

        decade_proportion_df.plot(
            kind='bar',
            stacked=True,
            color=color_palette[:len(decade_proportion_df.columns)], 
            alpha=0.9,
            width=0.8
        )

        plt.title("Proportion of Comedy Sub-genres by Decade (Excluding Simply Comedy)", fontsize=16)
        plt.xlabel("Decade", fontsize=12)
        plt.ylabel("Proportion", fontsize=12)
        plt.legend(title="Comedy Sub-genres", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        return f
else:
    def plot_genre_proportions(decade_proportion_df, color_palette):
        """
        Creates an interactive stacked bar chart showing comedy sub-genre proportions by decade using Plotly.
        
        Args:
            decade_proportion (DataFrame): DataFrame with decades as index and genres as columns.
            color_palette (list): List of colors for the different genres.
            
        Returns:
            plotly.graph_objects.Figure: The interactive Plotly figure
        """
        fig = go.Figure()
        
        # Add traces for each genre
        for idx, genre in enumerate(decade_proportion_df.columns):
            fig.add_trace(go.Bar(
                name=genre,
                x=decade_proportion_df.index,
                y=decade_proportion_df[genre],
                marker_color=color_palette[idx] if idx < len(color_palette) else None,
                hovertemplate="%{y:.1%}<extra>" + genre + "</extra>"
            ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': "Proportion of Comedy Sub-genres by Decade (Excluding Simply Comedy)",
                'font': {'size': 16}
            },
            xaxis_title={
                'text': "Decade",
                'font': {'size': 12}
            },
            yaxis_title={
                'text': "Proportion",
                'font': {'size': 12}
            },
            barmode='stack',
            showlegend=True,
            legend={
                'title': "Comedy Sub-genres",
                'yanchor': "top",
                'y': 1,
                'xanchor': "left",
                'x': 1.05
            },
            height=600,
            width=1000,
            yaxis={
                'gridcolor': 'rgba(128, 128, 128, 0.2)',
                'gridwidth': 1,
                'griddash': 'dash',
                'tickformat': ',.0%'  # Format y-axis as percentages
            },
            # Add a range slider for better decade navigation
            xaxis={
                'rangeslider': {'visible': True},
                'type': 'category'  # Ensure decades are treated as categories
            },
            hovermode='x unified'  # Show all genres for a decade when hovering
        )
        
        return fig
    
def cmu_get_genres_split(cmu_df):
    cmu_cleaned_movies = prepro_cmu_movies(cmu_df)
    cmu_comedies = cmu_cleaned_movies[get_comedies_mask(cmu_cleaned_movies)]
    comedy_genres = explode_and_filter_comedy_genres(cmu_comedies)
    comedy_genres_count = count_comedy_genres_by_release_and_genre(comedy_genres)
    comedy_genres_count = assign_decade_to_genres(comedy_genres_count)
    decade_genre_counts = count_genres_by_decade(comedy_genres_count)
    decade_genre_pivot = pivot_genre_data_by_decade(decade_genre_counts)
    decade_proportion = calculate_genre_proportions(decade_genre_pivot)
    return plot_genre_proportions(decade_proportion, COLOR_PALETTE)