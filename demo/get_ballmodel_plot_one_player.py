from vaapi.client import Vaapi
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from itertools import groupby
import datetime
import sys
from io import StringIO

LOG_ID = 3

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


def setup_output_folder(log_id):
    """Create output folder with timestamp and log ID"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"ball_detection_analysis_{log_id}_{timestamp}"
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created output folder: {folder_name}")
    
    return folder_name


def get_logs(log_id=30):
    """Retrieve ball detection logs from the API"""
    print(f"Retrieving logs for log_id: {log_id}")
    response = client.ballmodel.list(
        log_id=log_id,
    )
    
    # Print summary of response
    if response and len(response) > 0:
        print(f"Retrieved {len(response)} log entries")
        print(f"First response entry: {response[0]}")
        print(f"Response type: {type(response[0])}")
    else:
        print("No data retrieved from API")
    
    # Save the response to a JSON file
    json_file = os.path.join(output_folder, "ball_detection_data.json")
    save_to_json(response, json_file)
    
    return response


def analyze_ball_detection(log_data):
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


def validate_with_json(json_file):
    """
    Validate our data analysis by checking the JSON file directly
    This helps identify any issues in the data parsing
    """
    print("\n---- VALIDATING JSON DATA ----")
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Count True/False values in the JSON data
        true_count = 0
        false_count = 0
        missing_count = 0
        
        for entry in data:
            rep_data = entry.get('representation_data', {})
            knows = rep_data.get('knows', None)
            
            if knows is True:
                true_count += 1
            elif knows is False:
                false_count += 1
            else:
                missing_count += 1
        
        total = true_count + false_count + missing_count
        
        print(f"\nJSON File Validation ({json_file}):")
        print(f"Total entries: {total}")
        print(f"Entries with knows=True: {true_count} ({true_count/total*100:.2f}% if present)")
        print(f"Entries with knows=False: {false_count} ({false_count/total*100:.2f}% if present)")
        print(f"Entries with missing knows: {missing_count} ({missing_count/total*100:.2f}% if present)")
        
        return true_count > 0  # Return True if we found any 'knows=True' entries
        
    except Exception as e:
        print(f"Error validating JSON file: {e}")
        return False


def object_to_dict(obj):
    """
    Convert a custom object to a dictionary by extracting all its attributes.
    Works recursively on nested objects.
    """
    if obj is None:
        return None
    
    # Handle basic types that are already JSON serializable
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    
    # Handle lists and tuples
    if isinstance(obj, (list, tuple)):
        return [object_to_dict(item) for item in obj]
    
    # Handle dictionaries
    if isinstance(obj, dict):
        return {k: object_to_dict(v) for k, v in obj.items()}
    
    # Try to convert custom object to dict
    result = {}
    
    # First try using __dict__
    if hasattr(obj, '__dict__'):
        for key, value in obj.__dict__.items():
            # Skip private attributes
            if not key.startswith('_'):
                result[key] = object_to_dict(value)
                
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
                    result[attr] = object_to_dict(getattr(obj, attr))
                except:
                    # Skip attributes that can't be accessed
                    pass
    
    return result


def save_to_json(response_data, filename):
    """
    Save the response data to a JSON file by converting custom objects to dictionaries
    """
    print(f"\n---- SAVING DATA TO JSON: {filename} ----")
    
    # Convert the custom objects to a serializable format
    serializable_data = []
    
    # First, let's print details about one entry to help with debugging
    if response_data and len(response_data) > 0:
        print("\nDebugging data structure:")
        sample = response_data[0]
        print(f"Sample entry type: {type(sample)}")
        
        # Try different methods to see what works
        print("Available methods to access data:")
        if hasattr(sample, '__dict__'):
            print("- __dict__ is available")
        if hasattr(sample, 'to_dict'):
            print("- to_dict() method is available") 
        if hasattr(sample, 'as_dict'):  
            print("- as_dict() method is available")
    
    # Process all entries
    for entry in response_data:
        try:
            # Use our recursive function to convert the entire object to a dict
            entry_dict = object_to_dict(entry)
            serializable_data.append(entry_dict)
            
        except Exception as e:
            print(f"Error serializing entry: {e}")
            # Try a simpler approach as fallback
            try:
                simple_dict = {
                    'id': getattr(entry, 'id', None),
                    'frame': getattr(entry, 'frame', None),
                }
                serializable_data.append(simple_dict)
                print(f"  Used fallback serialization for entry {simple_dict['id']}")
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


def plot_ball_detection_histogram(knows_ball):
    """Create a histogram of ball detection status (True/False counts)"""
    print("\n---- CREATING BALL DETECTION HISTOGRAM ----")
    
    if len(knows_ball) == 0:
        print("No valid data for histogram")
        return
    
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
    
    # Set labels and title
    plt.ylabel('Count')
    plt.title('Ball Detection Status Distribution')
    plt.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(output_folder, 'ball_detection_histogram.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Saved histogram to {output_path}")
    

def plot_ball_detection(frames, knows_ball):
    """Create a visualization of ball detection over time"""
    print("\n---- CREATING BALL DETECTION TIMELINE PLOT ----")
    
    if len(frames) == 0:
        print("No valid frames to plot")
        return
        
    plt.figure(figsize=(12, 6))
    
    # Convert boolean array to integers (1 for True, 0 for False)
    knows_int = knows_ball.astype(int)
    
    # Plot the detection status over frames - use step plot to clearly show True/False transitions
    plt.step(frames, knows_int, 'b-', where='post', linewidth=1.0)
    
    # Add horizontal lines at 0 and 1 for reference
    plt.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    plt.axhline(y=1, color='gray', linestyle='-', alpha=0.3)
    
    # Set labels and title
    plt.xlabel('Frame Number')
    plt.ylabel('Ball Detection Status')
    plt.title('Ball Detection Over Time')
    plt.yticks([0, 1], ['Not Detected', 'Detected'])
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3)
    
    # Ensure y-axis limits give some padding
    plt.ylim(-0.1, 1.1)
    
    plt.tight_layout()
    output_path = os.path.join(output_folder, 'ball_detection_timeline.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Saved timeline plot to {output_path}")
      

def plot_simplified_consecutive_runs(frames, knows_ball):
    """
    Create a simpler visualization of ball detection runs.
    Instead of showing all runs as parallel lines, this shows:
    1. A single timeline with status changes
    2. Markers for run lengths at transition points
    """
    if len(frames) == 0 or len(knows_ball) == 0:
        print("No valid data for simplified run analysis")
        return
    
    # Find runs of consecutive values
    runs = []
    
    # Group consecutive values
    current_value = knows_ball[0]
    start_idx = 0
    
    for i in range(1, len(knows_ball)):
        if knows_ball[i] != current_value:
            # End of a run
            end_idx = i - 1
            run_length = end_idx - start_idx + 1
            runs.append((frames[start_idx], frames[end_idx], current_value, run_length))
            
            # Start new run
            start_idx = i
            current_value = knows_ball[i]
    
    # Add the last run
    if start_idx < len(knows_ball):
        end_idx = len(knows_ball) - 1
        run_length = end_idx - start_idx + 1
        runs.append((frames[start_idx], frames[end_idx], current_value, run_length))
    
    # Create the plot
    plt.figure(figsize=(14, 6))
    
    # Convert the status to 0/1 for plotting
    status = [1 if r[2] else 0 for r in runs]
    x_start = [r[0] for r in runs]
    x_end = [r[1] for r in runs]
    run_lengths = [r[3] for r in runs]
    
    # Plot the status as a step function
    for i in range(len(runs)):
        if i < len(runs) - 1:
            plt.hlines(status[i], x_start[i], x_end[i], colors='blue' if status[i] else 'red', linewidth=2)
            plt.vlines(x_end[i], status[i], status[i+1], colors='gray', linestyles='--', linewidth=1)
    
    # Add the last segment
    if runs:
        plt.hlines(status[-1], x_start[-1], x_end[-1], colors='blue' if status[-1] else 'red', linewidth=2)
    
    # Add text labels for run lengths
    for i, run in enumerate(runs):
        if run[3] > 100:  # Only label runs longer than 100 frames
            plt.text(run[0] + (run[1] - run[0])/2, status[i] + 0.1, 
                     f"{run[3]}", ha='center', va='bottom', fontsize=9,
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))
    
    # Set labels and title
    plt.xlabel('Frame Number')
    plt.ylabel('Ball Detection Status')
    plt.title('Simplified Ball Detection Status Timeline')
    plt.yticks([0, 1], ['Not Detected', 'Detected'])
    plt.grid(True, alpha=0.3)
    
    # Add a second plot showing a cumulative count of transitions
    plt.figure(figsize=(14, 6))
    
    # Calculate cumulative number of runs
    x_transitions = []
    y_run_count = []
    current_count = 1
    
    for i in range(len(runs)):
        # Start point of run
        if i == 0:
            x_transitions.append(x_start[i])
            y_run_count.append(current_count)
        
        # End point of run (transition point)
        if i < len(runs) - 1:
            x_transitions.append(x_end[i])
            y_run_count.append(current_count)
            
            # Start of next run
            current_count += 1
            x_transitions.append(x_start[i+1])
            y_run_count.append(current_count)
    
    # Add last point
    if runs:
        x_transitions.append(x_end[-1])
        y_run_count.append(current_count)
    
    # Plot the cumulative run count
    plt.step(x_transitions, y_run_count, where='post', color='green', linewidth=2)
    
    # Add markers at transition points
    plt.scatter(x_transitions, y_run_count, color='green', s=30, zorder=3)
    
    # Add status indicators
    for i, run in enumerate(runs):
        mid_x = run[0] + (run[1] - run[0])/2
        plt.text(mid_x, i+1 + 0.2, "Ball Detected" if run[2] else "No Ball", 
                 ha='center', va='bottom', fontsize=8, 
                 color='blue' if run[2] else 'red',
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))
        
        # Add run length
        if run[3] > 100:  # Only label runs longer than 100 frames
            plt.text(mid_x, i+1 - 0.2, f"{run[3]} frames", 
                     ha='center', va='top', fontsize=7,
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))
    
    # Set labels and title
    plt.xlabel('Frame Number')
    plt.ylabel('Cumulative Run Count')
    plt.title('Ball Detection Status Transitions (Cumulative Run Count)')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the plots
    plt.savefig(os.path.join(output_folder, 'ball_detection_status_timeline.png'))
    plt.savefig(os.path.join(output_folder, 'ball_detection_transitions.png'))
    
    print(f"Saved simplified plots to {output_folder}")
    plt.close('all')


def create_summary_file(log_id, output_folder, log_text):
    """Create a concise summary text file with only key metrics"""
    summary_path = os.path.join(output_folder, 'analysis_summary.txt')
    
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
    
    # Write concise summary
    with open(summary_path, 'w') as f:
        f.write(f"LOG_ID: {log_id}\n")
        f.write(f"DATE: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"TOTAL_FRAMES: {metrics.get('total_frames', 'N/A')}\n")
        f.write(f"KNOWS_TRUE_COUNT: {metrics.get('knows_true_count', 'N/A')}\n")
        f.write(f"KNOWS_TRUE_PERCENT: {metrics.get('knows_true_percent', 'N/A')}%\n")
        f.write(f"KNOWS_FALSE_COUNT: {metrics.get('knows_false_count', 'N/A')}\n")
        f.write(f"KNOWS_FALSE_PERCENT: {metrics.get('knows_false_percent', 'N/A')}%\n")
        f.write(f"TOTAL_RUNS: {metrics.get('total_runs', 'N/A')}\n")
        f.write(f"DETECTED_RUNS: {metrics.get('detected_runs', 'N/A')}\n")
        f.write(f"NOT_DETECTED_RUNS: {metrics.get('not_detected_runs', 'N/A')}\n")
        f.write(f"AVG_DETECTED_LENGTH: {metrics.get('avg_detected_length', 'N/A')}\n")
        f.write(f"LONGEST_DETECTED: {metrics.get('longest_detected', 'N/A')}\n")
        f.write(f"AVG_NOT_DETECTED_LENGTH: {metrics.get('avg_not_detected_length', 'N/A')}\n")
        f.write(f"LONGEST_NOT_DETECTED: {metrics.get('longest_not_detected', 'N/A')}\n")
    
    print(f"Created concise summary file: {summary_path}")
    return summary_path

def plot_improved_consecutive_runs(frames, knows_ball):
    """
    Create an improved visualization of consecutive runs with better axis labels
    and more space between runs to avoid overlapping text
    """
    if len(frames) == 0 or len(knows_ball) == 0:
        print("No valid data for consecutive runs analysis")
        return
    
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
    plt.suptitle('Consecutive Ball Detection Status Runs', fontsize=16)
    plt.figtext(0.5, 0.01, 
                "Each horizontal line shows a different consecutive sequence of frames with the same detection status.\n"
                "These sequences do NOT occur simultaneously - they are separate events arranged vertically for visualization.",
                ha="center", fontsize=10, bbox={"facecolor":"white", "alpha":0.8, "pad":5})
    
    # Plot horizontal lines representing runs with more spacing between them
    for i, (start, end, value, length) in enumerate(runs):
        color = 'blue' if value else 'red'
        label = 'Detected' if value and i == 0 else ('Not Detected' if not value and (i == 0 or i == 1) else None)
        plt.plot([start, end], [i, i], color=color, linewidth=3, label=label)
        
        # Add text label with better positioning to avoid overlap
        if length > max(run_lengths) * 0.03:  # Only label significant runs
            plt.text(start + (end-start)/2, i, f'{length}', 
                     ha='center', va='center', fontsize=9, 
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))
    
    # Set labels and title with clearer explanation
    plt.xlabel('Frame Number (Timeline)')
    plt.ylabel('Sequence Index (Each row is a different time period)')
    
    # Improved legend
    legend = plt.legend(loc='lower right', title="Detection Status")
    legend.get_title().set_fontweight('bold')
    
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout(rect=[0, 0.07, 1, 0.95])  # Make room for the annotation
    
    output_path = os.path.join(output_folder, 'improved_ball_detection_runs.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Saved improved consecutive runs plot to {output_path}")


def plot_side_by_side_comparison(frames, knows_ball):
    """
    Create a side by side comparison of different visualization approaches
    for the consecutive runs data
    """
    if len(frames) == 0 or len(knows_ball) == 0:
        print("No valid data for comparison analysis")
        return
    
    # Find runs of consecutive values (same as before)
    runs = []
    for value, group in groupby(zip(frames, knows_ball), key=lambda x: x[1]):
        group_list = list(group)
        run_length = len(group_list)
        start_frame = group_list[0][0]
        end_frame = group_list[-1][0]
        runs.append((start_frame, end_frame, value, run_length))
    
    # Create a figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Plot 1: Original stacked view (with better labels)
    for i, (start, end, value, length) in enumerate(runs):
        color = 'blue' if value else 'red'
        label = 'Detected' if value and i == 0 else ('Not Detected' if not value and i == 0 else None)
        ax1.plot([start, end], [i, i], color=color, linewidth=3, label=label)
        
        # Add text label for significant runs
        if length > max([r[3] for r in runs]) * 0.05:
            ax1.text(start + (end-start)/2, i, f'{length}', 
                     ha='center', va='bottom', fontsize=8)
    
    ax1.set_xlabel('Frame Number')
    ax1.set_ylabel('Sequence Index (Different time periods)')
    ax1.set_title('Stacked View of Detection Sequences')
    ax1.grid(True, axis='x', alpha=0.3)
    ax1.legend()
    
    # Plot 2: Timeline view
    # Convert boolean array to integers (1 for True, 0 for False)
    knows_int = knows_ball.astype(int)
    
    # Plot the detection status over frames
    ax2.step(frames, knows_int, 'b-', where='post', linewidth=1.5)
    
    # Add horizontal lines at 0 and 1 for reference
    ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax2.axhline(y=1, color='gray', linestyle='-', alpha=0.3)
    
    # Add annotations for long runs
    for start, end, value, length in runs:
        if length > max([r[3] for r in runs]) * 0.1:  # Only label very significant runs
            y_pos = 1 if value else 0
            ax2.annotate(f'{length}', 
                         xy=((start + end)/2, y_pos),
                         xytext=((start + end)/2, y_pos + 0.2 if value else y_pos - 0.2),
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='gray'),
                         ha='center', va='center', fontsize=8,
                         bbox=dict(boxstyle="round,pad=0.3", fc='white', alpha=0.8))
    
    ax2.set_xlabel('Frame Number')
    ax2.set_ylabel('Ball Detection Status')
    ax2.set_title('Timeline View of Ball Detection')
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Not Detected', 'Detected'])
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.3, 1.3)  # Give more space for annotations
    
    # Add an explanation of the two different views
    plt.figtext(0.5, 0.01, 
                "Left: Each horizontal line represents a different sequence of frames with consistent detection status.\n"
                "Right: The same data shown as a timeline, with status changes indicated by steps up or down.",
                ha="center", fontsize=10, bbox={"facecolor":"white", "alpha":0.8, "pad":5})
    
    plt.tight_layout(rect=[0, 0.07, 1, 0.95])  # Make room for the annotation
    output_path = os.path.join(output_folder, 'ball_detection_comparison.png')
    plt.savefig(output_path)
    plt.close()
    
    print(f"Saved side-by-side comparison plot to {output_path}")

if __name__ == "__main__":
    # Don't forget to add import re at the top of the file for regex matching
    import re
    
    # Set the log ID (default to 30 if not specified)
    log_id = LOG_ID

    # Create output folder
    output_folder = setup_output_folder(log_id)
    
    # Initialize log capture
    log_capture = LogCapture()
    log_capture.start()
    
    try:
        print(f"=== BALL DETECTION ANALYSIS FOR LOG ID: {log_id} ===")
        print(f"Output folder: {output_folder}")
        print(f"Started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Initialize API client
        client = Vaapi(
            base_url=os.environ.get("VAT_API_URL"),
            api_key=os.environ.get("VAT_API_TOKEN"),
        )
        
        # Get the log data and save to JSON
        log_data = get_logs(log_id)
        
        # Validate the data from the JSON file
        json_file = os.path.join(output_folder, "ball_detection_data.json")
        if os.path.exists(json_file):
            json_has_true_values = validate_with_json(json_file)
            if json_has_true_values:
                print("\nJSON file contains 'knows=True' values, confirming data is present in the source.")
        
        # Analyze the data
        frames, knows_ball = analyze_ball_detection(log_data)
        
        # Create visualizations
        plot_ball_detection(frames, knows_ball)
        plot_ball_detection_histogram(knows_ball)
        plot_simplified_consecutive_runs(frames, knows_ball)
        plot_improved_consecutive_runs(frames, knows_ball)
        plot_side_by_side_comparison(frames, knows_ball)
        
        print("\nAnalysis complete. Files created in folder:", output_folder)
        
    except Exception as e:
        print(f"Error during analysis: {e}")
    
    finally:
        # Stop log capture
        log_capture.stop()
        
        # Create summary file with log output
        log_text = log_capture.get_log()
        summary_file = create_summary_file(log_id, output_folder, log_text)
        
        print(f"\nAnalysis complete. Results saved to folder: {output_folder}")
        print(f"Summary file: {summary_file}")