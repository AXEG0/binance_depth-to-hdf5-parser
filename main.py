import os
import sys
import h5py
import time
import requests
import numpy as np
from datetime import datetime

symbol = 'BTCUSDT'
depth_limit = 1000
sleep_time = 5
max_retries = 10
retry_delay = 10  # seconds
counter = 0


def save_data_to_h5(data: {str: [[float]]}, timestamp: str):
    # Get the current date as a string and create the file name
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_name = f'data/{current_date}.h5'

    # Check if the file exists and set the mode accordingly
    mode = 'a' if os.path.exists(file_name) else 'w'

    # Open the h5 file with the selected mode
    with h5py.File(file_name, mode) as h5_file:
        # Create a group for the current timestamp
        timestamp_group = h5_file.create_group(timestamp)

        # Iterate over the data and save it to the h5 file
        for key, sub_data in data.items():
            key_group = timestamp_group.create_group(key)
            # Convert the list of lists to a numpy array and save it as a dataset
            key_group.create_dataset(
                'data',
                data=np.array(sub_data, dtype=float),
                compression="gzip",
                compression_opts=9
            )


while True:
    try:
        while True:
            retry_count = 0
            while retry_count < max_retries:
                try:
                    response = requests.get(
                        f'https://www.binance.com/api/v1/depth?symbol={symbol}&limit={depth_limit}',
                        timeout=10
                    ).json()
                    break  # break out of the retry loop if successful
                except requests.exceptions.ConnectionError as e:
                    print(f'Request failed: {e}. Retrying in {retry_delay} seconds...')
                    retry_count += 1
                    time.sleep(retry_delay)
            else:
                # If all retries failed, log an error message and skip this iteration
                print(f'Failed to retrieve data after {max_retries} retries. Skipping iteration.')
                continue

            current_time = time.time()
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
            current_time = current_time + "." + str(int(time.time() * 1000))[-3:]

            # Delete lastUpdateId key from response
            del response['lastUpdateId']
            save_data_to_h5(response, current_time)

            print(counter, current_time)
            print("-" * (counter % 10))
            counter += 1

            # Wait for one second before retrieving and inserting the next set of data
            time.sleep(sleep_time)

    except Exception as e:
        print("Error:", e)
        print("Restarting script in 60 seconds...")
        time.sleep(60)
        # Restart the script using the same command that launched it
        os.execv(sys.executable, ['python'] + sys.argv)
