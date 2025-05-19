import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from vaapi.client import Vaapi


class LogTimeAnalyzer:
    """
    Analyzes logs to determine if they belong to the same game based on duration.
    """
    def __init__(self, client):
        self.client = client
        self.threshold_minutes = 5  # Threshold in minutes to determine if logs are part of same game
        self.fps = 25  # Default frames per second
        self.output_dir = "log_time_analysis"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def fetch_ball_data_for_log(self, log_id):
        """Retrieve ball detection data for a specific log ID"""
        print(f"Retrieving ball model data for log_id: {log_id}")
        
        try:
            response = self.client.ballmodel.list(log_id=log_id)
            
            if response and len(response) > 0:
                print(f"Retrieved {len(response)} ball detection entries for log ID {log_id}")
                return response
            else:
                print(f"No ball detection data retrieved for log ID {log_id}")
                return []
        except Exception as e:
            print(f"Error retrieving data for log ID {log_id}: {e}")
            return []
    
    def get_log_info(self, log_id):
        """Get basic log information"""
        try:
            log_info = self.client.logs.get(log_id)
            return {
                'id': log_info.id,
                'game': log_info.game,
                'event_name': log_info.event_name,
                'game_name': log_info.game_name,
                'player_number': log_info.player_number
            }
        except Exception as e:
            print(f"Error retrieving log info for log ID {log_id}: {e}")
            return None
    
    def analyze_log_duration(self, log_id):
        """Analyze the duration of a specific log based on frame count"""
        ball_data = self.fetch_ball_data_for_log(log_id)
        log_info = self.get_log_info(log_id)
        
        if not ball_data:
            print(f"No data available for log ID {log_id}")
            return {
                'log_id': log_id,
                'frame_count': 0,
                'duration_seconds': 0,
                'duration_minutes': 0,
                'log_info': log_info
            }
            
        # Extract all frame numbers
        frames = []
        for entry in ball_data:
            if hasattr(entry, 'frame'):
                frames.append(entry.frame)
            elif isinstance(entry, dict) and 'frame' in entry:
                frames.append(entry['frame'])
                
        if not frames:
            print(f"No valid frames found in log ID {log_id}")
            return {
                'log_id': log_id,
                'frame_count': 0,
                'duration_seconds': 0,
                'duration_minutes': 0,
                'log_info': log_info
            }
                
        # Calculate statistics
        frame_count = len(frames)
        min_frame = min(frames)
        max_frame = max(frames)
        frame_range = max_frame - min_frame + 1  # +1 because inclusive range
        
        # Calculate duration in seconds and minutes
        duration_seconds = frame_range / self.fps
        duration_minutes = duration_seconds / 60
        
        print(f"\nLog ID {log_id} Analysis:")
        print(f"Frame count: {frame_count}")
        print(f"Frame range: {min_frame} to {max_frame} ({frame_range} frames)")
        print(f"Duration: {duration_seconds:.2f} seconds ({duration_minutes:.2f} minutes)")
        
        return {
            'log_id': log_id,
            'frame_count': frame_count,
            'frame_range': frame_range,
            'min_frame': min_frame,
            'max_frame': max_frame,
            'duration_seconds': duration_seconds,
            'duration_minutes': duration_minutes,
            'log_info': log_info
        }
    
    def analyze_game_logs(self, game_id_list, event_name=None):
        """
        Analyze all logs for a list of game IDs to identify if they're part of same game
        
        Parameters:
        - game_id_list: list of game IDs to analyze
        - event_name: optional filter by event name
        """
        print(f"\n==== ANALYZING LOGS FOR GAMES: {game_id_list} ====")
        
        # Fetch all logs
        try:
            all_logs = self.client.logs.list()
        except Exception as e:
            print(f"Error fetching logs: {e}")
            return
        
        # Filter logs by game ID and optionally by event
        game_logs = []
        for log in all_logs:
            if log.game in game_id_list and (event_name is None or log.event_name == event_name):
                game_logs.append({
                    'id': log.id,
                    'game': log.game,
                    'event_name': log.event_name,
                    'game_name': log.game_name,
                    'player_number': log.player_number
                })
        
        # Group logs by game ID
        logs_by_game = {}
        for log in game_logs:
            game_id = log['game']
            if game_id not in logs_by_game:
                logs_by_game[game_id] = []
            logs_by_game[game_id].append(log)
            
        # Print summary of logs found
        print(f"\nFound {len(game_logs)} logs for {len(logs_by_game)} games:")
        for game_id, logs in logs_by_game.items():
            sample_log = logs[0]
            print(f"- Game ID {game_id}: {sample_log['game_name']} - Event: {sample_log['event_name']} - {len(logs)} logs")
            
        # Analyze each log
        results = []
        for game_id, logs in logs_by_game.items():
            print(f"\n---- Analyzing Game ID: {game_id} ----")
            
            for log in logs:
                log_id = log['id']
                result = self.analyze_log_duration(log_id)
                results.append(result)
                
        # Save and display results
        self.save_results(results)
        return results
                
    def analyze_specific_logs(self, log_ids):
        """Analyze specific log IDs"""
        print(f"\n==== ANALYZING SPECIFIC LOGS: {log_ids} ====")
        
        results = []
        for log_id in log_ids:
            result = self.analyze_log_duration(log_id)
            results.append(result)
            
        # Save and display results
        self.save_results(results)
        return results
    
    def find_related_games(self, event_name, game_name_filter=None):
        """
        Find related games within an event that might be part of the same match
        
        Parameters:
        - event_name: Name of the event to search
        - game_name_filter: Optional filter to look for specific game names
        """
        print(f"\n==== FINDING RELATED GAMES IN EVENT: {event_name} ====")
        
        # Fetch all logs
        try:
            all_logs = self.client.logs.list()
        except Exception as e:
            print(f"Error fetching logs: {e}")
            return []
            
        # Filter logs by event and game name
        event_logs = []
        for log in all_logs:
            if log.event_name == event_name:
                if game_name_filter is None or game_name_filter in log.game_name:
                    event_logs.append({
                        'id': log.id,
                        'game': log.game,
                        'event_name': log.event_name,
                        'game_name': log.game_name,
                        'player_number': log.player_number
                    })
                    
        # Group logs by game name
        game_name_groups = {}
        for log in event_logs:
            game_name = log['game_name']
            if game_name not in game_name_groups:
                game_name_groups[game_name] = []
            game_name_groups[game_name].append(log)
            
        # Further group by game ID
        all_game_groups = []
        for game_name, logs in sorted(game_name_groups.items()):
            print(f"\n## Game: {game_name}")
            
            # Group by game ID
            game_id_groups = {}
            for log in logs:
                game_id = log['game']
                if game_id not in game_id_groups:
                    game_id_groups[game_id] = []
                game_id_groups[game_id].append(log)
                
            # Print each game ID group
            for game_id, game_logs in sorted(game_id_groups.items()):
                print(f"  Game ID: {game_id} - {len(game_logs)} logs")
                
                # Print each log
                for log in sorted(game_logs, key=lambda x: x['player_number']):
                    print(f"    Log ID: {log['id']} | Player: {log['player_number']}")
                    
            # Add to the master list of game groups
            for game_id, logs in game_id_groups.items():
                all_game_groups.append({
                    'game_name': game_name,
                    'game_id': game_id,
                    'logs': logs
                })
                
        return all_game_groups
    
    def analyze_matching_game_pairs(self, event_name, game_name_pattern=None):
        """
        Find and analyze pairs of games that might be the same match
        
        Parameters:
        - event_name: Name of the event to search
        - game_name_pattern: Optional filter pattern for game names
        """
        print(f"\n==== ANALYZING MATCHING GAME PAIRS IN EVENT: {event_name} ====")
        
        # Get all game groups
        game_groups = self.find_related_games(event_name, game_name_pattern)
        
        # Group by similar game names (e.g., same match, different halves)
        game_name_base_groups = {}
        
        # Use regex to identify base game names (removing "_half1", "_half2", etc.)
        import re
        
        for group in game_groups:
            # Extract base game name
            game_name = group['game_name']
            base_name_match = re.match(r'^(.+?)(?:_half\d+|_part\d+|_\d+)?$', game_name)
            
            if base_name_match:
                base_name = base_name_match.group(1)
            else:
                base_name = game_name
                
            if base_name not in game_name_base_groups:
                game_name_base_groups[base_name] = []
            
            game_name_base_groups[base_name].append(group)
            
        # Find game pairs that might be related
        potential_pairs = []
        
        for base_name, groups in game_name_base_groups.items():
            if len(groups) > 1:
                print(f"\n## Potential match: {base_name}")
                for group in groups:
                    print(f"  - {group['game_name']} (Game ID: {group['game_id']})")
                
                # Add all possible pairs in this group
                for i in range(len(groups)):
                    for j in range(i+1, len(groups)):
                        potential_pairs.append((groups[i], groups[j]))
        
        # Analyze each potential pair
        all_results = []
        
        for pair in potential_pairs:
            group1, group2 = pair
            print(f"\n==== ANALYZING POTENTIAL PAIR ====")
            print(f"Group 1: {group1['game_name']} (Game ID: {group1['game_id']})")
            print(f"Group 2: {group2['game_name']} (Game ID: {group2['game_id']})")
            
            # Get player 1 logs from each group (or the first player available)
            log1 = next((log for log in group1['logs'] if log['player_number'] == 1), group1['logs'][0])
            log2 = next((log for log in group2['logs'] if log['player_number'] == 1), group2['logs'][0])
            
            # Analyze these specific logs
            result1 = self.analyze_log_duration(log1['id'])
            result2 = self.analyze_log_duration(log2['id'])
            
            # Determine if they're part of the same game based on duration
            combined_minutes = result1['duration_minutes'] + result2['duration_minutes']
            is_same_game = (result1['duration_minutes'] < self.threshold_minutes or 
                           result2['duration_minutes'] < self.threshold_minutes)
            
            pair_result = {
                'group1': group1,
                'group2': group2,
                'log1': log1,
                'log2': log2,
                'result1': result1,
                'result2': result2,
                'combined_minutes': combined_minutes,
                'is_same_game': is_same_game
            }
            
            all_results.append(pair_result)
            
            # Print analysis result
            print(f"\nResult:")
            print(f"Log ID {result1['log_id']} duration: {result1['duration_minutes']:.2f} minutes")
            print(f"Log ID {result2['log_id']} duration: {result2['duration_minutes']:.2f} minutes")
            print(f"Combined duration: {combined_minutes:.2f} minutes")
            print(f"Are they part of the same game? {'YES' if is_same_game else 'NO'}")
            
        # Generate and save a report
        self.generate_matching_pairs_report(all_results, event_name)
        
        return all_results
    
    def generate_matching_pairs_report(self, results, event_name):
        """Generate a report of matching game pairs"""
        report_path = os.path.join(self.output_dir, f"{event_name}_matching_pairs_report.txt")
        csv_path = os.path.join(self.output_dir, f"{event_name}_matching_pairs_report.csv")
        
        # Create lists for tabulate and dataframe
        table_data = []
        df_data = []
        
        for result in results:
            g1_name = result['group1']['game_name']
            g1_id = result['group1']['game_id']
            g2_name = result['group2']['game_name']
            g2_id = result['group2']['game_id']
            
            duration1 = result['result1']['duration_minutes']
            duration2 = result['result2']['duration_minutes']
            combined = result['combined_minutes']
            same_game = "YES" if result['is_same_game'] else "NO"
            
            recommendation = "Analyze together" if result['is_same_game'] else "Analyze separately"
            
            # Add to table data
            table_data.append([
                g1_name, g1_id, 
                g2_name, g2_id,
                f"{duration1:.2f}", f"{duration2:.2f}", f"{combined:.2f}",
                same_game, recommendation
            ])
            
            # Add to dataframe data
            df_data.append({
                'Game1_Name': g1_name,
                'Game1_ID': g1_id,
                'Game1_LogID': result['log1']['id'],
                'Game1_Duration': duration1,
                'Game2_Name': g2_name,
                'Game2_ID': g2_id,
                'Game2_LogID': result['log2']['id'],
                'Game2_Duration': duration2,
                'Combined_Duration': combined,
                'Same_Game': result['is_same_game'],
                'Recommendation': recommendation
            })
        
        # Create pretty text report
        headers = [
            "Game 1 Name", "Game 1 ID", 
            "Game 2 Name", "Game 2 ID",
            "Duration 1 (min)", "Duration 2 (min)", "Combined (min)",
            "Same Game?", "Recommendation"
        ]
        
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        
        with open(report_path, 'w') as f:
            f.write(f"# Matching Game Pairs Analysis for Event: {event_name}\n\n")
            f.write(f"Analysis performed on: {pd.Timestamp.now()}\n")
            f.write(f"Duration threshold for same game: {self.threshold_minutes} minutes\n\n")
            f.write(table)
            f.write("\n\nRecommendations:\n")
            f.write("- 'Analyze together' means these logs should be considered parts of the same game\n")
            f.write("- 'Analyze separately' means these are likely different games\n")
        
        # Create CSV report
        df = pd.DataFrame(df_data)
        df.to_csv(csv_path, index=False)
        
        print(f"\nGenerated matching pairs report: {report_path}")
        print(f"Generated CSV report: {csv_path}")
        
        # Create visualization
        self.visualize_game_durations(df_data, event_name)
    
    def visualize_game_durations(self, df_data, event_name):
        """Create visualizations of game durations"""
        if not df_data:
            return
            
        plt.figure(figsize=(12, 8))
        
        # Convert data for plotting
        pairs = []
        durations1 = []
        durations2 = []
        combined = []
        is_same = []
        
        for item in df_data:
            pair_name = f"{item['Game1_Name']} + {item['Game2_Name']}"
            pairs.append(pair_name)
            durations1.append(item['Game1_Duration'])
            durations2.append(item['Game2_Duration'])
            combined.append(item['Combined_Duration'])
            is_same.append(item['Same_Game'])
        
        # Shortened labels for the x-axis
        short_labels = [f"Pair {i+1}" for i in range(len(pairs))]
        
        # Create a grouped bar chart
        x = np.arange(len(pairs))
        width = 0.25
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Plot bars
        rects1 = ax.bar(x - width, durations1, width, label='Game 1 Duration', color='skyblue')
        rects2 = ax.bar(x, durations2, width, label='Game 2 Duration', color='lightgreen')
        rects3 = ax.bar(x + width, combined, width, label='Combined Duration', color='salmon')
        
        # Draw threshold line
        ax.axhline(y=self.threshold_minutes, color='red', linestyle='--', 
                   label=f'Threshold ({self.threshold_minutes} min)')
        
        # Add text annotations for the same/different game classification
        for i, val in enumerate(is_same):
            color = 'green' if val else 'red'
            text = "SAME GAME" if val else "DIFF GAME"
            ax.annotate(text, 
                       xy=(i, max(durations1[i], durations2[i]) + 0.5),
                       ha='center', va='bottom',
                       color=color, fontweight='bold')
        
        # Add labels, title and custom x-axis tick labels
        ax.set_xlabel('Game Pairs')
        ax.set_ylabel('Duration (minutes)')
        ax.set_title(f'Game Duration Analysis for Event: {event_name}')
        ax.set_xticks(x)
        ax.set_xticklabels(short_labels)
        ax.legend()
        
        # Add a table at the bottom with the full names
        the_table = plt.table(cellText=[[pair] for pair in pairs],
                              colLabels=["Full Game Pair Names"],
                              loc='bottom',
                              bbox=[0, -0.50, 1, 0.3])
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(9)
        the_table.scale(1, 1.5)
        
        # Adjust layout
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout(rect=[0, 0.3, 1, 1])
        
        # Save figure
        plot_path = os.path.join(self.output_dir, f"{event_name}_game_durations.png")
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Generated visualization: {plot_path}")
        
    def save_results(self, results):
        """Save analysis results to files"""
        if not results:
            print("No results to save")
            return
            
        # Create a DataFrame
        data = []
        for result in results:
            log_info = result.get('log_info', {})
            
            data.append({
                'log_id': result['log_id'],
                'game_id': log_info.get('game', 'Unknown'),
                'event_name': log_info.get('event_name', 'Unknown'),
                'game_name': log_info.get('game_name', 'Unknown'),
                'player_number': log_info.get('player_number', 'Unknown'),
                'frame_count': result.get('frame_count', 0),
                'frame_range': result.get('frame_range', 0),
                'duration_seconds': result.get('duration_seconds', 0),
                'duration_minutes': result.get('duration_minutes', 0)
            })
            
        df = pd.DataFrame(data)
        
        # Save to CSV
        csv_file = os.path.join(self.output_dir, "log_time_analysis.csv")
        df.to_csv(csv_file, index=False)
        print(f"\nSaved analysis results to {csv_file}")
        
        # Create a pretty text report
        report_file = os.path.join(self.output_dir, "log_time_analysis_report.txt")
        
        with open(report_file, 'w') as f:
            f.write("===============================================\n")
            f.write("              LOG TIME ANALYSIS               \n")
            f.write("===============================================\n\n")
            
            f.write(f"Analysis Date: {pd.Timestamp.now()}\n")
            f.write(f"FPS Used for Calculations: {self.fps}\n")
            f.write(f"Same-Game Threshold: {self.threshold_minutes} minutes\n\n")
            
            # Group by game ID
            games = df.groupby(['game_id', 'game_name'])
            
            for (game_id, game_name), game_logs in games:
                f.write(f"\n==== GAME: {game_name} (ID: {game_id}) ====\n\n")
                
                table_data = []
                for _, row in game_logs.iterrows():
                    table_data.append([
                        row['log_id'],
                        row['player_number'],
                        row['frame_count'],
                        row['frame_range'],
                        f"{row['duration_seconds']:.2f}",
                        f"{row['duration_minutes']:.2f}"
                    ])
                
                headers = ["Log ID", "Player", "Frame Count", "Frame Range", 
                          "Duration (sec)", "Duration (min)"]
                          
                table = tabulate(table_data, headers=headers, tablefmt="grid")
                f.write(table)
                f.write("\n")
                
                # Check if this might be an incomplete game
                if game_logs['duration_minutes'].max() < self.threshold_minutes:
                    f.write(f"\nNOTE: All logs in this game have durations less than {self.threshold_minutes} minutes!\n")
                    f.write("This may indicate the game was interrupted or is part of a multi-part game.\n")
                    f.write("Consider analyzing it together with another game of the same name.\n\n")
        
        print(f"Generated detailed report: {report_file}")
        
        # Create visualizations
        self.create_duration_visualizations(df)
    
    def create_duration_visualizations(self, df):
        """Create visualizations of log durations"""
        # Create a bar chart of durations by game ID
        plt.figure(figsize=(12, 8))
        
        # Group by game
        game_groups = df.groupby(['game_id', 'game_name'])
        
        # Set up plot data
        game_labels = []
        player_durations = {}
        
        for (game_id, game_name), game_df in game_groups:
            game_labels.append(f"{game_name}\n(ID: {game_id})")
            
            # Group by player
            for player, player_df in game_df.groupby('player_number'):
                player_key = f"Player {player}"
                if player_key not in player_durations:
                    player_durations[player_key] = []
                
                # Get the duration for this player in this game
                duration = player_df['duration_minutes'].values[0]
                player_durations[player_key].append(duration)
                
                # Pad other players' lists if they don't have a value for this game
                for p_key in player_durations:
                    if p_key != player_key and len(player_durations[p_key]) < len(game_labels):
                        player_durations[p_key].append(0)
        
        # Plot the data
        fig, ax = plt.subplots(figsize=(14, 8))
        
        x = np.arange(len(game_labels))
        width = 0.15  # width of bars
        multiplier = 0
        
        # Plot each player's durations
        for player, durations in player_durations.items():
            # Ensure all player lists have the same length
            while len(durations) < len(game_labels):
                durations.append(0)
                
            offset = width * multiplier
            rects = ax.bar(x + offset, durations, width, label=player)
            multiplier += 1
        
        # Add threshold line
        ax.axhline(y=self.threshold_minutes, color='red', linestyle='--', 
                  label=f'Threshold ({self.threshold_minutes} min)')
        
        # Add labels, title and legend
        ax.set_ylabel('Duration (minutes)')
        ax.set_title('Log Durations by Game and Player')
        ax.set_xticks(x + width * (len(player_durations) - 1) / 2)
        ax.set_xticklabels(game_labels)
        ax.legend(loc='upper left')
        
        plt.tight_layout()
        
        # Save the figure
        duration_plot = os.path.join(self.output_dir, "log_durations.png")
        plt.savefig(duration_plot, dpi=300)
        plt.close()
        
        print(f"Generated duration visualization: {duration_plot}")


def main():
    # Initialize client (must set environment variables)
    print("Initializing client...")
    api_url = os.environ.get("VAT_API_URL")
    api_token = os.environ.get("VAT_API_TOKEN")
    
    if not api_url or not api_token:
        print("Error: Environment variables VAT_API_URL and VAT_API_TOKEN must be set")
        return
    
    try:
        client = Vaapi(
            base_url=api_url,
            api_key=api_token,
        )
        print("Client initialized successfully")
    except Exception as e:
        print(f"Error initializing client: {e}")
        return
    
    # Create analyzer
    analyzer = LogTimeAnalyzer(client)
    
    # Example usage
    event_name = "2025-03-12-GO25"
    
    # Find all potentially related games in this event
    #print("\n--- LOOKING FOR POTENTIALLY RELATED GAMES ---")
    #analyzer.analyze_matching_game_pairs(event_name)
    
    # You can also analyze specific logs or game IDs
    #print("\n--- EXAMPLE: ANALYZING SPECIFIC GAME IDS ---")
    #analyzer.analyze_game_logs([90, 97], event_name)
    
    #print("\n--- EXAMPLE: ANALYZING SPECIFIC LOG IDS ---")
    analyzer.analyze_specific_logs([76, 83])  # First player logs from half 1
    
    print("\nAnalysis complete. Check the log_time_analysis directory for reports.")


if __name__ == "__main__":
    main()