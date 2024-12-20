import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ..utils.constants import NOTEBOOK_RUNCONFIG as cfg
from ..utils.constants import COLOR_PALETTE
from ..utils.data_utils import *
import matplotlib.pyplot as plt
import numpy as np

if cfg.USE_MATPLOTLIB:
    def plot_monthly_revenues(all_movies_revenues, comedy_movies_revenues, color_all_movies, color_comedy_movies):
        """
        Plots a bar chart comparing monthly revenues for all movies and comedy movies.

        Parameters:
            all_movies_revenues (list): Revenues for all movies.
            comedy_movies_revenues (list): Revenues for comedy movies.
            color_all_movies (str): Color for all movies bar.
            color_comedy_movies (str): Color for comedy movies bar.
        """
        months = ["January", "February", "March", "April", "May", "June", "July", "August",
                "September", "October", "November", "December"]
        bar_width = 0.35
        x = np.arange(len(months))
        f = plt.figure(figsize=(12, 6))
        plt.bar(x - bar_width / 2, all_movies_revenues, bar_width, label='All Movies', color=color_all_movies)
        plt.bar(x + bar_width / 2, comedy_movies_revenues, bar_width, label='Comedy Movies', color=color_comedy_movies)
        plt.xlabel('Months')
        plt.ylabel('Average Revenue ($)')
        plt.title('Monthly Average Revenue: All Movies vs Comedy Movies')
        plt.xticks(x, months, rotation=45)
        plt.legend()
        plt.tight_layout()
        return f
    
    def plot_dual_trends(x1, y1, label1, color1, x2, y2, label2, color2, title, xlabel, ylabel):
        """
        Plots two trends on the same graph.
        
        Args:
            x1, y1 (Series): Data for the first trend (x and y values).
            label1 (str): Label for the first trend.
            color1 (str): Color for the first trend.
            x2, y2 (Series): Data for the second trend (x and y values).
            label2 (str): Label for the second trend.
            color2 (str): Color for the second trend.
            title (str): Title for the plot.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
        """
        f = plt.figure(figsize=(12, 6))

        plt.plot(x1, y1, marker='o', color=color1, linestyle='-', label=label1)
        
        plt.plot(x2, y2, marker='o', color=color2, linestyle='-', label=label2)

        plt.title(title, fontsize=16)
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        plt.legend(loc='upper left', fontsize=12)
        plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.7)
        plt.xlim(min(x1.min(), x2.min()), max(x1.max(), x2.max()))

        return f
else:
    def plot_monthly_revenues(all_movies_revenues, comedy_movies_revenues, color_all_movies, color_comedy_movies):
        """
        Creates an interactive bar chart comparing monthly revenues for all movies and comedy movies using Plotly.
        
        Parameters:
            all_movies_revenues (list): Revenues for all movies.
            comedy_movies_revenues (list): Revenues for comedy movies.
            color_all_movies (str): Color for all movies bar.
            color_comedy_movies (str): Color for comedy movies bar.
            
        Returns:
            plotly.graph_objects.Figure: The interactive Plotly figure
        """
        months = ["January", "February", "March", "April", "May", "June", "July", 
                "August", "September", "October", "November", "December"]
        
        fig = go.Figure()
        
        # Add bars for all movies
        fig.add_trace(go.Bar(
            name='All Movies',
            x=months,
            y=all_movies_revenues,
            marker_color=color_all_movies,
            hovertemplate="Month: %{x}<br>" +
                        "Revenue: $%{y:,.2f}<br>" +
                        "<extra></extra>",
            offsetgroup=0  # For bar positioning
        ))
        
        # Add bars for comedy movies
        fig.add_trace(go.Bar(
            name='Comedy Movies',
            x=months,
            y=comedy_movies_revenues,
            marker_color=color_comedy_movies,
            hovertemplate="Month: %{x}<br>" +
                        "Revenue: $%{y:,.2f}<br>" +
                        "<extra></extra>",
            offsetgroup=1  # For bar positioning
        ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Monthly Average Revenue: All Movies vs Comedy Movies',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Months',
            yaxis_title='Average Revenue ($)',
            barmode='group',  # Group bars side by side
            xaxis={
                'tickangle': -45,  # Rotate labels
                # Add range slider
                'rangeslider': {'visible': True},
            },
            yaxis={
                'tickformat': '$,.0f',  # Format y-axis as currency
            },
            # Add hover mode for better interaction
            hovermode='x unified',
            # Set figure size
            height=600,
            width=1000,
            # Add legend
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )
        
        return fig
    
    def plot_dual_trends(x1, y1, label1, color1, x2, y2, label2, color2, title, xlabel, ylabel):
        """
        Creates an interactive dual trend line plot using Plotly.
        
        Args:
            x1, y1 (Series): Data for the first trend (x and y values).
            label1 (str): Label for the first trend.
            color1 (str): Color for the first trend.
            x2, y2 (Series): Data for the second trend (x and y values).
            label2 (str): Label for the second trend.
            color2 (str): Color for the second trend.
            title (str): Title for the plot.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            
        Returns:
            plotly.graph_objects.Figure: The interactive Plotly figure
        """
        fig = go.Figure()
        
        # Add first trend line
        fig.add_trace(go.Scatter(
            x=x1,
            y=y1,
            name=label1,
            mode='lines+markers',
            line=dict(color=color1),
            marker=dict(
                size=8,
                color=color1,
                symbol='circle'
            ),
            hovertemplate=f"{label1}<br>" +
                        f"{xlabel}: %{{x}}<br>" +
                        f"{ylabel}: %{{y:.2f}}<br>" +
                        "<extra></extra>"
        ))
        
        # Add second trend line
        fig.add_trace(go.Scatter(
            x=x2,
            y=y2,
            name=label2,
            mode='lines+markers',
            line=dict(color=color2),
            marker=dict(
                size=8,
                color=color2,
                symbol='circle'
            ),
            hovertemplate=f"{label2}<br>" +
                        f"{xlabel}: %{{x}}<br>" +
                        f"{ylabel}: %{{y:.2f}}<br>" +
                        "<extra></extra>"
        ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': title,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 16}
            },
            xaxis_title={
                'text': xlabel,
                'font': {'size': 14}
            },
            yaxis_title={
                'text': ylabel,
                'font': {'size': 14}
            },
            # Set axis ranges
            xaxis={
                'range': [min(x1.min(), x2.min()), max(x1.max(), x2.max())],
                # Add range slider
                'rangeslider': {'visible': True}
            },
            # Add grid
            xaxis_showgrid=True,
            yaxis_showgrid=True,
            xaxis_gridwidth=0.5,
            yaxis_gridwidth=0.5,
            xaxis_gridcolor='rgba(128, 128, 128, 0.2)',
            yaxis_gridcolor='rgba(128, 128, 128, 0.2)',
            # Set figure size
            height=600,
            width=1000,
            # Add legend
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                font=dict(size=12)
            ),
            # Set hover mode
            hovermode='x unified'
        )
        
        return fig
    
    


def cmu_monthly_get_rev(cmu_movies_df):
    release_month_movies = clean_movie_data(cmu_movies_df)
    all_movies_stats = calculate_monthly_stats(release_month_movies)
    comedy_stats = calculate_monthly_stats(release_month_movies, comedy_only=True)
    return plot_monthly_revenues(all_movies_stats['box_office_revenue'].tolist(), comedy_stats['box_office_revenue'].tolist(), COLOR_PALETTE[0], COLOR_PALETTE[1])


def cmu_yearly_get_dual_trends(cmu_movies_df):
    cmu_cleaned_movies = prepro_cmu_movies(cmu_movies_df)
    cmu_comedies = cmu_cleaned_movies[get_comedies_mask(cmu_cleaned_movies)]

    revenues_per_year = calculate_revenues_per_year(cmu_cleaned_movies, cmu_comedies)
    movies_per_year = get_movies_per_year(cmu_cleaned_movies,cmu_comedies)

    return plot_dual_trends(
        x1=movies_per_year['release_date'], 
        y1=movies_per_year['comedy_proportion'], 
        label1='Proportion of comedy movies released', 
        color1=COLOR_PALETTE[1], 
        x2=revenues_per_year['release_date'], 
        y2=revenues_per_year['comedy_revenue'], 
        label2='Proportion of comedy revenues', 
        color2=COLOR_PALETTE[2], 
        title='Proportion of comedy movies and revenues each year (worldwide)',
        xlabel='Year', 
        ylabel='Proportion'
    )