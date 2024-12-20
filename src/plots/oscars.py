import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ..utils.constants import NOTEBOOK_RUNCONFIG as cfg
from ..utils.constants import COLOR_PALETTE
from ..utils.data_utils import *
import matplotlib.pyplot as plt

if cfg.USE_MATPLOTLIB:
    def plot_comedy_vs_total_awards(country_comparison_df, color_palette):
        """
        Plots a bar chart comparing total award-winning movies vs. winning comedies by country.
        
        Args:
            country_comparison_df (DataFrame): DataFrame with country comparison data (total awards and winning comedies).
            color_palette (list): List of colors for the bars.
        """
        fig, ax = plt.subplots(figsize=(15, 8))

        ax.bar(country_comparison_df['countries'], country_comparison_df['Winning_Movies_Total'], 
            label='Total Winning Movies', alpha=0.7, color=color_palette[1])
        ax.bar(country_comparison_df['countries'], country_comparison_df['Winning_Comedies'], 
            label='Winning Comedies', alpha=0.7, color=color_palette[0])
        ax.set_yscale('log')
        plt.xlabel('Countries')
        plt.ylabel('Number of Movies (Log Scale)')
        plt.title('Comparison of Award-Winning Comedies vs. Total Award-Winning Movies Per Country')
        plt.xticks(rotation=90)
        plt.legend()
        plt.tight_layout()
        return fig

    def plot_comedy_percentage(country_comparison_df, color_palette):
        """
        Plots a bar chart showing the percentage of award-winning comedies per country.
        
        Args:
            country_comparison_df (DataFrame): DataFrame with the 'Winning_Comedies_Percentage' column.
            color_palette (list): List of colors for plotting.
        """
        fig, ax = plt.subplots(figsize=(15, 8))

        ax.bar(country_comparison_df['countries'], country_comparison_df['Winning_Comedies_Percentage'], 
            label='Winning Comedies (%)', alpha=0.7, color=color_palette[0])

        ax.set_ylabel('Percentage of Winning Awards Comedies (%)')
        plt.xlabel('Countries')
        plt.title('Proportion of Award-Winning Comedies Over Award-Winning Total Movies per Country')
        plt.xticks(rotation=90)
        plt.legend()
        plt.tight_layout()
        return fig

    def plot_comedy_vs_total_revenue(country_comparison_df, color_palette):
        """
        Plots a bar chart comparing total box office revenue vs. comedy revenue by country.
        
        Args:
            country_comparison_df (DataFrame): DataFrame with country comparison data.
            color_palette (list): List of colors for the bars.
            top_n (int): Number of top countries to display.
        """
        plot_data = country_comparison_df
        
        fig, ax = plt.subplots(figsize=(15, 8))

        ax.bar(plot_data['countries'], 
            plot_data['Total_Revenue_M'],
            label='Total Box Office Revenue', 
            alpha=0.7, 
            color=color_palette[1])
        ax.bar(plot_data['countries'], 
            plot_data['Comedy_Revenue_M'],
            label='Comedy Box Office Revenue', 
            alpha=0.7, 
            color=color_palette[0])

        ax.set_yscale('log')
        plt.xlabel('Countries')
        plt.ylabel('Box Office Revenue (Millions USD, Log Scale)')
        plt.title('Comparison of Comedy vs. Total Box Office Revenue by Country')
        plt.xticks(rotation=90, ha='right')
        plt.legend()
        plt.grid(True, alpha=0.3, axis='y')
        return fig

    def plot_comedy_percentage_revenue(country_comparison_df, color_palette):
        """
        Plots a bar chart showing the percentage of award-winning comedies per country.
        
        Args:
            country_comparison_df (DataFrame): DataFrame with the 'Winning_Comedies_Percentage' column.
            color_palette (list): List of colors for plotting.
        """
        fig, ax = plt.subplots(figsize=(15, 8))

        ax.bar(country_comparison_df['countries'], country_comparison_df['Comedy_Percentage'], 
            label='Comedies Revenues (%)', alpha=0.7, color=color_palette[0])

        ax.set_ylabel('Percentage of Revenues of Comedies (%)')
        plt.xlabel('Countries')
        plt.title('Proportion of revenues from Comedy Movies per Country')
        plt.xticks(rotation=90)
        plt.legend()
        plt.tight_layout()
        plt.show()

else:
    def plot_comedy_vs_total_awards(country_comparison_df, color_palette):
        """
        Plots an interactive bar chart comparing total award-winning movies vs. winning comedies by country using Plotly.
        
        Args:
            country_comparison_df (DataFrame): DataFrame with country comparison data (total awards and winning comedies).
            color_palette (list): List of colors for the bars.
        """
        fig = go.Figure()
        
        # Add bars for total winning movies
        fig.add_trace(go.Bar(
            x=country_comparison_df['countries'],
            y=country_comparison_df['Winning_Movies_Total'],
            name='Total Winning Movies',
            marker_color=color_palette[1],
            opacity=0.7
        ))
        
        # Add bars for winning comedies
        fig.add_trace(go.Bar(
            x=country_comparison_df['countries'],
            y=country_comparison_df['Winning_Comedies'],
            name='Winning Comedies',
            marker_color=color_palette[0],
            opacity=0.7
        ))
        
        # Update layout
        fig.update_layout(
            title='Comparison of Award-Winning Comedies vs. Total Award-Winning Movies Per Country',
            xaxis_title='Countries',
            yaxis_title='Number of Movies (Log Scale)',
            yaxis_type='log',
            xaxis_tickangle=-90,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            ),
            barmode='overlay',
            height=600,
            width=1000,
            showlegend=True
        )
        
        return fig

    def plot_comedy_percentage(country_comparison_df, color_palette):
        """
        Plots an interactive bar chart showing the percentage of award-winning comedies per country using Plotly.
        
        Args:
            country_comparison_df (DataFrame): DataFrame with the 'Winning_Comedies_Percentage' column.
            color_palette (list): List of colors for plotting.
            
        Returns:
            plotly.graph_objects.Figure: The interactive Plotly figure
        """
        fig = go.Figure()
        
        # Add bars for comedy percentage
        fig.add_trace(go.Bar(
            x=country_comparison_df['countries'],
            y=country_comparison_df['Winning_Comedies_Percentage'],
            name='Winning Comedies (%)',
            marker_color=color_palette[0],
            opacity=0.7,
            hovertemplate='%{y:.1f}%<extra></extra>'  # Format hover text to show percentage with 1 decimal
        ))
        
        # Update layout
        fig.update_layout(
            title='Proportion of Award-Winning Comedies Over Award-Winning Total Movies per Country',
            xaxis_title='Countries',
            yaxis_title='Percentage of Winning Awards Comedies (%)',
            xaxis_tickangle=-90,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            ),
            height=600,
            width=1000,
            showlegend=True,
            # Add a range slider for better navigation with many countries
            xaxis=dict(rangeslider=dict(visible=True))
        )
        
        return fig

    def plot_comedy_vs_total_revenue(country_comparison_df, color_palette):
        """
        Plots an interactive bar chart comparing total box office revenue vs. comedy revenue by country using Plotly.
        
        Args:
            country_comparison_df (DataFrame): DataFrame with country comparison data.
            color_palette (list): List of colors for the bars.
            
        Returns:
            plotly.graph_objects.Figure: The interactive Plotly figure
        """
        fig = go.Figure()
        
        # Add bars for total revenue
        fig.add_trace(go.Bar(
            x=country_comparison_df['countries'],
            y=country_comparison_df['Total_Revenue_M'],
            name='Total Box Office Revenue',
            marker_color=color_palette[1],
            opacity=0.7,
            hovertemplate='$%{y:.1f}M<extra></extra>'
        ))
        
        # Add bars for comedy revenue
        fig.add_trace(go.Bar(
            x=country_comparison_df['countries'],
            y=country_comparison_df['Comedy_Revenue_M'],
            name='Comedy Box Office Revenue',
            marker_color=color_palette[0],
            opacity=0.7,
            hovertemplate='$%{y:.1f}M<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title='Comparison of Comedy vs. Total Box Office Revenue by Country',
            xaxis_title='Countries',
            yaxis_title='Box Office Revenue (Millions USD, Log Scale)',
            yaxis_type='log',
            xaxis_tickangle=-90,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            ),
            height=600,
            width=1000,
            showlegend=True,
            barmode='overlay',
            # Add grid for y-axis only
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(128, 128, 128, 0.3)',
            ),
            # Add a range slider for better navigation
            xaxis=dict(
                rangeslider=dict(visible=True),
                tickangle=-90,
            ),
        )
        
        return fig
    
    def plot_comedy_percentage_revenue(country_comparison_df, color_palette):
        """
        Plots an interactive bar chart showing the percentage of comedy revenue per country using Plotly.
        
        Args:
            country_comparison_df (DataFrame): DataFrame with the 'Comedy_Percentage' column.
            color_palette (list): List of colors for plotting.
            
        Returns:
            plotly.graph_objects.Figure: The interactive Plotly figure
        """
        fig = go.Figure()
        
        # Add bars for comedy percentage
        fig.add_trace(go.Bar(
            x=country_comparison_df['countries'],
            y=country_comparison_df['Comedy_Percentage'],
            name='Comedies Revenues (%)',
            marker_color=color_palette[0],
            opacity=0.7,
            hovertemplate='%{y:.1f}%<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title='Proportion of Revenues from Comedy Movies per Country',
            xaxis_title='Countries',
            yaxis_title='Percentage of Revenues of Comedies (%)',
            xaxis_tickangle=-90,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            ),
            height=600,
            width=1000,
            showlegend=True,
            # Add reference line for mean percentage
            shapes=[{
                'type': 'line',
                'yref': 'y',
                'y0': country_comparison_df['Comedy_Percentage'].mean(),
                'y1': country_comparison_df['Comedy_Percentage'].mean(),
                'x0': -0.5,
                'x1': len(country_comparison_df['countries']) - 0.5,
                'line': {
                    'color': 'red',
                    'dash': 'dash',
                    'width': 1
                }
            }],
            # Add a range slider for better navigation
            xaxis=dict(
                rangeslider=dict(visible=True),
            )
        )
        
        # Add annotation for mean line
        fig.add_annotation(
            x=len(country_comparison_df['countries']) - 1,
            y=country_comparison_df['Comedy_Percentage'].mean(),
            text=f'Mean: {country_comparison_df["Comedy_Percentage"].mean():.1f}%',
            showarrow=True,
            arrowhead=1,
            ax=50,
            ay=-20,
            font=dict(color='red')
        )
        
        return fig
    
def _get_ccd(cmu_df,oscars_df):
    renamed_oscars = rename_oscars_cols(oscars_df)
    cmu_cleaned = prepro_cmu_movies(cmu_df)
    movies_awards_df = merge_ccmu_rosc(cmu_cleaned,renamed_oscars)
    return prepare_award_comparison_data(movies_awards_df)

def osc_get_awrd_win_comp(cmu_df,oscars_df):
    return plot_comedy_vs_total_awards(_get_ccd(cmu_df,oscars_df), COLOR_PALETTE)

def osc_get_awrd_win_prop(cmu_df,oscars_df):
    country_comparison_df = _get_ccd(cmu_df,oscars_df)
    country_comparison_df['Winning_Comedies_Percentage'] = (
        country_comparison_df['Winning_Comedies'] / country_comparison_df['Winning_Movies_Total'] * 100
    )
    return plot_comedy_percentage(country_comparison_df,COLOR_PALETTE)

def osc_get_total_bo_per_country(cmu_df):
    cmu_cleaned = prepro_cmu_movies(cmu_df)
    country_comparison_df_revenue = prepare_revenue_comparison_data(cmu_cleaned)
    return plot_comedy_vs_total_revenue(country_comparison_df_revenue, COLOR_PALETTE)


def osc_get_prop_bo_per_country(cmu_df):
    cmu_cleaned = prepro_cmu_movies(cmu_df)
    country_comparison_df_revenue = prepare_revenue_comparison_data(cmu_cleaned)
    country_comparison_df_revenue['Comedy_Percentage'] = (
        country_comparison_df_revenue['Comedy_Revenue'] / country_comparison_df_revenue['Total_Revenue'] * 100
    )
    return plot_comedy_percentage_revenue(country_comparison_df_revenue, COLOR_PALETTE)