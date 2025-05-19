import csv
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict
from itertools import groupby
import datetime
import sys
from io import StringIO
import re
import pandas as pd
from vaapi.client import Vaapi


# Class to organize log data
class LogOrganizer:
    def __init__(self, client):
        self.client = client
        self.logs_data = []
        self.sorted_logs = []
        self.dataframe = None
    
    def fetch_logs(self):
        """Fetch all logs from the API and organize them"""
        print("Fetching logs...")
        response = self.client.logs.list()
        
        # Convert logs to dictionaries for easier handling
        for log in response:
            log_dict = {
                'id': log.id,
                'game': log.game,
                'event_name': log.event_name,
                'game_name': log.game_name,
                'player_number': log.player_number
            }
            self.logs_data.append(log_dict)
        
        print(f"Retrieved {len(self.logs_data)} logs")
        return self.logs_data
    
    def sort_logs(self, sort_by='event_name'):
        """
        Sort logs by specified field(s)
        
        Parameters:
        - sort_by: field or list of fields to sort by
        """
        if isinstance(sort_by, str):
            sort_by = [sort_by]
        
        self.sorted_logs = sorted(self.logs_data, key=lambda x: [x[field] for field in sort_by])
        return self.sorted_logs
    
    def filter_logs(self, **filters):
        """
        Filter logs based on key-value pairs
        
        Example:
        filter_logs(event_name='2025-03-12-GO25', player_number=1)
        """
        filtered = self.logs_data
        
        for key, value in filters.items():
            filtered = [log for log in filtered if str(log.get(key, '')) == str(value)]
        
        return filtered
    
    def to_dataframe(self):
        """Convert logs to pandas DataFrame for more advanced analysis"""
        if not self.logs_data:
            self.fetch_logs()
        
        self.dataframe = pd.DataFrame(self.logs_data)
        return self.dataframe
    
    def save_to_csv(self, filepath="logs_inventory.csv"):
        """Save the logs data to a CSV file"""
        if self.dataframe is None:
            self.to_dataframe()
        
        self.dataframe.to_csv(filepath, index=False)
        print(f"Saved logs inventory to {filepath}")
        return filepath
    
    def group_by_event(self):
        """Group logs by event name and return as dictionary"""
        if self.dataframe is None:
            self.to_dataframe()
        
        grouped = self.dataframe.groupby('event_name')
        events = {}
        
        for name, group in grouped:
            events[name] = group.to_dict('records')
        
        return events
        
    def group_by_game(self):
        """Group logs by game ID and return as dictionary"""
        if self.dataframe is None:
            self.to_dataframe()
        
        # Group by both event name and game ID to distinguish games with same names
        grouped = self.dataframe.groupby(['event_name', 'game'])
        games = {}
        
        for (event_name, game_id), group in grouped:
            key = f"{event_name}_{game_id}"
            games[key] = group.to_dict('records')
        
        return games
    
    def get_game_context(self, log_id):
        """Get detailed game context for a specific log ID"""
        log_info = self.get_log_info(log_id)
        if not log_info:
            return "Unknown Context"
        
        event = log_info.get('event_name', 'Unknown')
        game_name = log_info.get('game_name', 'Unknown')
        game_id = log_info.get('game', 'Unknown')
        player = log_info.get('player_number', 'Unknown')
        
        return {
            'event': event,
            'game_name': game_name,
            'game_id': game_id,
            'player': player,
            'display': f"{event} - {game_name} (ID: {game_id}) - Player {player}"
        }
    
    def print_organized_logs(self):
        """Print logs in an organized, easy-to-read format"""
        if not self.sorted_logs:
            # Sort by event, game_name, game ID, and then player_number for consistent grouping
            self.sort_logs(['event_name', 'game_name', 'game', 'player_number'])
        
        current_event = None
        current_game_name = None
        current_game_id_set = set()
        
        print("\n=== ORGANIZED LOGS INVENTORY ===")
        
        # First, group logs by event and game name
        event_game_groups = {}
        for log in self.sorted_logs:
            event = log['event_name']
            game_name = log['game_name']
            
            if event not in event_game_groups:
                event_game_groups[event] = {}
            
            if game_name not in event_game_groups[event]:
                event_game_groups[event][game_name] = []
            
            event_game_groups[event][game_name].append(log)
        
        # Now output the organized logs
        for event, games in sorted(event_game_groups.items()):
            print(f"\n## EVENT: {event}")
            
            for game_name, logs in sorted(games.items()):
                # Group by game ID within same game name
                game_id_groups = {}
                for log in logs:
                    game_id = log['game']
                    if game_id not in game_id_groups:
                        game_id_groups[game_id] = []
                    game_id_groups[game_id].append(log)
                
                # Print each game with its IDs clearly separated
                print(f"\n  GAME: {game_name}")
                
                for game_id, game_logs in sorted(game_id_groups.items()):
                    print(f"    Game ID: {game_id} - Event: {event}")
                    
                    # Sort logs by player number within each game ID
                    sorted_game_logs = sorted(game_logs, key=lambda x: x['player_number'])
                    
                    for log in sorted_game_logs:
                        print(f"      Log ID: {log['id']} | Player: {log['player_number']} | Event: {log['event_name']}")
    
    def get_log_info(self, log_id):
        """Get information for a specific log ID"""
        for log in self.logs_data:
            if log['id'] == log_id:
                return log
        return None


# Enhanced analysis class with game context
class BallDetectionAnalyzer:
    def __init__(self, client, log_organizer):
        self.client = client
        self.log_organizer = log_organizer
        self.current_log_id = None
        self.current_log_info = None
        self.output_folder = None
        self.log_capture = None
    
    def setup_analysis(self, log_id):
        """Set up for analysis of a specific log ID"""
        self.current_log_id = log_id
        
        # Get log information
        self.current_log_info = self.log_organizer.get_log_info(log_id)
        if not self.current_log_info:
            print(f"Error: Log ID {log_id} not found. Run log_organizer.fetch_logs() first.")
            return False
        
        # Create output folder
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"ball_detection_{log_id}_{timestamp}"
        
        # Add event and game info to folder name
        if self.current_log_info:
            event = self.current_log_info.get('event_name', '').replace('/', '_')
            game = self.current_log_info.get('game_name', '').replace('/', '_')
            player = self.current_log_info.get('player_number', '')
            folder_name = f"ball_detection_{event}_{game}_player{player}_{timestamp}"
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Created output folder: {folder_name}")
        
        self.output_folder = folder_name
        
        # Setup log capture
        self.log_capture = LogCapture()
        
        return True
    
    def get_log_data(self):
        """Retrieve ball detection logs from the API"""
        print(f"Retrieving ball model data for log_id: {self.current_log_id}")
        response = self.client.ballmodel.list(
            log_id=self.current_log_id,
        )
        
        # Print summary of response
        if response and len(response) > 0:
            print(f"Retrieved {len(response)} ball detection entries")
        else:
            print("No ball detection data retrieved from API")
        
        # Save the response to a JSON file
        json_file = os.path.join(self.output_folder, "ball_detection_data.json")
        self.save_to_json(response, json_file)
        
        return response
    
    def analyze_ball_detection(self, log_data):
        """Analyze ball detection data from the logs"""
        print("\n---- ANALYZING BALL DETECTION DATA ----")
        
        # Extract frame numbers and ball detection status
        frames = []
        knows_ball = []
        
        for entry in log_data:
            try:
                # Handle both dictionary and object format
                if isinstance(entry, dict):
                    # Handle JSON dictionary format
                    frame = entry.get('frame')
                    rep_data = entry.get('representation_data', {})
                    knows = rep_data.get('knows', False)
                else:
                    # Handle object format - try both attribute access and dictionary access
                    frame = getattr(entry, 'frame', None)
                    
                    # First try to get representation_data as attribute
                    rep_data = getattr(entry, 'representation_data', None)
                    
                    # If rep_data is a dictionary, get 'knows' directly
                    if isinstance(rep_data, dict):
                        knows = rep_data.get('knows', False)
                    # If rep_data is an object, try to get 'knows' as attribute
                    elif rep_data is not None:
                        knows = getattr(rep_data, 'knows', False)
                    else:
                        knows = False
                
                frames.append(frame)
                knows_ball.append(knows)
            except Exception as e:
                print(f"Error processing entry: {e}")
                continue
        
        # Create numpy arrays for easier processing
        frames = np.array(frames)
        knows_ball = np.array(knows_ball)
        
        # Count occurrences of True and False
        true_count = np.sum(knows_ball)
        false_count = len(knows_ball) - true_count
        
        # Calculate percentage of frames where ball is detected
        total_frames = len(knows_ball)
        detection_percentage = (true_count / total_frames) * 100 if total_frames > 0 else 0
        
        print(f"\nBall Detection Analysis:")
        print(f"Total frames analyzed: {total_frames}")
        print(f"Ball detected (knows=True): {true_count} frames ({detection_percentage:.2f}%)")
        print(f"Ball not detected (knows=False): {false_count} frames ({100-detection_percentage:.2f}%)")
        
        return frames, knows_ball
    
    def plot_ball_detection(self, frames, knows_ball):
        """Create a visualization of ball detection over time with game context"""
        print("\n---- CREATING BALL DETECTION TIMELINE PLOT ----")
        
        if len(frames) == 0:
            print("No valid frames to plot")
            return
        
        # Get game context for the title
        context_title = self.get_context_title()
        
        plt.figure(figsize=(12, 6))
        
        # Convert boolean array to integers (1 for True, 0 for False)
        knows_int = knows_ball.astype(int)
        
        # Plot the detection status over frames - use step plot to clearly show True/False transitions
        plt.step(frames, knows_int, 'b-', where='post', linewidth=1.0)
        
        # Add horizontal lines at 0 and 1 for reference
        plt.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
        plt.axhline(y=1, color='gray', linestyle='-', alpha=0.3)
        
        # Set labels and title with context
        plt.xlabel('Frame Number')
        plt.ylabel('Ball Detection Status')
        plt.title(f'Ball Detection Over Time\n{context_title}')
        plt.yticks([0, 1], ['Not Detected', 'Detected'])
        
        # Add grid for better readability
        plt.grid(True, alpha=0.3)
        
        # Ensure y-axis limits give some padding
        plt.ylim(-0.1, 1.1)
        
        # Add detection percentage to the plot
        true_percentage = (np.sum(knows_ball) / len(knows_ball)) * 100
        plt.figtext(0.01, 0.01, f"Detection rate: {true_percentage:.2f}%", 
                   ha="left", fontsize=9, 
                   bbox={"facecolor":"white", "alpha":0.8, "pad":5})
        
        plt.tight_layout()
        output_path = os.path.join(self.output_folder, 'ball_detection_timeline.png')
        plt.savefig(output_path)
        plt.close()
        print(f"Saved timeline plot to {output_path}")
    
    def plot_ball_detection_histogram(self, knows_ball):
        """Create a histogram of ball detection status (True/False counts) with game context"""
        print("\n---- CREATING BALL DETECTION HISTOGRAM ----")
        
        if len(knows_ball) == 0:
            print("No valid data for histogram")
            return
        
        # Get game context for the title
        context_title = self.get_context_title()
        
        # Count True and False values
        true_count = np.sum(knows_ball)
        false_count = len(knows_ball) - true_count
        
        # Calculate percentages
        total = len(knows_ball)
        true_percent = (true_count / total) * 100
        false_percent = (false_count / total) * 100
        
        # Create the histogram
        plt.figure(figsize=(10, 6))
        
        # Plot the bars
        labels = ['Detected (True)', 'Not Detected (False)']
        counts = [true_count, false_count]
        colors = ['#3498db', '#e74c3c']  # Blue for detected, red for not detected
        
        bars = plt.bar(labels, counts, color=colors)
        
        # Add count values on top of the bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')
        
        # Add percentage labels
        plt.text(0, true_count/2, f'{true_percent:.1f}%', ha='center', va='center', color='white', fontweight='bold')
        plt.text(1, false_count/2, f'{false_percent:.1f}%', ha='center', va='center', color='white', fontweight='bold')
        
        # Set labels and title with context
        plt.ylabel('Count')
        plt.title(f'Ball Detection Status Distribution\n{context_title}')
        plt.grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_folder, 'ball_detection_histogram.png')
        plt.savefig(output_path)
        plt.close()
        print(f"Saved histogram to {output_path}")
    
    def plot_consecutive_runs(self, frames, knows_ball):
        """Create a visualization of consecutive runs with game context"""
        print("\n---- CREATING CONSECUTIVE DETECTION RUNS PLOT ----")
        
        if len(frames) == 0 or len(knows_ball) == 0:
            print("No valid data for consecutive runs analysis")
            return
        
        # Get game context for the title
        context_title = self.get_context_title()
        
        # Find runs of consecutive values
        runs = []
        run_lengths = []
        run_start_frames = []
        run_values = []
        
        # Group consecutive values
        for value, group in groupby(zip(frames, knows_ball), key=lambda x: x[1]):
            group_list = list(group)
            run_length = len(group_list)
            start_frame = group_list[0][0]
            end_frame = group_list[-1][0]
            
            # Store the run details
            runs.append((start_frame, end_frame, value, run_length))
            run_lengths.append(run_length)
            run_start_frames.append(start_frame)
            run_values.append(value)
        
        # Print some statistics about the runs
        detected_runs = [length for length, value in zip(run_lengths, run_values) if value]
        not_detected_runs = [length for length, value in zip(run_lengths, run_values) if not value]
        
        print("\nConsecutive Run Analysis:")
        print(f"Total runs: {len(runs)}")
        print(f"Detected runs: {len(detected_runs)}")
        print(f"Not detected runs: {len(not_detected_runs)}")
        
        if detected_runs:
            print(f"Average length of 'detected' runs: {np.mean(detected_runs):.2f} frames")
            print(f"Longest 'detected' run: {max(detected_runs)} frames")
        
        if not_detected_runs:
            print(f"Average length of 'not detected' runs: {np.mean(not_detected_runs):.2f} frames")
            print(f"Longest 'not detected' run: {max(not_detected_runs)} frames")
        
        # Create the visualization
        plt.figure(figsize=(14, 8))  # Larger figure for better spacing
        
        # Add a clear explanation in the title
        plt.suptitle(f'Consecutive Ball Detection Status Runs\n{context_title}', fontsize=14)
        plt.figtext(0.5, 0.01, 
                    "Each horizontal line shows a different consecutive sequence of frames with the same detection status.\n"
                    "These sequences do NOT occur simultaneously - they are separate events arranged vertically for visualization.",
                    ha="center", fontsize=9, bbox={"facecolor":"white", "alpha":0.8, "pad":5})
        
        # Plot horizontal lines representing runs with more spacing between them
        for i, (start, end, value, length) in enumerate(runs):
            color = 'blue' if value else 'red'
            label = 'Detected' if value and i == 0 else ('Not Detected' if not value and (i == 0 or i == 1) else None)
            plt.plot([start, end], [i, i], color=color, linewidth=3, label=label)
            
            # Add text label with better positioning to avoid overlap
            if length > max(run_lengths) * 0.03:  # Only label significant runs
                plt.text(start + (end-start)/2, i, f'{length}', 
                         ha='center', va='center', fontsize=8, 
                         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))
        
        # Set labels and title with clearer explanation
        plt.xlabel('Frame Number (Timeline)')
        plt.ylabel('Sequence Index (Each row is a different time period)')
        
        # Improved legend
        legend = plt.legend(loc='lower right', title="Detection Status")
        legend.get_title().set_fontweight('bold')
        
        plt.grid(True, axis='x', alpha=0.3)
        plt.tight_layout(rect=[0, 0.07, 1, 0.95])  # Make room for the annotation
        
        output_path = os.path.join(self.output_folder, 'ball_detection_runs.png')
        plt.savefig(output_path)
        plt.close()
        print(f"Saved consecutive runs plot to {output_path}")
    
    def save_to_json(self, response_data, filename):
        """Save the response data to a JSON file"""
        print(f"\n---- SAVING DATA TO JSON: {filename} ----")
        
        # Convert the custom objects to a serializable format
        serializable_data = []
        
        # Process all entries
        for entry in response_data:
            try:
                # Use recursive function to convert the entire object to a dict
                entry_dict = self.object_to_dict(entry)
                serializable_data.append(entry_dict)
                
            except Exception as e:
                print(f"Error serializing entry: {e}")
                try:
                    simple_dict = {
                        'id': getattr(entry, 'id', None),
                        'frame': getattr(entry, 'frame', None),
                    }
                    serializable_data.append(simple_dict)
                except:
                    print("  Fallback serialization also failed")
        
        # Check for 'knows' values in the serialized data
        true_count = sum(1 for entry in serializable_data 
                         if entry.get('representation_data', {}).get('knows') is True)
        false_count = sum(1 for entry in serializable_data 
                          if entry.get('representation_data', {}).get('knows') is False)
        
        print(f"\nSerialized data check:")
        print(f"Total entries: {len(serializable_data)}")
        print(f"Entries with knows=True: {true_count}")
        print(f"Entries with knows=False: {false_count}")
        
        # Write to JSON file
        try:
            with open(filename, 'w') as f:
                json.dump(serializable_data, f, indent=2)
            print(f"Successfully saved {len(serializable_data)} entries to {filename}")
        except Exception as e:
            print(f"Error saving to JSON file: {e}")
    
    def object_to_dict(self, obj):
        """Convert a custom object to a dictionary recursively"""
        if obj is None:
            return None
        
        # Handle basic types that are already JSON serializable
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        
        # Handle lists and tuples
        if isinstance(obj, (list, tuple)):
            return [self.object_to_dict(item) for item in obj]
        
        # Handle dictionaries
        if isinstance(obj, dict):
            return {k: self.object_to_dict(v) for k, v in obj.items()}
        
        # Try to convert custom object to dict
        result = {}
        
        # First try using __dict__
        if hasattr(obj, '__dict__'):
            for key, value in obj.__dict__.items():
                # Skip private attributes
                if not key.startswith('_'):
                    result[key] = self.object_to_dict(value)
                    
        # If that didn't work or returned an empty dict, try accessing common attributes
        if not result and hasattr(obj, 'representation_data'):
            # Direct attribute access for common fields
            result['id'] = getattr(obj, 'id', None)
            result['frame'] = getattr(obj, 'frame', None)
            
            # Handle representation_data specially
            rep_data = getattr(obj, 'representation_data', None)
            if rep_data:
                if isinstance(rep_data, dict):
                    result['representation_data'] = rep_data
                else:
                    rep_dict = {}
                    # Try direct attribute access
                    rep_dict['knows'] = getattr(rep_data, 'knows', None)
                    rep_dict['valid'] = getattr(rep_data, 'valid', None)
                    
                    # Handle position dictionaries
                    for attr in ['position', 'positionPreview', 'speed']:
                        pos_obj = getattr(rep_data, attr, None)
                        if pos_obj:
                            pos_dict = {}
                            pos_dict['x'] = getattr(pos_obj, 'x', None)
                            pos_dict['y'] = getattr(pos_obj, 'y', None)
                            rep_dict[attr] = pos_dict
                    
                    result['representation_data'] = rep_dict
        
        # If still empty, try dir()
        if not result:
            for attr in dir(obj):
                # Skip methods and private attributes
                if not attr.startswith('_') and not callable(getattr(obj, attr)):
                    try:
                        result[attr] = self.object_to_dict(getattr(obj, attr))
                    except:
                        # Skip attributes that can't be accessed
                        pass
        
        return result
    
    def create_summary_file(self, log_text):
        """Create a concise summary text file with only key metrics and append to CSV"""
        summary_path = os.path.join(self.output_folder, 'analysis_summary.txt')
        
        # Extract key metrics from log text
        metrics = {}
        
        # Find total frames
        total_frames_match = re.search(r"Total frames analyzed: (\d+)", log_text)
        if total_frames_match:
            metrics["total_frames"] = int(total_frames_match.group(1))
        
        # Find detection counts and percentages
        knows_true_match = re.search(r"Ball detected \(knows=True\): (\d+) frames \((\d+\.\d+)%\)", log_text)
        if knows_true_match:
            metrics["knows_true_count"] = int(knows_true_match.group(1))
            metrics["knows_true_percent"] = float(knows_true_match.group(2))
        
        knows_false_match = re.search(r"Ball not detected \(knows=False\): (\d+) frames \((\d+\.\d+)%\)", log_text)
        if knows_false_match:
            metrics["knows_false_count"] = int(knows_false_match.group(1))
            metrics["knows_false_percent"] = float(knows_false_match.group(2))
        
        # Find run statistics
        total_runs_match = re.search(r"Total runs: (\d+)", log_text)
        if total_runs_match:
            metrics["total_runs"] = int(total_runs_match.group(1))
        
        detected_runs_match = re.search(r"Detected runs: (\d+)", log_text)
        if detected_runs_match:
            metrics["detected_runs"] = int(detected_runs_match.group(1))
        
        not_detected_runs_match = re.search(r"Not detected runs: (\d+)", log_text)
        if not_detected_runs_match:
            metrics["not_detected_runs"] = int(not_detected_runs_match.group(1))
        
        avg_detected_match = re.search(r"Average length of 'detected' runs: (\d+\.\d+)", log_text)
        if avg_detected_match:
            metrics["avg_detected_length"] = float(avg_detected_match.group(1))
        
        longest_detected_match = re.search(r"Longest 'detected' run: (\d+)", log_text)
        if longest_detected_match:
            metrics["longest_detected"] = int(longest_detected_match.group(1))
        
        avg_not_detected_match = re.search(r"Average length of 'not detected' runs: (\d+\.\d+)", log_text)
        if avg_not_detected_match:
            metrics["avg_not_detected_length"] = float(avg_not_detected_match.group(1))
        
        longest_not_detected_match = re.search(r"Longest 'not detected' run: (\d+)", log_text)
        if longest_not_detected_match:
            metrics["longest_not_detected"] = int(longest_not_detected_match.group(1))
        
        # Add game context to summary
        log_info = self.current_log_info or {}
        
        # Create a dictionary with all the summary data
        summary_data = {
            "log_id": self.current_log_id,
            "event": log_info.get('event_name', 'Unknown'),
            "game_name": log_info.get('game_name', 'Unknown'),
            "game_id": log_info.get('game', 'Unknown'),
            "player": log_info.get('player_number', 'Unknown'),
            "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_frames": metrics.get('total_frames', 'N/A'),
            "knows_true_count": metrics.get('knows_true_count', 'N/A'),
            "knows_true_percent": metrics.get('knows_true_percent', 'N/A'),
            "knows_false_count": metrics.get('knows_false_count', 'N/A'),
            "knows_false_percent": metrics.get('knows_false_percent', 'N/A'),
            "total_runs": metrics.get('total_runs', 'N/A'),
            "detected_runs": metrics.get('detected_runs', 'N/A'),
            "not_detected_runs": metrics.get('not_detected_runs', 'N/A'),
            "avg_detected_length": metrics.get('avg_detected_length', 'N/A'),
            "longest_detected": metrics.get('longest_detected', 'N/A'),
            "avg_not_detected_length": metrics.get('avg_not_detected_length', 'N/A'),
            "longest_not_detected": metrics.get('longest_not_detected', 'N/A')
        }
        
        # Write to text file
        with open(summary_path, 'w') as f:
            for key, value in summary_data.items():
                key_upper = key.upper()
                f.write(f"{key_upper}: {value}\n")
        
        # Append to CSV file - create overall_summary.csv in the script directory
        csv_path = "overall_ball_detection_summary.csv"
        is_new_file = not os.path.exists(csv_path)
        
        mode = 'w' if is_new_file else 'a'  # Write mode if new file, append mode if existing
        
        with open(csv_path, mode, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(summary_data.keys()))
            
            # Write header only for new file
            if is_new_file:
                writer.writeheader()
            
            # Write the data row
            writer.writerow(summary_data)
            
        print(f"Created concise summary file: {summary_path}")
        print(f"{'Created' if is_new_file else 'Updated'} overall summary CSV: {csv_path}")
        
        return summary_path
    
    def get_context_title(self):
        """Generate a context title for plots based on current log info"""
        if not self.current_log_info:
            return "Unknown Game"
        
        event = self.current_log_info.get('event_name', 'Unknown')
        game = self.current_log_info.get('game_name', 'Unknown')
        game_id = self.current_log_info.get('game', 'Unknown')
        player = self.current_log_info.get('player_number', 'Unknown')
        
        return f"{event} - {game} (Game ID: {game_id}) - Player {player}"
    
    def run_analysis(self, log_id):
        """Run the complete ball detection analysis workflow"""
        # Setup analysis environment
        if not self.setup_analysis(log_id):
            return False
        
        # Start log capture
        self.log_capture.start()
        
        try:
            # Get the game context for logging
            context_title = self.get_context_title()
            print(f"=== BALL DETECTION ANALYSIS ===")
            print(f"Log ID: {log_id}")
            print(f"Context: {context_title}")
            print(f"Output folder: {self.output_folder}")
            print(f"Started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Get the log data
            log_data = self.get_log_data()
            
            # Analyze the data
            frames, knows_ball = self.analyze_ball_detection(log_data)
            
            # Create visualizations with context
            self.plot_ball_detection(frames, knows_ball)
            self.plot_ball_detection_histogram(knows_ball)
            self.plot_consecutive_runs(frames, knows_ball)
            
            print("\nAnalysis complete. Files created in folder:", self.output_folder)
            
            return True
            
        except Exception as e:
            print(f"Error during analysis: {e}")
            return False
            
        finally:
            # Stop log capture
            self.log_capture.stop()
            
            # Create summary file with log output
            log_text = self.log_capture.get_log()
            summary_file = self.create_summary_file(log_text)
            
            print(f"\nAnalysis complete. Results saved to folder: {self.output_folder}")
            print(f"Summary file: {summary_file}")


# Log capture utility class
class LogCapture:
    """Utility class to capture console output"""
    def __init__(self):
        self.log_buffer = StringIO()
        self.original_stdout = sys.stdout
        self.log_file = None
    
    def start(self):
        """Start capturing stdout"""
        sys.stdout = self.log_buffer
    
    def stop(self):
        """Stop capturing and restore stdout"""
        sys.stdout = self.original_stdout
    
    def get_log(self):
        """Get the captured log content"""
        return self.log_buffer.getvalue()
    
    def save_log(self, file_path):
        """Save the log to a file"""
        with open(file_path, 'w') as f:
            f.write(self.get_log())
            print(f"Log saved to {file_path}")


# Main function to demonstrate usage
def main():
    # Initialize API client
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    
    # Initialize log organizer
    log_organizer = LogOrganizer(client)
    
    # Fetch and organize logs
    #log_organizer.fetch_logs()
    #log_organizer.sort_logs(['event_name', 'game_name', 'player_number'])
    
    # Print organized logs
    #log_organizer.print_organized_logs()
    
    # Save logs to CSV for easy viewing and sorting
    csv_path = log_organizer.save_to_csv()
    
    analyzer = BallDetectionAnalyzer(client, log_organizer)
    analyzer.run_analysis(268)

    # Prompt user to select a log for analysis
    print("\nYou can analyze a specific log by running:")
    print("analyzer = BallDetectionAnalyzer(client, log_organizer)")
    print("analyzer.run_analysis(log_id)")
    
    # Example of how to analyze a specific log
    print("\nExample usage:")
    print("# Analyze a specific log")
    print("analyzer = BallDetectionAnalyzer(client, log_organizer)")
    print("analyzer.run_analysis(264)  # Analyze log ID 264")
    
    # Example of how to analyze multiple logs
    print("\n# Analyze multiple logs")
    print("events = log_organizer.group_by_event()")
    print("target_event = '2025-03-12-GO25'")
    print("for log in events.get(target_event, []):")
    print("    analyzer.run_analysis(log['id'])")
    

if __name__ == "__main__":
    main()


"""
OUTPUT:
## EVENT: 2024-07-15_RC24

  GAME: BerlinUnited_vs_BHuman_half1
    Game ID: 17 - Event: 2024-07-15_RC24
      Log ID: 111 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 112 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 113 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 114 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 115 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 116 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 117 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_BHuman_half2
    Game ID: 18 - Event: 2024-07-15_RC24
      Log ID: 118 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 119 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 120 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 121 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 122 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 123 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 124 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_HTWK_Einlauftest
    Game ID: 21 - Event: 2024-07-15_RC24
      Log ID: 139 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 140 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 141 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 142 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 143 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 144 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 145 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_HTWK_half1
    Game ID: 22 - Event: 2024-07-15_RC24
      Log ID: 146 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 147 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 148 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 149 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 150 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 151 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 152 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_HTWK_half2
    Game ID: 23 - Event: 2024-07-15_RC24
      Log ID: 153 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 154 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 155 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 156 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 157 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 158 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 159 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_NaoDevils_half1
    Game ID: 6 - Event: 2024-07-15_RC24
      Log ID: 34 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 35 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 36 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 37 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 38 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 39 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 40 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_NaoDevils_half1-test
    Game ID: 26 - Event: 2024-07-15_RC24
      Log ID: 176 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 175 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 177 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 178 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 179 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 180 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 181 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 182 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_NaoDevils_half2
    Game ID: 7 - Event: 2024-07-15_RC24
      Log ID: 41 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 42 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 43 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 44 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 45 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 46 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 47 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_NaoDevils_half2-test
    Game ID: 27 - Event: 2024-07-15_RC24
      Log ID: 183 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 184 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 185 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 186 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 187 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 188 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 189 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_Nomadz_half1
    Game ID: 14 - Event: 2024-07-15_RC24
      Log ID: 90 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 91 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 92 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 93 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 94 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 95 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 96 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_Nomadz_half1-to
    Game ID: 15 - Event: 2024-07-15_RC24
      Log ID: 97 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 98 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 99 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 100 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 101 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 102 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 103 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_Nomadz_half2
    Game ID: 16 - Event: 2024-07-15_RC24
      Log ID: 104 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 105 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 106 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 107 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 108 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 109 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 110 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_Roboeirean_half1
    Game ID: 11 - Event: 2024-07-15_RC24
      Log ID: 69 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 70 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 71 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 72 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 73 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 74 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 75 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_Roboeirean_half2
    Game ID: 12 - Event: 2024-07-15_RC24
      Log ID: 76 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 77 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 78 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 79 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 80 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 81 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 82 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_Roboeirean_half2-to
    Game ID: 13 - Event: 2024-07-15_RC24
      Log ID: 83 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 84 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 85 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 86 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 87 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 88 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 89 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_Runswift_half1
    Game ID: 8 - Event: 2024-07-15_RC24
      Log ID: 48 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 49 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 50 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 51 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 52 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 53 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 54 | Player: 7 | Event: 2024-07-15_RC24
    Game ID: 24 - Event: 2024-07-15_RC24
      Log ID: 160 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 161 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 162 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 163 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 164 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 166 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 165 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 167 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_Runswift_half2
    Game ID: 9 - Event: 2024-07-15_RC24
      Log ID: 55 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 56 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 57 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 58 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 59 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 60 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 61 | Player: 7 | Event: 2024-07-15_RC24
    Game ID: 25 - Event: 2024-07-15_RC24
      Log ID: 168 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 169 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 170 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 171 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 172 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 173 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 174 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_Runswift_half2-to
    Game ID: 10 - Event: 2024-07-15_RC24
      Log ID: 62 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 63 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 64 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 65 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 66 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 67 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 68 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_SPQR_half1-test
    Game ID: 1 - Event: 2024-07-15_RC24
      Log ID: 1 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 2 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 3 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 4 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 5 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 6 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_SPQR_half2-test
    Game ID: 2 - Event: 2024-07-15_RC24
      Log ID: 7 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 8 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 9 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 10 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 11 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 12 | Player: 6 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_empty_half1-test
    Game ID: 3 - Event: 2024-07-15_RC24
      Log ID: 13 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 14 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 15 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 16 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 17 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 18 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 19 | Player: 7 | Event: 2024-07-15_RC24
    Game ID: 19 - Event: 2024-07-15_RC24
      Log ID: 125 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 126 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 127 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 128 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 129 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 130 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 131 | Player: 7 | Event: 2024-07-15_RC24

  GAME: BerlinUnited_vs_empty_half2-test
    Game ID: 20 - Event: 2024-07-15_RC24
      Log ID: 132 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 133 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 134 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 135 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 136 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 137 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 138 | Player: 7 | Event: 2024-07-15_RC24

  GAME: SPQR_vs_BerlinUnited_half1
    Game ID: 4 - Event: 2024-07-15_RC24
      Log ID: 20 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 21 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 22 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 23 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 24 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 25 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 26 | Player: 7 | Event: 2024-07-15_RC24

  GAME: SPQR_vs_BerlinUnited_half2
    Game ID: 5 - Event: 2024-07-15_RC24
      Log ID: 27 | Player: 1 | Event: 2024-07-15_RC24
      Log ID: 28 | Player: 2 | Event: 2024-07-15_RC24
      Log ID: 29 | Player: 3 | Event: 2024-07-15_RC24
      Log ID: 30 | Player: 4 | Event: 2024-07-15_RC24
      Log ID: 31 | Player: 5 | Event: 2024-07-15_RC24
      Log ID: 32 | Player: 6 | Event: 2024-07-15_RC24
      Log ID: 33 | Player: 7 | Event: 2024-07-15_RC24

## EVENT: 2025-03-12-GO25

  GAME: BerlinUnited_vs_BHuman_half1
    Game ID: 58 - Event: 2025-03-12-GO25
      Log ID: 245 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 246 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 247 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 248 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 249 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 250 | Player: 6 | Event: 2025-03-12-GO25
      Log ID: 251 | Player: 7 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_BHuman_half2
    Game ID: 59 - Event: 2025-03-12-GO25
      Log ID: 252 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 253 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 254 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 255 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 256 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 257 | Player: 6 | Event: 2025-03-12-GO25
      Log ID: 258 | Player: 7 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_Bembelbots_half1
    Game ID: 29 - Event: 2025-03-12-GO25
      Log ID: 191 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 196 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 197 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 198 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 199 | Player: 5 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_Bembelbots_half2
    Game ID: 33 - Event: 2025-03-12-GO25
      Log ID: 200 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 201 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 202 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 203 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 204 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 205 | Player: 6 | Event: 2025-03-12-GO25
      Log ID: 206 | Player: 7 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_DutchNaoTeam_half1
    Game ID: 38 - Event: 2025-03-12-GO25
      Log ID: 235 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 236 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 237 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 238 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 239 | Player: 5 | Event: 2025-03-12-GO25
    Game ID: 93 - Event: 2025-03-12-GO25
      Log ID: 259 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 260 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 261 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 262 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 263 | Player: 5 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_DutchNaoTeam_half2
    Game ID: 39 - Event: 2025-03-12-GO25
      Log ID: 240 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 241 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 242 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 243 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 244 | Player: 5 | Event: 2025-03-12-GO25
    Game ID: 94 - Event: 2025-03-12-GO25
      Log ID: 264 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 265 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 266 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 267 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 268 | Player: 5 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_HTWK_half1
    Game ID: 34 - Event: 2025-03-12-GO25
      Log ID: 207 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 208 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 209 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 210 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 211 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 212 | Player: 6 | Event: 2025-03-12-GO25
      Log ID: 213 | Player: 7 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_HTWK_half2
    Game ID: 35 - Event: 2025-03-12-GO25
      Log ID: 214 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 215 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 216 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 217 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 218 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 219 | Player: 6 | Event: 2025-03-12-GO25
      Log ID: 220 | Player: 7 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_Hulks_half1
    Game ID: 95 - Event: 2025-03-12-GO25
      Log ID: 269 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 270 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 271 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 272 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 273 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 274 | Player: 7 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_Hulks_half2
    Game ID: 96 - Event: 2025-03-12-GO25
      Log ID: 275 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 276 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 277 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 278 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 279 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 280 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 281 | Player: 6 | Event: 2025-03-12-GO25
      Log ID: 282 | Player: 7 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_NaoDevils_half1
    Game ID: 36 - Event: 2025-03-12-GO25
      Log ID: 221 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 222 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 223 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 224 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 225 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 226 | Player: 6 | Event: 2025-03-12-GO25
      Log ID: 227 | Player: 7 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_NaoDevils_half2
    Game ID: 37 - Event: 2025-03-12-GO25
      Log ID: 228 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 229 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 230 | Player: 3 | Event: 2025-03-12-GO25
      Log ID: 231 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 232 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 233 | Player: 6 | Event: 2025-03-12-GO25
      Log ID: 234 | Player: 7 | Event: 2025-03-12-GO25

  GAME: BerlinUnited_vs_empty_half1-test
    Game ID: 28 - Event: 2025-03-12-GO25
      Log ID: 190 | Player: 1 | Event: 2025-03-12-GO25
      Log ID: 192 | Player: 2 | Event: 2025-03-12-GO25
      Log ID: 193 | Player: 4 | Event: 2025-03-12-GO25
      Log ID: 194 | Player: 5 | Event: 2025-03-12-GO25
      Log ID: 195 | Player: 7 | Event: 2025-03-12-GO25
Saved logs inventory to logs_inventory.csv

You can analyze a specific log by running:
analyzer = BallDetectionAnalyzer(client, log_organizer)
analyzer.run_analysis(log_id)

Example usage:
# Analyze a specific log
analyzer = BallDetectionAnalyzer(client, log_organizer)
analyzer.run_analysis(264)  # Analyze log ID 264

# Analyze multiple logs
events = log_organizer.group_by_event()
target_event = '2025-03-12-GO25'
for log in events.get(target_event, []):
    analyzer.run_analysis(log['id'])
"""