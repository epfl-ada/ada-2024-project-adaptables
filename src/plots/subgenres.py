import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ..utils.constants import NOTEBOOK_RUNCONFIG as cfg
from ..utils.constants import COLOR_PALETTE
from ..utils.data_utils import *
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba, to_hex


if cfg.USE_MATPLOTLIB:
    def plot_genres_by_country(genre_by_country_filtered, top_countries, all_genres, revenue_by_country, color_palette):
        """
        Plots pie charts of the top comedy subgenres for each country.
        """
        base_colors = [to_rgba(color) for color in color_palette]
        
        while len(base_colors) < len(all_genres):
            new_colors = []
            for color in base_colors[:10]: 
                new_color = (
                    min(1.0, color[0] * 0.8),
                    min(1.0, color[1] * 0.8),
                    min(1.0, color[2] * 0.8),
                    color[3]
                )
                new_colors.append(new_color)
            base_colors.extend(new_colors)
        
        extended_palette = [to_hex(color) for color in base_colors[:len(all_genres)]]
        color_mapping = dict(zip(all_genres, extended_palette))
        
        f = plt.figure(figsize=(20, 10))
        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        
        for i, country in enumerate(top_countries):
            country_data = genre_by_country_filtered[
                genre_by_country_filtered['countries'] == country
            ].copy()

            country_data = country_data.sort_values('Count', ascending=False)
            colors = [color_mapping[genre] for genre in country_data['genres']]
            
            plt.subplot(2, 4, i+1)
            plt.pie(country_data['Count'],
                labels=country_data['genres'],
                colors=colors,
                autopct='%1.1f%%')
            
            revenue = revenue_by_country[country] / 1e6 
            plt.title(f"{country}\nRevenue: ${revenue:.1f}M\nTotal Movies: {country_data['Count'].sum()}")
            plt.axis('equal')
        
        plt.suptitle('Top 10 Comedy Subgenres Distribution by Country (Ranked by Box Office Revenue)', 
                    fontsize=16, fontweight='bold', y=1.02)
        return f
else:
    def plot_genres_by_country(genre_by_country_filtered, top_countries, all_genres, revenue_by_country, color_palette):
        """
        Creates an interactive visualization of pie charts showing top comedy subgenres for each country.
        
        Args:
            genre_by_country_filtered (DataFrame): DataFrame with genre data by country
            top_countries (list): List of countries to display
            color_palette (list): Base color palette
            all_genres (list): List of all genres
            revenue_by_country (dict): Dictionary of revenue by country
        
        Returns:
            plotly.graph_objects.Figure: The interactive Plotly figure
        """
        # Extend color palette if needed
        base_colors = [to_rgba(color) for color in color_palette]
        
        while len(base_colors) < len(all_genres):
            new_colors = []
            for color in base_colors[:10]: 
                new_color = (
                    min(1.0, color[0] * 0.8),
                    min(1.0, color[1] * 0.8),
                    min(1.0, color[2] * 0.8),
                    color[3]
                )
                new_colors.append(new_color)
            base_colors.extend(new_colors)
        
        extended_palette = [to_hex(color) for color in base_colors[:len(all_genres)]]
        color_mapping = dict(zip(all_genres, extended_palette))
    
        
        # Create subplot layout
        rows = (len(top_countries) + 3) // 4  # Calculate rows needed (ceiling division)
        cols = min(4, len(top_countries))  # Use 4 columns or less
        
        # Create subplot titles with both country and revenue
        subplot_titles = []
        for country in top_countries:
            total_movies = genre_by_country_filtered[
                genre_by_country_filtered['countries'] == country
            ]['Count'].sum()
            subplot_titles.append(
                f"{country}<br>Revenue: ${revenue_by_country[country]/1e6:.1f}M<br>Total Movies: {total_movies}"
            )
        
        fig = make_subplots(
            rows=rows, 
            cols=cols,
            specs=[[{'type': 'pie'} for _ in range(cols)] for _ in range(rows)],
            subplot_titles=subplot_titles,
            vertical_spacing=0.1  # Increase spacing between rows
        )
        
        # Add pie charts for each country
        for i, country in enumerate(top_countries):
            row = (i // cols) + 1
            col = (i % cols) + 1
            
            country_data = genre_by_country_filtered[
                genre_by_country_filtered['countries'] == country
            ].sort_values('Count', ascending=False)
            
            colors = [color_mapping[genre] for genre in country_data['genres']]
            
            fig.add_trace(
                go.Pie(
                    values=country_data['Count'],
                    labels=country_data['genres'],
                    marker_colors=colors,
                    textposition='inside',
                    textinfo='percent',
                    hovertemplate="<b>%{label}</b><br>" +
                                "Count: %{value}<br>" +
                                "Percentage: %{percent}<br>" +
                                "<extra></extra>",
                    showlegend=(i == 0)  # Show legend only for first pie
                ),
                row=row, 
                col=col
            )
        
        # Update layout with more space at the top and increased height
        fig.update_layout(
            title={
                'text': 'Top 10 Comedy Subgenres Distribution by Country<br>(Ranked by Box Office Revenue)',
                'y': 0.98,  # Move title higher
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 16, 'weight': 'bold'}
            },
            showlegend=True,
            height=900,  # Increased height
            width=1200,
            legend={
                'title': 'Genres',
                'orientation': 'h',
                'y': -0.1,
                'x': 0.5,
                'xanchor': 'center'
            },
            margin=dict(t=100)  # Add more top margin
        )
        
        return fig

def cmu_subgenre_get_multi_pies(cmu_df):
    cmu_cleaned_movies = prepro_cmu_movies(cmu_df)
    cmu_comedy_movies = filter_comedy_movies(cmu_cleaned_movies)
    genre_by_country_filtered, top_countries, all_genres, revenue_by_country = process_genre_by_country(cmu_comedy_movies)
    return plot_genres_by_country(genre_by_country_filtered, top_countries, all_genres, revenue_by_country, COLOR_PALETTE)
