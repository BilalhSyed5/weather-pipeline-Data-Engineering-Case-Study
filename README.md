# Weather Pipeline

## Overview

This project is a weather data pipeline that fetches current and forecast weather data for Dallas, Houston, and Austin from the AccuWeather API, processes it, and stores it in a DuckDB database. It also includes SQL queries to analyze the stored data.

## Files

### `main.py`

- **Description:** Fetches weather data from the AccuWeather API and stores it in a DuckDB database.
- **Functions:**
  - `fetch_weather_data(location_id: str)`: Fetches current and forecast weather data for a given location ID.
  - `process_weather_data(city: str, data: Dict[str, Any])`: Processes and formats the fetched weather data.
  - `store_data(data: List[Dict[str, Any]])`: Stores the processed weather data in a DuckDB database.
  - `main()`: Main function that coordinates fetching, processing, and storing the data.

### `queries.py`

- **Description:** Contains SQL queries to analyze the weather data stored in the DuckDB database.
- **Functions:**
  - `execute_query(query: str)`: Executes a given SQL query and returns the results.
  - `print_results(query: str, results: List[Tuple[Any, ...]])`: Prints the results of a query.
  - `main()`: Runs a set of predefined queries and prints the results.

### `requirements.txt`

- **Description:** Lists the Python packages required for the project.
- **Packages:**
  - `requests==2.31.0`: For making HTTP requests.
  - `duckdb==1.1.0`: For interacting with the DuckDB database.
  - `mypy==1.4.1`: For type checking.
  - `types-requests==2.31.0.2`: Type stubs for `requests`.

### `Dockerfile`

- **Description:** Defines the Docker image for running the project.
- **Instructions:**
  - **Base Image:** Uses Python 3.11 slim.
  - **Work Directory:** Sets `/app` as the working directory.
  - **Dependencies:** Installs Python packages from `requirements.txt`.
  - **Files:** Copies `main.py` and `queries.py` into the Docker image.
  - **Command:** Runs `main.py` and `queries.py` sequentially.

## Running the Project

1. **Build the Docker Image:**
   ```bash
   docker build -t weather-pipeline:latest .
1. **Build the Docker Image:**
   ```bash
   docker run weather-pipeline:latest"# weather-pipeline-Data-Engineering-Case-Study" 
