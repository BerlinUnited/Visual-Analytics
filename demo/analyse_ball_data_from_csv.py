import pandas as pd
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
    
    # Create the visualization
    plt.figure(figsize=(12, 8))
    
    # Create the player visibility bar chart
    ax = sns.barplot(x='player', y='knows_true_percent', data=filtered_df, palette='Blues_d')
    
    # Calculate and plot the average line
    avg_visibility = filtered_df['knows_true_percent'].mean()
    plt.axhline(y=avg_visibility, color='orange', linestyle='--', label=f'Average: {avg_visibility:.2f}%')
    
    # Add value labels on top of each bar
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        ax.text(p.get_x() + p.get_width()/2., 
                height + 1,
                f'{height:.2f}%', 
                ha="center", fontsize=10)
    
    # Set labels and title
    plt.title(f'Ball Visibility per Player{title_suffix}', fontsize=14)
    plt.xlabel('Player', fontsize=12)
    plt.ylabel('Ball Visibility (%)', fontsize=12)
    plt.ylim(0, max(filtered_df['knows_true_percent']) * 1.15)  # Add space for labels
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Add stats in a text box
    stats_text = (
        f"Average: {avg_visibility:.2f}%\n"
        f"Median: {filtered_df['knows_true_percent'].median():.2f}%\n"
        f"Min: {filtered_df['knows_true_percent'].min():.2f}%\n"
        f"Max: {filtered_df['knows_true_percent'].max():.2f}%\n"
        f"Range: {filtered_df['knows_true_percent'].max() - filtered_df['knows_true_percent'].min():.2f}%"
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
    
    # Calculate average visibility per game
    game_avg = filtered_df.groupby(['game_id', 'game_name'])['knows_true_percent'].mean().reset_index()
    game_avg['game_label'] = game_avg['game_name'] + " (ID: " + game_avg['game_id'].astype(str) + ")"
    
    # Sort by average visibility for better visualization
    game_avg = game_avg.sort_values('knows_true_percent', ascending=False)
    
    # Create the visualization
    plt.figure(figsize=(14, 8))
    
    # Create the game visibility bar chart
    ax = sns.barplot(x='game_label', y='knows_true_percent', data=game_avg, palette='Blues_d')
    
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