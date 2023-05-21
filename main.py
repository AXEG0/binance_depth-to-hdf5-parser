import os
import sys
import h5py
import time
import requests
import argparse
import numpy as np
from datetime import datetime


class DataCollector:
    """
    Collects data from Binance and stores it in a HDF5 file.

    Parameters
    ----------
    symbol : str
        Trading symbol - e.g. BTCUSDT.
    depth_limit : int
        Depth limit - maximum number of price levels to return.
    sleep_time : int
        Sleep time by seconds.
    max_retries : int
        Max retries by seconds.
    retry_delay : int
        Retry delay by seconds.

    Attributes
    ----------
    symbol : str
        Trading symbol - e.g. BTCUSDT.
    depth_limit : int
        Depth limit - maximum number of price levels to return.
    sleep_time : int
        Sleep time by seconds.
    max_retries : int
        Max retries by seconds.
    retry_delay : int
        Retry delay by seconds.
    counter : int
        Counter for the number of data points collected.

    Methods
    -------
    save_data_to_h5(data, timestamp)
        Saves data to a HDF5 file.
    collect_data()
        Collects data from Binance and stores it in a HDF5 file.


    Examples
    --------
    >>> collector = DataCollector('BTCUSDT', 1000, 5, 3, 60)
    >>> collector.collect_data()
    0 2021-01-01 00:00:00.000
    ----------

    1 2021-01-01 00:00:01.000
    ----------
    """

    def __init__(self, symbol, depth_limit, sleep_time, max_retries, retry_delay):
        self.symbol = symbol
        self.depth_limit = depth_limit
        self.sleep_time = sleep_time
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.counter = 0

    def save_data_to_h5(self, data: {str: [[float]]}, timestamp: str):
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_name = f'data/{current_date}.h5'

        # Check if file exists
        if os.path.exists(file_name):
            # Extract date from filename
            file_date = os.path.basename(file_name).split('.')[0]

            # Compare extracted date with current date
            if file_date == current_date:
                mode = 'a'  # append if same day
            else:
                # if the dates don't match, we create a new file for the new day
                file_name = f'data/{current_date}.h5'
                mode = 'w'  # create new file if different day
        else:
            mode = 'w'  # create new file if doesn't exist

        with h5py.File(file_name, mode) as h5_file:
            timestamp_group = h5_file.create_group(timestamp)
            for key, sub_data in data.items():
                key_group = timestamp_group.create_group(key)
                key_group.create_dataset(
                    'data',
                    data=np.array(sub_data, dtype=float),
                    compression="gzip",
                    compression_opts=9
                )

    def collect_data(self):
        while True:
            try:
                retry_count = 0
                while retry_count < self.max_retries:
                    try:
                        response = requests.get(
                            f'https://www.binance.com/api/v1/depth?symbol={self.symbol}&limit={self.depth_limit}',
                            timeout=10
                        ).json()
                        break
                    except requests.exceptions.ConnectionError as e:
                        print(f'Request failed: {e}. Retrying in {self.retry_delay} seconds...')
                        retry_count += 1
                        time.sleep(self.retry_delay)
                else:
                    print(f'Failed to retrieve data after {self.max_retries} retries. Skipping iteration.')
                    continue

                current_time = time.time()
                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                current_time = current_time + "." + str(int(time.time() * 1000))[-3:]
                del response['lastUpdateId']
                self.save_data_to_h5(response, current_time)
                print(self.counter, current_time)
                print("-" * (self.counter % 10))
                self.counter += 1
                time.sleep(self.sleep_time)

            except Exception as e:
                print("Error:", e)
                print("Restarting script in 60 seconds...")
                time.sleep(60)
                os.execv(sys.executable, ['python'] + sys.argv)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect and store data from Binance.')
    parser.add_argument('--symbol', required=True, help='Trading symbol.')
    parser.add_argument('--depth_limit', type=int, required=True, help='Depth limit.')
    parser.add_argument('--sleep_time', type=int, required=True, help='Sleep time.')
    parser.add_argument('--max_retries', type=int, required=True, help='Max retries.')
    parser.add_argument('--retry_delay', type=int, required=True, help='Retry delay.')

    args = parser.parse_args()

    collector = DataCollector(args.symbol, args.depth_limit, args.sleep_time, args.max_retries, args.retry_delay)
    collector.collect_data()
