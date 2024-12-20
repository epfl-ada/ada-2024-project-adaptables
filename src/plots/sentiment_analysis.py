# This file contains the code for generating the 2 plots used for intefence from the sentiment analysis data
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr, ttest_ind
import pandas as pd
import numpy as np
from functools import partial, cache
from ..utils.data_utils import mrt_preprocess_df
import matplotlib.pyplot as plt
import seaborn as sns


## PLOTLY VERSION

def scatter_plot_corr(df_tuple, col1, col2, merge_col, movie_type):
    df1, df2 = df_tuple
    df_corr = pd.merge(df1, df2, on=merge_col)
    
    correlation_value, _ = pearsonr(df_corr[col1], df_corr[col2])
    
    # Regression line
    x = df_corr[col1]
    y = df_corr[col2]
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    # Create scatter plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name='Data points',
        marker=dict(
            color='blue',
            size=8
        )
    ))
    
    # Add regression line
    fig.add_trace(go.Scatter(
        x=x,
        y=p(x),
        mode='lines',
        name='Regression line',
        line=dict(color='red')
    ))
    
    # Update layout
    fig.update_layout(
        title=f"Scatter Plot with correlation {movie_type}: {correlation_value:.2f}",
        xaxis_title=col1,
        yaxis_title=col2,
        showlegend=True,
        height=600,
        width=800
    )
    
    return fig

def ttest_and_boxplot(df_comedy_tuple, df_not_comedy_tuple, column, expert_str):
    df_comedy_score, df_comedy_sa = df_comedy_tuple
    df_not_comedy_score, df_not_comedy_sa = df_not_comedy_tuple
    
    comedies = df_comedy_sa[column]
    not_comedies = df_not_comedy_sa[column]
    
    # Perform t-test
    t_stat, p_value = ttest_ind(comedies, not_comedies, equal_var=False)
    
    # Temporary dfs used for the visualization only
    comedies_df = pd.DataFrame({column: comedies, 'Group': 'Comedy'})
    not_comedies_df = pd.DataFrame({column: not_comedies, 'Group': 'Non-Comedy'})
    combined_df = pd.concat([comedies_df, not_comedies_df])
    summary_stats = combined_df.groupby('Group')[column]

    # Create box plots for each group
    fig = go.Figure()
    for group in ['Comedy', 'Non-Comedy']:
        fig.add_trace(go.Box(
            y=combined_df[combined_df['Group'] == group][column],
            name=group,
            boxpoints='outliers'
        ))
    
    # Update layout
    fig.update_layout(
        title=f"{column} distribution of {expert_str}: Comedy vs. Non-Comedy<br>"+
              f"T-Statistic: {t_stat:.2f}, P-Value: {p_value:.4f}",
        xaxis_title="Movie Type",
        yaxis_title=column,
        height=600,
        width=800
    )
    
    # Print statistical results
    print(f"T-Statistic: {t_stat:.2f}")
    print(f"P-Value: {p_value:.4f}")
    print("Conclusion:", "Significant difference between the two groups." if p_value < 0.05 
          else "No significant difference between the two groups.")
    print("\nSummary Statistics:")
    print(summary_stats.describe())
    
    return fig


### PLT version


# def scatter_plot_corr(df_tuple, col1, col2, merge_col, movie_type):
#     df1,df2 = df_tuple 
#     df_corr = pd.merge(df1, df2, on=merge_col)
    
#     #correlation_value = df_corr[col1].corr(df_corr[col2])
#     correlation_value, p_value = pearsonr(df_corr[col1], df_corr[col2]) 
#     f = plt.figure(figsize=(8, 6))
#     sns.regplot(x = col1, y = col2, data= df_corr, ci=None, line_kws={"color": "red"})
#     plt.title(f"Scatter Plot with correlation {movie_type}: {correlation_value:.2f}")
#     plt.xlabel(col1)
#     plt.ylabel(col2)
#     return f



# def ttest_and_boxplot (df_comedy_tuple, df_not_comedy_tuple, column, expert_str):
    
#     df_comedy_score, df_comedy_sa = df_comedy_tuple
#     df_not_comedy_score, df_not_comedy_sa = df_not_comedy_tuple
#     comedies = df_comedy_sa[column]
#     not_comedies = df_not_comedy_sa[column]

#     t_stat, p_value = ttest_ind(comedies, not_comedies, equal_var=False)
#     print(f"T-Statistic: {t_stat:.2f}")
#     print(f"P-Value: {p_value:.4f}")

#     if p_value < 0.05:
#         print("Conclusion: Significant difference between the two groups.")
#     else:
#         print("Conclusion: No significant difference between the two groups.")
    
#     comedies_df = pd.DataFrame({column: comedies, 'Group': 'Comedy'})
#     not_comedies_df = pd.DataFrame({column: not_comedies, 'Group': 'Non-Comedy'})
#     combined_df = pd.concat([comedies_df, not_comedies_df])

    
#     summary_stats = combined_df.groupby('Group')[column].describe()
#     print(summary_stats)

#     f = plt.figure(figsize=(8, 6))
#     sns.boxplot(x='Group', y=column, data=combined_df, palette='coolwarm')
#     plt.title(f"{column} distribution of {expert_str}  : Comedy vs. Non-Comedy")
#     plt.xlabel("Movie Type")
#     plt.ylabel(column)
#     return f

# @cache would have been very relevant -- unfortunately, it is not possible without monkey patching a custom dataframe hash
def _mrt_get_dfs(sa_df,col1, col2, merge_col,ci_df):
    preprocess_func = partial(mrt_preprocess_df,df=sa_df, col1=col1, col2=col2, merge_col=merge_col,comedy_ids=ci_df,use_zscore=False) 

    df_expert_comedies= preprocess_func(expert=True, comedy=True)
    df_non_expert_comedies = preprocess_func(expert=False, comedy=True)
    df_expert_not_comedies = preprocess_func(expert=True, comedy=False)
    df_non_expert_not_comedies = preprocess_func(expert=False, comedy=False)

    return [df_expert_comedies,df_non_expert_comedies,df_expert_not_comedies,df_non_expert_not_comedies]


def mrt_get_scatterplots(sa_df,col1, col2, merge_col,ci_df):
    # Gets the first scatter plots of the data story
    return [scatter_plot_corr(df, 'originalScore' ,'sa', 'id',title) for df,title in zip(_mrt_get_dfs(sa_df,col1, col2, merge_col,ci_df),['for comedies reviewed by experts','for comedies reviewed by non experts','for movies without comedies reviewed by experts', 'for movies without comedies reviewed by non-experts'])]

def mrt_get_boxplots(sa_df,col1, col2, merge_col,ci_df):
    # Get the boxplots of the data story
    df_expert_comedies,df_non_expert_comedies,df_expert_not_comedies,df_non_expert_not_comedies = _mrt_get_dfs(sa_df,col1, col2, merge_col,ci_df)
    return [ttest_and_boxplot(df_a,df_b,'sa',non_+'expert') for (df_a,df_b),non_ in zip([(df_expert_comedies, df_expert_not_comedies),(df_non_expert_comedies, df_non_expert_not_comedies)],['','non'])]
    