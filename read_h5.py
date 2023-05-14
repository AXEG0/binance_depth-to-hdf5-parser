import os
import h5py


def load_all_data_from_h5(date: str) -> {str: {str: [[float]]}}:
    # Create the file name based on the given date
    file_name = f'data/{date}.h5'

    # Check if the file exists
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"The file {file_name} does not exist.")

    # Open the h5 file in read mode
    all_data = {}
    with h5py.File(file_name, 'r') as h5_file:
        # Loop through all the timestamp groups
        for timestamp in h5_file.keys():
            timestamp_group = h5_file[timestamp]

            # Read the data and convert it to the original data structure
            data = {}
            for key in timestamp_group.keys():
                key_group = timestamp_group[key]
                # Load the dataset and convert it to a list of lists
                data[key] = key_group['data'][:].tolist()

            # Store the data in the all_data dictionary with the timestamp as the key
            all_data[timestamp] = data

    return all_data


date = '2023-05-14'
all_data = load_all_data_from_h5(date)
print(all_data)