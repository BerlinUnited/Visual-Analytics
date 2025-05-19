# Function to create a comprehensive analysis of ball visibility
def analyze_ball_visibility(df, output_dir=None):
    """
    Perform a comprehensive analysis of ball visibility data with multiple visualizations
    """
    if output_dir and not output_dir.endswith('/'):
        output_dir += '/'
    
    # Make sure output directory exists
    if output_dir:
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    # 1. Overall player visibility histogram (all games)
    player_vis_path = f"{output_dir}player_visibility_all_games.png" if output_dir else None
    plot_player_visibility_histogram(df, save_path=player_vis_path)
    
    # 2. Game visibility histogram (average per game)
    game_vis_path = f"{output_dir}game_visibility.png" if output_dir else None
    plot_game_visibility_histogram(df, save_path=game_vis_path)
    
    # 3. Combined game halves histogram (whole games)
    combined_game_path = f"{output_dir}combined_game_halves_visibility.png" if output_dir else None
    plot_combined_game_halves_histogram(df, save_path=combined_game_path)
    
    # 4. Maximum robot visibility per game
    max_robot_path = f"{output_dir}max_robot_visibility.png" if output_dir else None
    max_robot_data = plot_max_robot_visibility_histogram(df, save_path=max_robot_path)
    
    # 5. Minimum robot visibility per game
    min_robot_path = f"{output_dir}min_robot_visibility.png" if output_dir else None
    min_robot_data = plot_min_robot_visibility_histogram(df, save_path=min_robot_path)
    
    # 6. Second worst robot visibility per game
    second_min_robot_path = f"{output_dir}second_min_robot_visibility.png" if output_dir else None
    second_min_robot_data = plot_second_min_robot_visibility_histogram(df, save_path=second_min_robot_path)
    
    # 7. Event-specific analysis
    events = df['event'].unique()
    for event in events:
        # Skip if there are too few records for this event
        event_df = df[df['event'] == event]
        if len(event_df) < 3:
            continue
            
        # Create event-specific player visibility histogram
        event_player_path = f"{output_dir}player_visibility_event_{event}.png" if output_dir else None
        plot_player_visibility_histogram(df, event_filter=event, save_path=event_player_path)
        
        # Create event-specific game visibility histogram
        event_game_path = f"{output_dir}game_visibility_event_{event}.png" if output_dir else None
        plot_game_visibility_histogram(df, event_filter=event, save_path=event_game_path)
        
        # Create event-specific combined halves histogram
        event_combined_path = f"{output_dir}combined_halves_event_{event}.png" if output_dir else None
        plot_combined_game_halves_histogram(df, event_filter=event, save_path=event_combined_path)
        
        # Create event-specific max robot histogram
        event_max_robot_path = f"{output_dir}max_robot_event_{event}.png" if output_dir else None
        plot_max_robot_visibility_histogram(df, event_filter=event, save_path=event_max_robot_path)
        
        # Create event-specific min robot histogram
        event_min_robot_path = f"{output_dir}min_robot_event_{event}.png" if output_dir else None
        plot_min_robot_visibility_histogram(df, event_filter=event, save_path=event_min_robot_path)
        
        # Create event-specific second-worst robot histogram
        event_second_min_path = f"{output_dir}second_min_robot_event_{event}.png" if output_dir else None
        plot_second_min_robot_visibility_histogram(df, event_filter=event, save_path=event_second_min_path)
    
    # 8. Game-specific player visibility (for each game)
    games = df[['game_id', 'game_name']].drop_duplicates().values
    for game_id, game_name in games:
        # Skip if there are too few records for this game
        game_df = df[df['game_id'] == game_id]
        if len(game_df) < 3:
            continue
            
        # Create game-specific player visibility histogram
        game_player_path = f"{output_dir}player_visibility_game_{game_id}.png" if output_dir else None
        plot_player_visibility_histogram(df, game_filter=game_id, save_path=game_player_path)
    
    # 9. Summary statistics
    print("\n=== BALL VISIBILITY ANALYSIS SUMMARY ===")
    print(f"Total records analyzed: {len(df)}")
    print(f"Number of unique games: {df['game_id'].nunique()}")
    print(f"Number of unique events: {df['event'].nunique()}")
    
    # Overall statistics
    avg_visibility = df['knows_true_percent'].mean()
    median_visibility = df['knows_true_percent'].median()
    min_visibility = df['knows_true_percent'].min()
    max_visibility = df['knows_true_percent'].max()
    
    print("\nOverall Ball Visibility Statistics:")
    print(f"Average: {avg_visibility:.2f}%")
    print(f"Median: {median_visibility:.2f}%")
    print(f"Minimum: {min_visibility:.2f}%")
    print(f"Maximum: {max_visibility:.2f}%")
    print(f"Range: {max_visibility - min_visibility:.2f}%")
    
    # Stats by player
    print("\nBall Visibility by Player:")
    player_stats = df.groupby('player')['knows_true_percent'].agg(['mean', 'median', 'min', 'max', 'count']).reset_index()
    player_stats = player_stats.sort_values('mean', ascending=False)  # Sort descending by mean visibility
    
    for _, row in player_stats.iterrows():
        print(f"Player {row['player']}: Avg={row['mean']:.2f}%,import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from collections import defaultdict

# Function to load and prepare the data
def load_ball_visibility_data(csv_file_path):
    """
    Load ball visibility data from CSV and prepare it for analysis
    """
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Convert percentage columns to float if they're not already
    percentage_columns = ['knows_true_percent', 'knows_false_percent']
    for col in percentage_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Print basic information about the dataset
    print(f"Loaded data with {len(df)} records")
    print(f"Number of unique games: {df['game_id'].nunique()}")
    print(f"Number of unique events: {df['event'].nunique()}")
    
    return df

# Function to create histograms for player ball visibility
def plot_player_visibility_histogram(df, game_filter=None, event_filter=None, save_path=None):
    """
    Create a histogram showing ball visibility per player
    Optionally filter by game_id or event
    """
    # Apply filters if provided
    filtered_df = df.copy()
    title_suffix = ""
    
    if game_filter is not None:
        filtered_df = filtered_df[filtered_df['game_id'] == game_filter]
        game_name = filtered_df['game_name'].iloc[0] if not filtered_df.empty else f"Game ID {game_filter}"
        title_suffix = f" - {game_name}"
    
    if event_filter is not None:
        filtered_df = filtered_df[filtered_df['event'] == event_filter]
        title_suffix = f"{title_suffix} - Event: {event_filter}"
    
    if filtered_df.empty:
        print("No data available after applying filters.")
        return
        
    # Count unique players to determine team size and color
    player_count = filtered_df['player'].nunique()
    bar_color = get_team_color(player_count)
    
    # Create the visualization
    plt.figure(figsize=(12, 8))
    
    # Create the player visibility bar chart with color based on team size
    player_data = filtered_df.groupby('player')['knows_true_percent'].mean().reset_index()
    player_data = player_data.sort_values('knows_true_percent', ascending=False)  # Sort descending
    
    # Create bar chart
    ax = plt.bar(player_data['player'].astype(str), player_data['knows_true_percent'], color=bar_color)
    
    # Calculate and plot the average line
    avg_visibility = filtered_df['knows_true_percent'].mean()
    plt.axhline(y=avg_visibility, color='red', linestyle='--', label=f'Average: {avg_visibility:.2f}%')
    
    # Add value labels on top of each bar
    for i, rect in enumerate(ax):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., height + 1,
                 f'{height:.2f}%', 
                 ha="center", fontsize=10)
    
    # Set labels and title
    plt.title(f'Ball Visibility per Player{title_suffix}', fontsize=14)
    plt.xlabel('Player', fontsize=12)
    plt.ylabel('Ball Visibility (%)', fontsize=12)
    plt.ylim(0, max(player_data['knows_true_percent']) * 1.15)  # Add space for labels
    
    # Create custom legend for team size
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=bar_color, label=f'{player_count} Robots'),
        plt.Line2D([0], [0], color='red', linestyle='--', label=f'Avg: {avg_visibility:.2f}%')
    ]
    plt.legend(handles=legend_elements)
    
    plt.grid(axis='y', alpha=0.3)
    
    # Add stats in a text box
    stats_text = (
        f"Average: {avg_visibility:.2f}%\n"
        f"Median: {player_data['knows_true_percent'].median():.2f}%\n"
        f"Min: {player_data['knows_true_percent'].min():.2f}%\n"
        f"Max: {player_data['knows_true_percent'].max():.2f}%\n"
        f"Range: {player_data['knows_true_percent'].max() - player_data['knows_true_percent'].min():.2f}%"
    )
    
    plt.figtext(0.15, 0.02, stats_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Player visibility histogram saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

# Function to create histograms for game ball visibility
def plot_game_visibility_histogram(df, event_filter=None, save_path=None):
    """
    Create a histogram showing average ball visibility per game
    Optionally filter by event
    """
    # Apply event filter if provided
    filtered_df = df.copy()
    title_suffix = ""
    
    if event_filter is not None:
        filtered_df = filtered_df[filtered_df['event'] == event_filter]
        title_suffix = f" - Event: {event_filter}"
    
    if filtered_df.empty:
        print("No data available after applying filters.")
        return
    
    # Calculate average visibility per game and count players per game
    game_data = []
    for (game_id, game_name), game_group in filtered_df.groupby(['game_id', 'game_name']):
        avg_visibility = game_group['knows_true_percent'].mean()
        player_count = game_group['player'].nunique()
        
        game_data.append({
            'game_id': game_id,
            'game_name': game_name,
            'game_label': f"{game_name} (ID: {game_id})",
            'knows_true_percent': avg_visibility,
            'player_count': player_count
        })
    
    # Convert to DataFrame
    game_avg = pd.DataFrame(game_data)
    
    # Sort by average visibility for better visualization (descending order)
    game_avg = game_avg.sort_values('knows_true_percent', ascending=False)
    
    # Create the visualization
    plt.figure(figsize=(14, 8))
    
    # Create the game visibility bar chart with colors based on team size
    bar_colors = [get_team_color(count) for count in game_avg['player_count']]
    ax = plt.bar(game_avg['game_label'], game_avg['knows_true_percent'], color=bar_colors)
    
    # Calculate and plot the overall average line
    overall_avg = game_avg['knows_true_percent'].mean()
    plt.axhline(y=overall_avg, color='red', linestyle='--', label=f'Overall Avg: {overall_avg:.2f}%')
    
    # Add value labels on top of each bar
    for i, rect in enumerate(ax):
        height = rect.get_height()
        player_count = game_avg.iloc[i]['player_count']
        plt.text(rect.get_x() + rect.get_width()/2., 
                 height + 1,
                 f'{height:.2f}%\n({player_count} robots)', 
                 ha="center", fontsize=9, rotation=0)
    
    # Set labels and title
    plt.title(f'Average Ball Visibility per Game{title_suffix}', fontsize=14)
    plt.xlabel('Game', fontsize=12)
    plt.ylabel('Average Ball Visibility (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, max(game_avg['knows_true_percent']) * 1.15)  # Add space for labels
    
    # Create custom legend for team sizes
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#4287f5', label='7 Robots'),
        Patch(facecolor='#f59e42', label='5 Robots'),
        plt.Line2D([0], [0], color='red', linestyle='--', label=f'Overall Avg: {overall_avg:.2f}%')
    ]
    plt.legend(handles=legend_elements)
    
    plt.grid(axis='y', alpha=0.3)
    
    # Add stats in a text box
    stats_text = (
        f"Overall Average: {overall_avg:.2f}%\n"
        f"Median: {game_avg['knows_true_percent'].median():.2f}%\n"
        f"Min: {game_avg['knows_true_percent'].min():.2f}%\n"
        f"Max: {game_avg['knows_true_percent'].max():.2f}%\n"
        f"Range: {game_avg['knows_true_percent'].max() - game_avg['knows_true_percent'].min():.2f}%"
    )
    
    plt.figtext(0.15, 0.02, stats_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Game visibility histogram saved to {save_path}")
    else:
        plt.show()
    
    plt.close()
    
    return game_avg
    
    # Calculate and plot the overall average line
    overall_avg = game_avg['knows_true_percent'].mean()
    plt.axhline(y=overall_avg, color='red', linestyle='--', label=f'Overall Avg: {overall_avg:.2f}%')
    
    # Add value labels on top of each bar
    for i, rect in enumerate(ax):
        height = rect.get_height()
        player_count = game_avg.iloc[i]['player_count']
        plt.text(rect.get_x() + rect.get_width()/2., 
                 height + 1,
                 f'{height:.2f}%\n({player_count} robots)', 
                 ha="center", fontsize=9, rotation=0)
    
    # Set labels and title
    plt.title(f'Average Ball Visibility per Game{title_suffix}', fontsize=14)
    plt.xlabel('Game', fontsize=12)
    plt.ylabel('Average Ball Visibility (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, max(game_avg['knows_true_percent']) * 1.15)  # Add space for labels
    
    # Create custom legend for team sizes
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#4287f5', label='7 Robots'),
        Patch(facecolor='#f59e42', label='5 Robots'),
        plt.Line2D([0], [0], color='red', linestyle='--', label=f'Overall Avg: {overall_avg:.2f}%')
    ]
    plt.legend(handles=legend_elements)
    
    plt.grid(axis='y', alpha=0.3)
    
    # Add stats in a text box
    stats_text = (
        f"Overall Average: {overall_avg:.2f}%\n"
        f"Median: {game_avg['knows_true_percent'].median():.2f}%\n"
        f"Min: {game_avg['knows_true_percent'].min():.2f}%\n"
        f"Max: {game_avg['knows_true_percent'].max():.2f}%\n"
        f"Range: {game_avg['knows_true_percent'].max() - game_avg['knows_true_percent'].min():.2f}%"
    )
    
    plt.figtext(0.15, 0.02, stats_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Game visibility histogram saved to {save_path}")
    else:
        plt.show()
    
    plt.close()='knows_true_percent', data=game_avg, color='#4287f5')  # Single consistent blue color
    
    # Calculate and plot the overall average line
    overall_avg = game_avg['knows_true_percent'].mean()
    plt.axhline(y=overall_avg, color='orange', linestyle='--', label=f'Overall Avg: {overall_avg:.2f}%')
    
    # Add value labels on top of each bar
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        ax.text(p.get_x() + p.get_width()/2., 
                height + 1,
                f'{height:.2f}%', 
                ha="center", fontsize=9, rotation=0)
    
    # Set labels and title
    plt.title(f'Average Ball Visibility per Game{title_suffix}', fontsize=14)
    plt.xlabel('Game', fontsize=12)
    plt.ylabel('Average Ball Visibility (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, max(game_avg['knows_true_percent']) * 1.15)  # Add space for labels
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Add stats in a text box
    stats_text = (
        f"Overall Average: {overall_avg:.2f}%\n"
        f"Median: {game_avg['knows_true_percent'].median():.2f}%\n"
        f"Min: {game_avg['knows_true_percent'].min():.2f}%\n"
        f"Max: {game_avg['knows_true_percent'].max():.2f}%\n"
        f"Range: {game_avg['knows_true_percent'].max() - game_avg['knows_true_percent'].min():.2f}%"
    )
    
    plt.figtext(0.15, 0.02, stats_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Game visibility histogram saved to {save_path}")
    else:
        plt.show()
    
    plt.close()
    
# Function to plot minimum ball visibility per game and which robot achieved it
def plot_min_robot_visibility_histogram(df, event_filter=None, save_path=None):
    """
    Create a histogram showing the minimum ball visibility per game 
    and identifying which robot had the lowest visibility
    """
    # Apply event filter if provided
    filtered_df = df.copy()
    title_suffix = ""
    
    if event_filter is not None:
        filtered_df = filtered_df[filtered_df['event'] == event_filter]
        title_suffix = f" - Event: {event_filter}"
    
    if filtered_df.empty:
        print("No data available after applying filters.")
        return
    
    # Group by game to find the minimum visibility and which player had it
    game_min_data = []
    
    # Group by game_id and game_name
    for (game_id, game_name), game_group in filtered_df.groupby(['game_id', 'game_name']):
        # Find the row with the minimum visibility
        min_row = game_group.loc[game_group['knows_true_percent'].idxmin()]
        
        # Count unique players in this game
        player_count = game_group['player'].nunique()
        
        game_min_data.append({
            'game_id': game_id,
            'game_name': game_name,
            'min_visibility': min_row['knows_true_percent'],
            'worst_player': min_row['player'],
            'game_label': f"{game_name} (ID: {game_id})",
            'player_count': player_count
        })
    
    # Convert to DataFrame
    game_min_df = pd.DataFrame(game_min_data)
    
    # Sort by minimum visibility in ascending order (worst first)
    game_min_df = game_min_df.sort_values('min_visibility')
    
    # Create the visualization
    plt.figure(figsize=(14, 8))
    
    # Create the game min visibility bar chart with colors based on team size
    ax = plt.bar(game_min_df['game_label'], game_min_df['min_visibility'], 
                 color=[get_team_color(count) for count in game_min_df['player_count']])
    
    # Calculate and plot the overall average line for min values
    overall_min_avg = game_min_df['min_visibility'].mean()
    plt.axhline(y=overall_min_avg, color='red', linestyle='--', 
                label=f'Avg Min: {overall_min_avg:.2f}%')
    
    # Add value labels on top of each bar showing min value and player
    for i, rect in enumerate(ax):
        height = rect.get_height()
        player = game_min_df.iloc[i]['worst_player']
        player_count = game_min_df.iloc[i]['player_count']
        plt.text(rect.get_x() + rect.get_width()/2., height + 1,
                 f'{height:.2f}%\nPlayer {player}\n({player_count} robots)', 
                 ha="center", fontsize=9, rotation=0)
    
    # Set labels and title
    plt.title(f'Minimum Ball Visibility per Game (Worst Robot){title_suffix}', fontsize=14)
    plt.xlabel('Game', fontsize=12)
    plt.ylabel('Minimum Ball Visibility (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, max(game_min_df['min_visibility']) * 1.15)  # Add space for labels
    
    # Create custom legend for team sizes
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#4287f5', label='7 Robots'),
        Patch(facecolor='#f59e42', label='5 Robots'),
        plt.Line2D([0], [0], color='red', linestyle='--', label=f'Avg Min: {overall_min_avg:.2f}%')
    ]
    plt.legend(handles=legend_elements)
    
    plt.grid(axis='y', alpha=0.3)
    
    # Add stats in a text box
    stats_text = (
        f"Average Min: {overall_min_avg:.2f}%\n"
        f"Median Min: {game_min_df['min_visibility'].median():.2f}%\n"
        f"Min of Min: {game_min_df['min_visibility'].min():.2f}%\n"
        f"Max of Min: {game_min_df['min_visibility'].max():.2f}%\n"
        f"Range: {game_min_df['min_visibility'].max() - game_min_df['min_visibility'].min():.2f}%"
    )
    
    plt.figtext(0.15, 0.02, stats_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Minimum robot visibility histogram saved to {save_path}")
    else:
        plt.show()
    
    plt.close()
    
    return game_min_df
    # Apply event filter if provided
    filtered_df = df.copy()
    title_suffix = ""
    
    if event_filter is not None:
        filtered_df = filtered_df[filtered_df['event'] == event_filter]
        title_suffix = f" - Event: {event_filter}"
    
    if filtered_df.empty:
        print("No data available after applying filters.")
        return
    
    # Group by game to find the maximum visibility and which player achieved it
    game_max_data = []
    
    # Group by game_id and game_name
    for (game_id, game_name), game_group in filtered_df.groupby(['game_id', 'game_name']):
        # Find the row with the maximum visibility
        max_row = game_group.loc[game_group['knows_true_percent'].idxmax()]
        
        game_max_data.append({
            'game_id': game_id,
            'game_name': game_name,
            'max_visibility': max_row['knows_true_percent'],
            'top_player': max_row['player'],
            'game_label': f"{game_name} (ID: {game_id})"
        })
    
    # Convert to DataFrame
    game_max_df = pd.DataFrame(game_max_data)
    
    # Sort by maximum visibility in descending order
    game_max_df = game_max_df.sort_values('max_visibility', ascending=False)
    
    # Create the visualization
    plt.figure(figsize=(14, 8))
    
    # Create the game max visibility bar chart with a single consistent color
    ax = sns.barplot(x='game_label', y='max_visibility', data=game_max_df, color='#4287f5')
    
    # Calculate and plot the overall average line for max values
    overall_max_avg = game_max_df['max_visibility'].mean()
    plt.axhline(y=overall_max_avg, color='orange', linestyle='--', 
                label=f'Avg Max: {overall_max_avg:.2f}%')
    
    # Add value labels on top of each bar showing max value and player
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        player = game_max_df.iloc[i]['top_player']
        ax.text(p.get_x() + p.get_width()/2., 
                height + 1,
                f'{height:.2f}%\nPlayer {player}', 
                ha="center", fontsize=9, rotation=0)
    
    # Set labels and title
    plt.title(f'Maximum Ball Visibility per Game (Best Robot){title_suffix}', fontsize=14)
    plt.xlabel('Game', fontsize=12)
    plt.ylabel('Maximum Ball Visibility (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, max(game_max_df['max_visibility']) * 1.15)  # Add space for labels
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Add stats in a text box
    stats_text = (
        f"Average Max: {overall_max_avg:.2f}%\n"
        f"Median Max: {game_max_df['max_visibility'].median():.2f}%\n"
        f"Min of Max: {game_max_df['max_visibility'].min():.2f}%\n"
        f"Max of Max: {game_max_df['max_visibility'].max():.2f}%\n"
        f"Range: {game_max_df['max_visibility'].max() - game_max_df['max_visibility'].min():.2f}%"
    )
    
    plt.figtext(0.15, 0.02, stats_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Maximum robot visibility histogram saved to {save_path}")
    else:
        plt.show()
    
    plt.close()
    
    return game_max_df df.copy()
    title_suffix = ""
    
    if event_filter is not None:
        filtered_df = filtered_df[filtered_df['event'] == event_filter]
        title_suffix = f" - Event: {event_filter}"
    
    if filtered_df.empty:
        print("No data available after applying filters.")
        return
    
    # Step 1: Extract the base game name (removing half identifiers)
    filtered_df['base_game_name'] = filtered_df['game_name'].str.replace(r'_half\d+

# Function to create a comprehensive analysis of ball visibility
def analyze_ball_visibility(df, output_dir=None):
    """
    Perform a comprehensive analysis of ball visibility data with multiple visualizations
    """
    if output_dir and not output_dir.endswith('/'):
        output_dir += '/'
    
    # Make sure output directory exists
    if output_dir:
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    # 1. Overall player visibility histogram (all games)
    player_vis_path = f"{output_dir}player_visibility_all_games.png" if output_dir else None
    plot_player_visibility_histogram(df, save_path=player_vis_path)
    
    # 2. Game visibility histogram (average per game)
    game_vis_path = f"{output_dir}game_visibility.png" if output_dir else None
    plot_game_visibility_histogram(df, save_path=game_vis_path)
    
    # 3. Combined game halves histogram (whole games)
    combined_game_path = f"{output_dir}combined_game_halves_visibility.png" if output_dir else None
    plot_combined_game_halves_histogram(df, save_path=combined_game_path)
    
    # 4. Maximum robot visibility per game
    max_robot_path = f"{output_dir}max_robot_visibility.png" if output_dir else None
    max_robot_data = plot_max_robot_visibility_histogram(df, save_path=max_robot_path)
    
    # 5. Minimum robot visibility per game
    min_robot_path = f"{output_dir}min_robot_visibility.png" if output_dir else None
    min_robot_data = plot_min_robot_visibility_histogram(df, save_path=min_robot_path)
    
    # 6. Second worst robot visibility per game
    second_min_robot_path = f"{output_dir}second_min_robot_visibility.png" if output_dir else None
    second_min_robot_data = plot_second_min_robot_visibility_histogram(df, save_path=second_min_robot_path)
    
    # 7. Event-specific analysis
    events = df['event'].unique()
    for event in events:
        # Skip if there are too few records for this event
        event_df = df[df['event'] == event]
        if len(event_df) < 3:
            continue
            
        # Create event-specific player visibility histogram
        event_player_path = f"{output_dir}player_visibility_event_{event}.png" if output_dir else None
        plot_player_visibility_histogram(df, event_filter=event, save_path=event_player_path)
        
        # Create event-specific game visibility histogram
        event_game_path = f"{output_dir}game_visibility_event_{event}.png" if output_dir else None
        plot_game_visibility_histogram(df, event_filter=event, save_path=event_game_path)
        
        # Create event-specific combined halves histogram
        event_combined_path = f"{output_dir}combined_halves_event_{event}.png" if output_dir else None
        plot_combined_game_halves_histogram(df, event_filter=event, save_path=event_combined_path)
        
        # Create event-specific max robot histogram
        event_max_robot_path = f"{output_dir}max_robot_event_{event}.png" if output_dir else None
        plot_max_robot_visibility_histogram(df, event_filter=event, save_path=event_max_robot_path)
        
        # Create event-specific min robot histogram
        event_min_robot_path = f"{output_dir}min_robot_event_{event}.png" if output_dir else None
        plot_min_robot_visibility_histogram(df, event_filter=event, save_path=event_min_robot_path)
        
        # Create event-specific second-worst robot histogram
        event_second_min_path = f"{output_dir}second_min_robot_event_{event}.png" if output_dir else None
        plot_second_min_robot_visibility_histogram(df, event_filter=event, save_path=event_second_min_path)
    
    # 8. Game-specific player visibility (for each game)
    games = df[['game_id', 'game_name']].drop_duplicates().values
    for game_id, game_name in games:
        # Skip if there are too few records for this game
        game_df = df[df['game_id'] == game_id]
        if len(game_df) < 3:
            continue
            
        # Create game-specific player visibility histogram
        game_player_path = f"{output_dir}player_visibility_game_{game_id}.png" if output_dir else None
        plot_player_visibility_histogram(df, game_filter=game_id, save_path=game_player_path)
    
    # 9. Summary statistics
    print("\n=== BALL VISIBILITY ANALYSIS SUMMARY ===")
    print(f"Total records analyzed: {len(df)}")
    print(f"Number of unique games: {df['game_id'].nunique()}")
    print(f"Number of unique events: {df['event'].nunique()}")
    
    # Overall statistics
    avg_visibility = df['knows_true_percent'].mean()
    median_visibility = df['knows_true_percent'].median()
    min_visibility = df['knows_true_percent'].min()
    max_visibility = df['knows_true_percent'].max()
    
    print("\nOverall Ball Visibility Statistics:")
    print(f"Average: {avg_visibility:.2f}%")
    print(f"Median: {median_visibility:.2f}%")
    print(f"Minimum: {min_visibility:.2f}%")
    print(f"Maximum: {max_visibility:.2f}%")
    print(f"Range: {max_visibility - min_visibility:.2f}%")
    
    # Stats by player
    print("\nBall Visibility by Player:")
    player_stats = df.groupby('player')['knows_true_percent'].agg(['mean', 'median', 'min', 'max', 'count']).reset_index()
    player_stats = player_stats.sort_values('mean', ascending=False)  # Sort descending by mean visibility
    
    for _, row in player_stats.iterrows():
        print(f"Player {row['player']}: Avg={row['mean']:.2f}%, Median={row['median']:.2f}%, Min={row['min']:.2f}%, Max={row['max']:.2f}%, Games={int(row['count'])}")
    
    # Find best performing player and game
    best_player = player_stats.iloc[0]
    print(f"\nBest performing player: Player {best_player['player']} (Avg: {best_player['mean']:.2f}%)")
    
    # Game stats
    game_stats = df.groupby(['game_id', 'game_name'])['knows_true_percent'].mean().reset_index()
    game_stats = game_stats.sort_values('knows_true_percent', ascending=False)  # Sort descending
    best_game = game_stats.iloc[0]
    print(f"Best performing game: {best_game['game_name']} (ID: {best_game['game_id']}, Avg: {best_game['knows_true_percent']:.2f}%)")
    
    # Max robot stats
    if max_robot_data is not None:
        print("\nBest Robots per Game:")
        for _, row in max_robot_data.head(5).iterrows():
            print(f"Game: {row['game_name']} (ID: {row['game_id']}) - Player {row['top_player']} achieved {row['max_visibility']:.2f}%")
    
    # Min robot stats
    if min_robot_data is not None:
        print("\nWorst Robots per Game:")
        for _, row in min_robot_data.head(5).iterrows():
            print(f"Game: {row['game_name']} (ID: {row['game_id']}) - Player {row['worst_player']} had only {row['min_visibility']:.2f}%")
    
    # Second-worst robot stats
    if second_min_robot_data is not None:
        print("\nSecond-Worst Robots per Game:")
        for _, row in second_min_robot_data.head(5).iterrows():
            print(f"Game: {row['game_name']} (ID: {row['game_id']}) - Player {row['second_worst_player']} had {row['second_min_visibility']:.2f}%")
    
    # Analyze patterns in best/worst robots
    if max_robot_data is not None and min_robot_data is not None:
        print("\nAnalyzing Robot Performance Patterns:")
        
        # Count occurrences of each player as best/worst
        best_players = max_robot_data['top_player'].value_counts()
        worst_players = min_robot_data['worst_player'].value_counts()
        
        print("Players with highest frequency as best performer:")
        for player, count in best_players.head(3).items():
            print(f"Player {player}: Best in {count} games")
        
        print("\nPlayers with highest frequency as worst performer:")
        for player, count in worst_players.head(3).items():
            print(f"Player {player}: Worst in {count} games")
        
        # Check if there are consistent patterns in the data
        print("\nTeam size analysis:")
        team_sizes = df.groupby(['game_id', 'game_name'])['player'].nunique().reset_index()
        team_sizes.columns = ['game_id', 'game_name', 'team_size']
        print(f"Games with 5 robots: {len(team_sizes[team_sizes['team_size'] == 5])}")
        print(f"Games with 7 robots: {len(team_sizes[team_sizes['team_size'] == 7])}")
        
        # Compare performance between 5-robot and 7-robot teams
        if len(team_sizes[team_sizes['team_size'] == 5]) > 0 and len(team_sizes[team_sizes['team_size'] == 7]) > 0:
            team5_games = team_sizes[team_sizes['team_size'] == 5]['game_id'].tolist()
            team7_games = team_sizes[team_sizes['team_size'] == 7]['game_id'].tolist()
            
            team5_data = df[df['game_id'].isin(team5_games)]
            team7_data = df[df['game_id'].isin(team7_games)]
            
            team5_avg = team5_data['knows_true_percent'].mean()
            team7_avg = team7_data['knows_true_percent'].mean()
            
            print(f"\nAverage visibility in 5-robot teams: {team5_avg:.2f}%")
            print(f"Average visibility in 7-robot teams: {team7_avg:.2f}%")
            print(f"Difference: {abs(team5_avg - team7_avg):.2f}%")
            
    # Return all dataframes for further analysis if needed
    return {
        'raw_data': df,
        'max_robot_data': max_robot_data,
        'min_robot_data': min_robot_data,
        'second_min_robot_data': second_min_robot_data
    } Median={row['median']:.2f}%, Min={row['min']:.2f}%, Max={row['max']:.2f}%, Games={int(row['count'])}")
    
    # Find best performing player and game
    best_player = player_stats.iloc[0]
    print(f"\nBest performing player: Player {best_player['player']} (Avg: {best_player['mean']:.2f}%)")
    
    # Game stats
    game_stats = df.groupby(['game_id', 'game_name'])['knows_true_percent'].mean().reset_index()
    game_stats = game_stats.sort_values('knows_true_percent', ascending=False)  # Sort descending
    best_game = game_stats.iloc[0]
    print(f"Best performing game: {best_game['game_name']} (ID: {best_game['game_id']}, Avg: {best_game['knows_true_percent']:.2f}%)")
    
    # Max robot stats
    if max_robot_data is not None:
        print("\nBest Robots per Game:")
        for _, row in max_robot_data.head(5).iterrows():
            print(f"Game: {row['game_name']} (ID: {row['game_id']}) - Player {row['top_player']} achieved {row['max_visibility']:.2f}%")
    
    return df
    
    # 5. Summary statistics
    print("\n=== BALL VISIBILITY ANALYSIS SUMMARY ===")
    print(f"Total records analyzed: {len(df)}")
    print(f"Number of unique games: {df['game_id'].nunique()}")
    print(f"Number of unique events: {df['event'].nunique()}")
    
    # Overall statistics
    avg_visibility = df['knows_true_percent'].mean()
    median_visibility = df['knows_true_percent'].median()
    min_visibility = df['knows_true_percent'].min()
    max_visibility = df['knows_true_percent'].max()
    
    print("\nOverall Ball Visibility Statistics:")
    print(f"Average: {avg_visibility:.2f}%")
    print(f"Median: {median_visibility:.2f}%")
    print(f"Minimum: {min_visibility:.2f}%")
    print(f"Maximum: {max_visibility:.2f}%")
    print(f"Range: {max_visibility - min_visibility:.2f}%")
    
    # Stats by player
    print("\nBall Visibility by Player:")
    player_stats = df.groupby('player')['knows_true_percent'].agg(['mean', 'median', 'min', 'max', 'count']).reset_index()
    for _, row in player_stats.iterrows():
        print(f"Player {row['player']}: Avg={row['mean']:.2f}%, Median={row['median']:.2f}%, Min={row['min']:.2f}%, Max={row['max']:.2f}%, Games={int(row['count'])}")
    
    # Find best performing player and game
    best_player = player_stats.loc[player_stats['mean'].idxmax()]
    print(f"\nBest performing player: Player {best_player['player']} (Avg: {best_player['mean']:.2f}%)")
    
    # Game stats
    game_stats = df.groupby(['game_id', 'game_name'])['knows_true_percent'].mean().reset_index()
    best_game = game_stats.loc[game_stats['knows_true_percent'].idxmax()]
    print(f"Best performing game: {best_game['game_name']} (ID: {best_game['game_id']}, Avg: {best_game['knows_true_percent']:.2f}%)")

# Example usage
def main():
    # Define path to your CSV file with ball visibility data
    csv_file = "overall_ball_detection_summary.csv"  # Update this path to your local file
    output_dir = "ball_visibility_analysis/"  # Output directory for saving visualizations
    
    # Load the data
    ball_data = load_ball_visibility_data(csv_file)
    
    # Create visualizations and analysis
    analyze_ball_visibility(ball_data, output_dir)
    
    # If you want to create a specific visualization:
    # plot_player_visibility_histogram(ball_data, game_filter=17)
    # plot_game_visibility_histogram(ball_data)

if __name__ == "__main__":
    main()
, '', regex=True)
    
    # Step 2: Group by the base game name and player to get average across halves
    complete_games_df = filtered_df.groupby(['base_game_name', 'player'])['knows_true_percent'].mean().reset_index()
    
    # Step 3: Now average across all players for each complete game
    game_avg = complete_games_df.groupby('base_game_name')['knows_true_percent'].mean().reset_index()
    
    # Count number of players per game for reference
    player_counts = complete_games_df.groupby('base_game_name').size().reset_index()
    player_counts.columns = ['base_game_name', 'player_count']
    
    # Merge player counts with game averages
    game_avg = pd.merge(game_avg, player_counts, on='base_game_name')
    
    # Sort by average visibility for better visualization
    game_avg = game_avg.sort_values('knows_true_percent', ascending=False)
    
    # Create the visualization
    plt.figure(figsize=(14, 8))
    
    # Create the game visibility bar chart with a different color palette
    ax = sns.barplot(x='base_game_name', y='knows_true_percent', data=game_avg, palette='viridis')
    
    # Calculate and plot the overall average line
    overall_avg = game_avg['knows_true_percent'].mean()
    plt.axhline(y=overall_avg, color='orange', linestyle='--', label=f'Overall Avg: {overall_avg:.2f}%')
    
    # Add value labels on top of each bar
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        ax.text(p.get_x() + p.get_width()/2., 
                height + 1,
                f'{height:.2f}%\n({game_avg.iloc[i]["player_count"]} players)', 
                ha="center", fontsize=9, rotation=0)
    
    # Set labels and title
    plt.title(f'Average Ball Visibility per Complete Game (Combined Halves){title_suffix}', fontsize=14)
    plt.xlabel('Game', fontsize=12)
    plt.ylabel('Average Ball Visibility (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, max(game_avg['knows_true_percent']) * 1.15)  # Add space for labels
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Add stats in a text box
    stats_text = (
        f"Overall Average: {overall_avg:.2f}%\n"
        f"Median: {game_avg['knows_true_percent'].median():.2f}%\n"
        f"Min: {game_avg['knows_true_percent'].min():.2f}%\n"
        f"Max: {game_avg['knows_true_percent'].max():.2f}%\n"
        f"Range: {game_avg['knows_true_percent'].max() - game_avg['knows_true_percent'].min():.2f}%\n"
        f"Total Games: {len(game_avg)}"
    )
    
    plt.figtext(0.15, 0.02, stats_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Combined game halves visibility histogram saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

# Function to create a comprehensive analysis of ball visibility
def analyze_ball_visibility(df, output_dir=None):
    """
    Perform a comprehensive analysis of ball visibility data with multiple visualizations
    """
    if output_dir and not output_dir.endswith('/'):
        output_dir += '/'
    
    # 1. Overall player visibility histogram (all games)
    player_vis_path = f"{output_dir}player_visibility_all_games.png" if output_dir else None
    plot_player_visibility_histogram(df, save_path=player_vis_path)
    
    # 2. Game visibility histogram (average per game)
    game_vis_path = f"{output_dir}game_visibility.png" if output_dir else None
    plot_game_visibility_histogram(df, save_path=game_vis_path)
    
    # 3. Event-specific analysis
    events = df['event'].unique()
    for event in events:
        # Skip if there are too few records for this event
        event_df = df[df['event'] == event]
        if len(event_df) < 3:
            continue
            
        # Create event-specific player visibility histogram
        event_player_path = f"{output_dir}player_visibility_event_{event}.png" if output_dir else None
        plot_player_visibility_histogram(df, event_filter=event, save_path=event_player_path)
        
        # Create event-specific game visibility histogram
        event_game_path = f"{output_dir}game_visibility_event_{event}.png" if output_dir else None
        plot_game_visibility_histogram(df, event_filter=event, save_path=event_game_path)
    
    # 4. Game-specific player visibility (for each game)
    games = df[['game_id', 'game_name']].drop_duplicates().values
    for game_id, game_name in games:
        # Skip if there are too few records for this game
        game_df = df[df['game_id'] == game_id]
        if len(game_df) < 3:
            continue
            
        # Create game-specific player visibility histogram
        game_player_path = f"{output_dir}player_visibility_game_{game_id}.png" if output_dir else None
        plot_player_visibility_histogram(df, game_filter=game_id, save_path=game_player_path)
    
    # 5. Summary statistics
    print("\n=== BALL VISIBILITY ANALYSIS SUMMARY ===")
    print(f"Total records analyzed: {len(df)}")
    print(f"Number of unique games: {df['game_id'].nunique()}")
    print(f"Number of unique events: {df['event'].nunique()}")
    
    # Overall statistics
    avg_visibility = df['knows_true_percent'].mean()
    median_visibility = df['knows_true_percent'].median()
    min_visibility = df['knows_true_percent'].min()
    max_visibility = df['knows_true_percent'].max()
    
    print("\nOverall Ball Visibility Statistics:")
    print(f"Average: {avg_visibility:.2f}%")
    print(f"Median: {median_visibility:.2f}%")
    print(f"Minimum: {min_visibility:.2f}%")
    print(f"Maximum: {max_visibility:.2f}%")
    print(f"Range: {max_visibility - min_visibility:.2f}%")
    
    # Stats by player
    print("\nBall Visibility by Player:")
    player_stats = df.groupby('player')['knows_true_percent'].agg(['mean', 'median', 'min', 'max', 'count']).reset_index()
    for _, row in player_stats.iterrows():
        print(f"Player {row['player']}: Avg={row['mean']:.2f}%, Median={row['median']:.2f}%, Min={row['min']:.2f}%, Max={row['max']:.2f}%, Games={int(row['count'])}")
    
    # Find best performing player and game
    best_player = player_stats.loc[player_stats['mean'].idxmax()]
    print(f"\nBest performing player: Player {best_player['player']} (Avg: {best_player['mean']:.2f}%)")
    
    # Game stats
    game_stats = df.groupby(['game_id', 'game_name'])['knows_true_percent'].mean().reset_index()
    best_game = game_stats.loc[game_stats['knows_true_percent'].idxmax()]
    print(f"Best performing game: {best_game['game_name']} (ID: {best_game['game_id']}, Avg: {best_game['knows_true_percent']:.2f}%)")

# Example usage
def main():
    # Define path to your CSV file with ball visibility data
    csv_file = "overall_ball_detection_summary.csv"  # Update this path to your local file
    output_dir = "ball_visibility_analysis/"  # Output directory for saving visualizations
    
    # Load the data
    ball_data = load_ball_visibility_data(csv_file)
    
    # Create visualizations and analysis
    analyze_ball_visibility(ball_data, output_dir)
    
    # If you want to create a specific visualization:
    # plot_player_visibility_histogram(ball_data, game_filter=17)
    # plot_game_visibility_histogram(ball_data)

if __name__ == "__main__":
    main()