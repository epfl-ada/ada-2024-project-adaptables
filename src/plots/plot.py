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

if cfg.USE_MATPLOTLIB:
    import pandas as pd
    from matplotlib.colors import to_rgba

    def compare_topic_distrbutions(comedies_w_topicMemberships, non_comedies_w_topicMemberships, 
                            topics, group_col='year', bin_size=10, custom_bins=None):
        """
        Create a line chart showing the difference in MT element distributions between two datasets.
        
        Parameters:
        comedies_w_topicMemberships: Comedies DataFrame with columns 'year' and 'cMT'
        non_comedies_w_topicMemberships: Non-Comedies DataFrame with columns 'year' and 'cMT'
        topics: List of topics (labels)
        group_col: Column to group by (default 'year')
        bin_size: Size of year bins (default 10)
        custom_bins: Custom bins if needed
        
        Returns:
        matplotlib.figure.Figure: Figure showing difference in proportions (comedies - non_comedies)
        """
        def get_proportions(group, column, categories):
            counts = pd.Series(0, index=range(len(categories)))
            for idx in group[column]:
                counts[idx] += 1
            return counts / len(group) if len(group) > 0 else counts
        
        # Create copies and drop NA values
        comedies = comedies_w_topicMemberships.copy().dropna(subset=[group_col])
        non_comedies = non_comedies_w_topicMemberships.copy().dropna(subset=[group_col])
        
        # Create bins
        if pd.api.types.is_numeric_dtype(comedies[group_col]):
            if custom_bins is not None:
                bin_labels = [f"{custom_bins[i]}-{custom_bins[i+1]}" for i in range(len(custom_bins)-1)]
                comedies['group_bin'] = pd.cut(comedies[group_col], bins=custom_bins, labels=bin_labels)
                non_comedies['group_bin'] = pd.cut(non_comedies[group_col], bins=custom_bins, labels=bin_labels)
            else:
                min_val = min(comedies[group_col].min(), non_comedies[group_col].min())
                max_val = max(comedies[group_col].max(), non_comedies[group_col].max())
                min_val = (min_val // bin_size) * bin_size
                max_val = ((max_val // bin_size) + 1) * bin_size
                bins = range(int(min_val), int(max_val + bin_size), bin_size)
                bin_labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)]
                comedies['group_bin'] = pd.cut(comedies[group_col], bins=bins, labels=bin_labels)
                non_comedies['group_bin'] = pd.cut(non_comedies[group_col], bins=bins, labels=bin_labels)
        else:
            comedies['group_bin'] = comedies[group_col]
            non_comedies['group_bin'] = non_comedies[group_col]
        
        # Get all unique bins
        all_bins = sorted(set(comedies['group_bin'].unique()) | set(non_comedies['group_bin'].unique()))
        
        # Calculate proportions for each bin
        results = []
        for group_bin in all_bins:
            group_a = comedies[comedies['group_bin'] == group_bin]
            group_b = non_comedies[non_comedies['group_bin'] == group_bin]
            
            mt_props_a = get_proportions(group_a, 'cMT', topics)
            mt_props_b = get_proportions(group_b, 'cMT', topics)
            
            mt_diff = mt_props_a - mt_props_b
            results.append({
                'group_bin': group_bin,
                'MT_diff': mt_diff
            })
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Use a colormap that approximates Plotly's Set3
        colors = plt.cm.Set3(np.linspace(0, 1, len(topics)))
        
        # Plot each topic
        for element_idx, element in enumerate(topics):
            y_values = [result['MT_diff'][element_idx] for result in results]
            x_values = range(len(all_bins))
            color = colors[element_idx]
            
            # Create line plot with markers
            ax.plot(x_values, y_values, '-o', label=element, color=color, 
                    linewidth=2, markersize=6)
            
            # Add filled area
            ax.fill_between(x_values, y_values, 0, 
                        color=to_rgba(color, 0.2))
        
        # Add reference line at y=0
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        
        # Set axis labels and title
        ax.set_xlabel(group_col.capitalize())
        ax.set_ylabel('Difference in Proportion')
        ax.set_title(f'Difference in topic distribution by {group_col}\n(Comedies (positive) compared to Non-comedies)')
        
        # Set x-axis ticks
        ax.set_xticks(range(len(all_bins)))
        ax.set_xticklabels([str(b) for b in all_bins], rotation=45, ha='right')
        
        # Make y-axis symmetric around 0
        y_values_all = [v for result in results for v in result['MT_diff']]
        max_abs_diff = max(abs(min(y_values_all)), abs(max(y_values_all))) * 1.1
        ax.set_ylim(-max_abs_diff, max_abs_diff)
        
        # Add legend
        ax.legend(title='Topics', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        return fig

    def analyze_distributions(comedies_w_topicMemberships, topics, group_col='year', 
                            bin_size=10, custom_bins=None):
        """
        Create stacked bar charts showing the distribution of elements over time periods.
        
        Parameters:
        comedies_w_topicMemberships: DataFrame with columns 'year', 'cMT'
        topics: List of topics
        group_col: Column to group by (default 'year')
        bin_size: Size of year bins (default 10)
        custom_bins: Custom bins if needed
        
        Returns:
        matplotlib.figure.Figure: Figure containing the stacked bar chart
        """
        # Drop NA values
        comedies_w_topicMemberships = comedies_w_topicMemberships.dropna(subset=[group_col])
        
        # Create bins
        if pd.api.types.is_numeric_dtype(comedies_w_topicMemberships[group_col]):
            if custom_bins is not None:
                bin_labels = [f"{custom_bins[i]}-{custom_bins[i+1]}" for i in range(len(custom_bins)-1)]
                comedies_w_topicMemberships['group_bin'] = pd.cut(
                    comedies_w_topicMemberships[group_col], 
                    bins=custom_bins, 
                    labels=bin_labels
                )
            else:
                min_val = (comedies_w_topicMemberships[group_col].min() // bin_size) * bin_size
                max_val = ((comedies_w_topicMemberships[group_col].max() // bin_size) + 1) * bin_size
                bins = range(int(min_val), int(max_val + bin_size), bin_size)
                bin_labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)]
                comedies_w_topicMemberships['group_bin'] = pd.cut(
                    comedies_w_topicMemberships[group_col], 
                    bins=bins, 
                    labels=bin_labels
                )
        else:
            comedies_w_topicMemberships['group_bin'] = comedies_w_topicMemberships[group_col]
        
        def get_proportions(group, column, categories):
            counts = pd.Series(0, index=range(len(categories)))
            for idx in group[column]:
                counts[idx] += 1
            return counts / len(group)
        
        # Calculate proportions for each bin
        results = []
        for group_bin in sorted(comedies_w_topicMemberships['group_bin'].unique()):
            group = comedies_w_topicMemberships[comedies_w_topicMemberships['group_bin'] == group_bin]
            topic_props = get_proportions(group, 'cMT', topics)
            
            results.append({
                'group_bin': group_bin,
                'MT': topic_props
            })
        
        # Create the figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Use Set3 colormap for consistency with the previous plot
        colors = plt.cm.Set3(np.linspace(0, 1, len(topics)))
        
        # Get x-axis locations and labels
        x = np.arange(len(results))
        width = 0.8  # Width of the bars
        
        # Create bottom offset for stacking
        bottom = np.zeros(len(results))
        
        # Plot each topic as a stacked bar
        for topic_idx, topic in enumerate(topics):
            y_values = [result['MT'][topic_idx] for result in results]
            ax.bar(x, y_values, width, bottom=bottom, label=topic, 
                color=colors[topic_idx])
            bottom += y_values
        
        # Customize the plot
        ax.set_title('Topic Distribution by ' + group_col)
        ax.set_xlabel(group_col.capitalize())
        ax.set_ylabel('Proportion')
        
        # Set x-axis ticks
        ax.set_xticks(x)
        ax.set_xticklabels([str(r['group_bin']) for r in results], 
                        rotation=45, ha='right')
        
        # Set y-axis range
        ax.set_ylim(0, 1)
        
        # Add legend
        ax.legend(title='Topics', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Add grid for better readability
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        return fig
else:
    def compare_topic_distrbutions(comedies_w_topicMemberships, non_comedies_w_topicMemberships, topics, group_col='year', bin_size=10, custom_bins=None):
        """
        Create a line chart showing the difference in MT element distributions between two datasets.
        
        Parameters:
        comedies_w_topicMemberships: Comedies DataFrame with columns 'year' and 'cMT' - the membership index of each plot to a topic
        non_comedies_w_topicMemberships: Non-Comedies DataFrame with columns 'year' and 'cMT' - the membership index of each plot to a topic
        topic: List of topics (labels)
        group_col: Column to group by (default 'year')
        bin_size: Size of year bins (default 10)
        custom_bins: Custom bins if needed
        
        Returns:
        Plotly figure showing difference in proportions (comedies - non_comedies)
        """
        # Function to calculate proportions for each category
        def get_proportions(group, column, categories):
            counts = pd.Series(0, index=range(len(categories)))
            for idx in group[column]:
                counts[idx] += 1
            return counts / len(group) if len(group) > 0 else counts
        
        # Create a copy of the dataframes to avoid modifying the originals
        comedies_w_topicMemberships = comedies_w_topicMemberships.copy()
        non_comedies_w_topicMemberships = non_comedies_w_topicMemberships.copy()
        
        # Drop NA values
        comedies_w_topicMemberships = comedies_w_topicMemberships.dropna(subset=[group_col])
        non_comedies_w_topicMemberships = non_comedies_w_topicMemberships.dropna(subset=[group_col])
        
        # Create bins based on the grouping column type
        if pd.api.types.is_numeric_dtype(comedies_w_topicMemberships[group_col]):
            if custom_bins is not None:
                bin_labels = [f"{custom_bins[i]}-{custom_bins[i+1]}" for i in range(len(custom_bins)-1)]
                comedies_w_topicMemberships['group_bin'] = pd.cut(comedies_w_topicMemberships[group_col], bins=custom_bins, labels=bin_labels)
                non_comedies_w_topicMemberships['group_bin'] = pd.cut(non_comedies_w_topicMemberships[group_col], bins=custom_bins, labels=bin_labels)
            else:
                min_val = min(comedies_w_topicMemberships[group_col].min(), non_comedies_w_topicMemberships[group_col].min())
                max_val = max(comedies_w_topicMemberships[group_col].max(), non_comedies_w_topicMemberships[group_col].max())
                min_val = (min_val // bin_size) * bin_size
                max_val = ((max_val // bin_size) + 1) * bin_size
                bins = range(int(min_val), int(max_val + bin_size), bin_size)
                bin_labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)]
                comedies_w_topicMemberships['group_bin'] = pd.cut(comedies_w_topicMemberships[group_col], bins=bins, labels=bin_labels)
                non_comedies_w_topicMemberships['group_bin'] = pd.cut(non_comedies_w_topicMemberships[group_col], bins=bins, labels=bin_labels)
        else:
            comedies_w_topicMemberships['group_bin'] = comedies_w_topicMemberships[group_col]
            non_comedies_w_topicMemberships['group_bin'] = non_comedies_w_topicMemberships[group_col]
        
        # Now we can safely get all unique bins
        all_bins = sorted(set(comedies_w_topicMemberships['group_bin'].unique()) | set(non_comedies_w_topicMemberships['group_bin'].unique()))
        
        # Calculate proportions for each bin in both datasets
        results = []
        for group_bin in all_bins:
            group_a = comedies_w_topicMemberships[comedies_w_topicMemberships['group_bin'] == group_bin]
            group_b = non_comedies_w_topicMemberships[non_comedies_w_topicMemberships['group_bin'] == group_bin]
            
            mt_props_a = get_proportions(group_a, 'cMT', topics)
            mt_props_b = get_proportions(group_b, 'cMT', topics)
            
            # Calculate difference in proportions
            mt_diff = mt_props_a - mt_props_b
            
            results.append({
                'group_bin': group_bin,
                'MT_diff': mt_diff
            })
        
        fig = go.Figure()
        colors = px.colors.qualitative.Set3
        
        # Add a line for each MT element with filled area
        for element_idx, element in enumerate(topics):
            y_values = [result['MT_diff'][element_idx] for result in results]
            color = colors[element_idx % len(colors)]
            
            fig.add_trace(
                go.Scatter(
                    name=f'{element}',
                    x=[str(r['group_bin']) for r in results],
                    y=y_values,
                    mode='lines+markers',
                    line=dict(color=color, width=2),
                    marker=dict(size=8),
                    fill='tozeroy',  # Fill to zero on y-axis
                    fillcolor=color.replace('rgb', 'rgba').replace(')', ',0.2)'),  # Add transparency
                    hovertemplate='%{text}<br>Difference in Proportion: %{y:.2%}<extra></extra>',
                    text=[element] * len(y_values)
                )
            )

        
        # Add a reference line at y=0
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        # Update layout
        fig.update_layout(
            title=f'Difference in topic distribution by {group_col} (Comedies (positive), compared to Non-comedies)',
            yaxis_title='Difference in Proportion',
            xaxis_title=group_col.capitalize(),
            height=400,
            showlegend=True,
            legend_title_text='Topics'
        )
        
        # Update y-axis range to be symmetrical around 0
        max_abs_diff = max(abs(min(min(y_values) for element_idx, element in enumerate(topics))), 
                        abs(max(max(y_values) for element_idx, element in enumerate(topics)))) * 1.1
        fig.update_yaxes(range=[-max_abs_diff, max_abs_diff])
        
        return fig
    
    def analyze_distributions(comedies_w_topicMemberships, topics, group_col='year', bin_size=10, custom_bins=None):
        """
        Create separate stacked bar charts showing the distribution of elements over time periods.
        
        Parameters:
        comedies_w_topicMemberships: DataFrame with columns 'year', 'cMT'
        MT: List of topics
        bin_size: Size of year bins (default 10)
        
        Returns:
        List of three Plotly figures
        """
        comedies_w_topicMemberships = comedies_w_topicMemberships.dropna(subset=[group_col])
        
        # Create bins based on the grouping column type
        if pd.api.types.is_numeric_dtype(comedies_w_topicMemberships[group_col]):
            if custom_bins is not None:
                comedies_w_topicMemberships.loc[:,'group_bin'] = pd.cut(comedies_w_topicMemberships[group_col], bins=custom_bins, labels=[f"{custom_bins[i]}-{custom_bins[i+1]}" for i in range(len(custom_bins)-1)])
            else:
                min_val = (comedies_w_topicMemberships[group_col].min() // bin_size) * bin_size
                max_val = ((comedies_w_topicMemberships[group_col].max() // bin_size) + 1) * bin_size
                bins = range(int(min_val), int(max_val + bin_size), bin_size)
                comedies_w_topicMemberships.loc[:,'group_bin'] = pd.cut(comedies_w_topicMemberships[group_col], bins=bins, labels=[f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)])
        else:
            # For non-numeric columns, use the values directly
            comedies_w_topicMemberships['group_bin'] = comedies_w_topicMemberships[group_col]
        
        # Function to calculate proportions for each category
        def get_proportions(group, column, categories):
            counts = pd.Series(0, index=range(len(categories)))
            for idx in group[column]:
                counts[idx] += 1
            return counts / len(group)
        
        # Calculate proportions for each bin
        results = []
        for group_bin in sorted(comedies_w_topicMemberships['group_bin'].unique()):
            group = comedies_w_topicMemberships[comedies_w_topicMemberships['group_bin'] == group_bin]
            topic_props = get_proportions(group, 'cMT', topics)
            
            results.append({
                'group_bin': group_bin,
                'Topic': topic_props
            })
        
        # Create separate figures for each category
        categories = [('Topic',topics)]
        colors = px.colors.qualitative.Set3
        figures = []
        
        for cat_name, elements in categories:
            fig = go.Figure()
            
            for element_idx, element in enumerate(elements):
                y_values = [result[cat_name][element_idx] for result in results]
                
                fig.add_trace(
                    go.Bar(
                        name=f'{element}',
                        x=[str(r['group_bin']) for r in results],
                        y=y_values,
                        marker_color=colors[element_idx % len(colors)],
                        hovertemplate='%{text}<br>Proportion: %{y:.2%}<extra></extra>',
                        text=[element] * len(y_values)
                    )
                )
            
            # Update layout for each figure
            fig.update_layout(
                title=f'{cat_name} Distribution by {group_col}',
                yaxis_title='Proportion',
                xaxis_title=group_col.capitalize(),
                barmode='stack',
                height=400,
                showlegend=True,
                legend_title_text='Topics'
            )
            
            # Update y-axis range
            fig.update_yaxes(range=[0, 1])
            
            figures.append(fig)
        
        return figures

    
def cmu_plots_get_topic_distributions(cmu_topic_similarities,topic_list):
    merged_comedies = cmu_topic_similarities.loc[cmu_topic_similarities.genres.apply(lambda s: "Comedy" in s),:]
    merged_nc = cmu_topic_similarities.iloc[~merged_comedies.index]
    return compare_topic_distrbutions(merged_comedies,merged_nc,topic_list,group_col='year', bin_size=10)

def cmu_plots_get_money_distr(cmu_topic_similarities,topic_list):
    merged_comedies = cmu_topic_similarities.loc[cmu_topic_similarities.genres.apply(lambda s: "Comedy" in s),:]
    return analyze_distributions(merged_comedies,topic_list,group_col="box_office_revenue",custom_bins = [0, 100_000, 1_000_000, 10_000_000, float('inf')])