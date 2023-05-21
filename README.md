# Binance Depth to HDF5 Parser

Binance Depth to HDF5 Parser is a utility designed to parse Binance depth data into Hierarchical Data Format (HDF5) files. HDF5 is an open-source file format that supports large, complex, heterogeneous data. 

## Why HDF5?

HDF5 is a highly efficient and flexible data storage format that provides several key benefits for storing Binance depth data:

1. **Selective Storage**: One of the main advantages of HDF5 over SQL-like databases is its ability to store only the necessary data and exclude redundant information. In SQL databases, data is often stored in tables, which can lead to redundancy and unnecessary storage consumption, especially when dealing with complex or hierarchical data structures. In contrast, HDF5's structure allows for the organization and structuring of data in a more flexible way, similar to a "file directory". This enables more efficient storage mechanisms that can be tailored to fit the specific requirements of the data, reducing redundancy and optimizing storage use.

2. **GZIP Compression**: With this utility, HDF5 files are compressed using GZIP with the highest compression level. This ensures that the stored data takes up minimal disk space while still maintaining fast read/write speeds. 

3. **Scalability and Portability**: HDF5 can handle anything from small to very large data collections (in the order of petabytes) and is portable across most computing platforms. The data stored in HDF5 format can be accessed by software written in many languages including Python, Java, MATLAB, R, etc.

## Prerequisites

Docker

## Build

To build the Docker image, run the following command:

```bash
docker build --no-cache -t binance_depth-to-hdf5-parser-image .
```

## Run

To run the application, use the following command:

```bash
docker run \
-p 4000:8023 \
-v /Users/aleksandr/PycharmProjects/binance_depth-to-hdf5-parser/data:/app/data \
-it binance_depth-to-hdf5-parser-image \
--symbol BTCUSDT \
--depth_limit 1000 \
--sleep_time 5 \
--max_retries 10 \
--retry_delay 10
```

The above command will run the binance_depth-to-hdf5-parser application with the following parameters:

- `-p 4000:8023`: Map local port 4000 to container's port 8023.
- `-v /Users/aleksandr/PycharmProjects/binance_depth-to-hdf5-parser/data:/app/data`: Map local volume to the container's volume. This is where the generated HDF5 files will be saved.
- `--symbol BTCUSDT`: The symbol for which depth data will be fetched and parsed.
- `--depth_limit 1000`: The maximum depth limit for the fetched data.
- `--sleep_time 5`: The time (in seconds) the application will sleep between data fetches.
- `--max_retries 10`: The maximum number of retries in case of failure when fetching data.
- `--retry_delay 10`: The time (in seconds) the application will wait before retrying after a failure.

## Reading HDF5 Files

Along with the parser, this repository also includes a script, `read_h5.py`, that simplifies the process of reading the generated HDF5 files. This Python script uses the h5py library, which is a Pythonic interface to the HDF5 file format.

### Usage

To use `read_h5.py`, run the following command:

```bash
python read_h5.py --file_path /path/to/hdf5/file
```

Replace `/path/to/hdf5/file` with the path to the HDF5 file you wish to read.

### What Does `read_h5.py` Do?

The `read_h5.py` script reads the HDF5 file and displays its contents in a human-readable format. This enables you to quickly inspect the stored data without needing to manually navigate the HDF5 file structure.

This script provides a convenient way to verify the contents of the HDF5 files generated by the Binance Depth to HDF5 Parser, making it a valuable tool for ensuring data integrity and understanding your dataset.

Remember, you'll need to have Python and the h5py library installed to use this script. If you don't already have h5py installed, you can install it via pip:

```bash
pip install h5py
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Aleksandr Golovin - axegggl@gmail.com

Project Link: [https://github.com/AXEG0/binance_depth-to-hdf5-parser](https://github.com/AXEG0/binance_depth-to-hdf5-parser)