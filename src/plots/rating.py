import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ..utils.constants import NOTEBOOK_RUNCONFIG as cfg
from ..utils.constants import COLOR_PALETTE
from ..utils.data_utils import *
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import seaborn as sns
from scipy import stats

if cfg.USE_MATPLOTLIB:
    def plot_audience_score_tomatoe_meter(df):
        f = plt.figure(figsize=(8, 6))
        # Create a scatter plot with a regression line
        sns.lmplot(
            data=df, 
            x='audienceScore', 
            y='tomatoMeter', 
            height=6, 
            aspect=1.5, 
            line_kws={'color': 'red'}
        )

        # Add titles and labels in English
        plt.title("Relationship between Audience Score and Tomato Meter")
        plt.xlabel("Audience Score (%)")
        plt.ylabel("Critics' Score (Tomato Meter %)")
        return f
else:

    def plot_audience_score_tomatoe_meter(df):
        # Create the scatter plot
        fig = px.scatter(
            df,
            x='audienceScore',
            y='tomatoMeter',
            title='Relationship between Audience Score and Tomato Meter',
            labels={
                'audienceScore': 'Audience Score (%)',
                'tomatoMeter': "Critics' Score (Tomato Meter %)"
            }
        )

        # Calculate the regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            df['audienceScore'],
            df['tomatoMeter']
        )
        
        # Create x values for the regression line
        x_range = np.linspace(df['audienceScore'].min(), df['audienceScore'].max(), 100)
        y_regression = slope * x_range + intercept

        # Add regression line
        fig.add_trace(
            go.Scatter(
                x=x_range,
                y=y_regression,
                mode='lines',
                name='Regression Line',
                line=dict(color='red'),
                hoverinfo='skip'
            )
        )

        # Update layout
        fig.update_layout(
            width=800,
            height=600,
            showlegend=True,
            template='plotly_white',
            title={
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

        return fig

def get_rt_audience_tomato_corr(mrt_movies):
    return plot_audience_score_tomatoe_meter(data_corr_analysis(mrt_movies))