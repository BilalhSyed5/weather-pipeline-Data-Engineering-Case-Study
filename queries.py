import duckdb
from typing import List, Tuple, Any

def execute_query(query: str) -> List[Tuple[Any, ...]]:
    conn = duckdb.connect("weather_data.db")
    result = conn.execute(query).fetchall()
    conn.close()
    return result

def print_results(query: str, results: List[Tuple[Any, ...]]) -> None:
    print(f"\nQuery: {query}")
    for row in results:
        print(row)

def main() -> None:
    queries = [
        ("Which city has the highest current temperature?",
        "SELECT city, current_temperature FROM weather_data ORDER BY current_temperature DESC LIMIT 1"),
        
        ("Which city has the highest forecast temperature?",
        "SELECT city, forecast_max_temperature FROM weather_data ORDER BY forecast_max_temperature DESC LIMIT 1"),
        
        ("List all cities with their current weather descriptions.",
        "SELECT city, current_weather_text FROM weather_data"),
        
        ("What is the average forecasted minimum temperature across all cities?",
        "SELECT AVG(forecast_min_temperature) as avg_min_temp FROM weather_data"),
        
        ("Which city has the largest temperature difference in the forecast?",
        "SELECT city, (forecast_max_temperature - forecast_min_temperature) as temp_difference "
        "FROM weather_data ORDER BY temp_difference DESC LIMIT 1")
    ]

    
    for description, query in queries:
        results = execute_query(query)
        print_results(description, results)

if __name__ == "__main__":
    main()