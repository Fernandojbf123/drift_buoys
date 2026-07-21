import os
from datetime import datetime
import pandas as pd

def write_downloads_history(serial):
    """
    Write the download history for a given serial number to a file.

    Args:
        serial (str): The serial number of the downloaded data.
    """
    
    # Define the path to the downloads history file
    
    tmp_folder = "descargar_datos/tmp_files/"
    history_file_path = os.path.join(tmp_folder, "downloads_history.csv")

    # Create the tmp_folder if it doesn't exist
    os.makedirs(tmp_folder, exist_ok=True)

    # Get the current timestamp
    timestamp = pd.Timestamp.now().replace(microsecond=0, second=0)  # Remove microseconds and seconds for cleaner output

    if not os.path.exists(history_file_path):
        # If the file doesn't exist, create it with headers
        history_df = pd.DataFrame(columns=["serial", "timestamp"])
        history_df.to_csv(history_file_path, index=False)  # Save the empty DataFrame with headers

    # Append the new entry to the history file
    history_df = pd.DataFrame([[serial, timestamp]], columns=["serial", "timestamp"])
    history_df.to_csv(history_file_path, mode="a", header=False, index=False)

    # print(f"Download history updated for serial: {serial}")