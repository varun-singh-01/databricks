import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_airline_fares_csv(num_samples: int = 10_000_000, filename: str = 'sample_airline_fares.csv'):
    """
    Generates a CSV file with a specified number of sample airline fares.

    Args:
        num_samples (int): The number of sample fare entries to generate.
        filename (str): The name of the CSV file to save the data to.
    """
    print(f"Generating {num_samples:,} sample airline fares...")

    # --- Configuration ---
    # Realistic-ish data for airlines, sources, and destinations
    airline_names = [
        "AirTravel", "SkyLink", "GlobalWings", "SwiftAir", "HorizonFly",
        "PacificJets", "AtlanticRoute", "ContinentalLine", "StarFlight",
        "ApexAirlines", "BlueSky Airways", "Eagle Air", "Freedom Fly",
        "Voyage Airlines", "Zenith Airways", "Northwind Air", "SouthBound Flights"
    ]

    # Sample major airports/cities for source and destination
    airports = [
        "LAX", "JFK", "ORD", "DFW", "DEN", "SFO", "SEA", "CLT", "MIA", "PHX",
        "ATL", "BOS", "IAD", "EWR", "MCO", "LAS", "DTW", "PHL", "MSP", "IAH",
        "LHR", "CDG", "DXB", "HND", "PEK", "PVG", "SIN", "SYD", "FRA", "AMS"
    ]

    # Date range for 'updated_date' (last year)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) # Data from the last year

    # --- Data Generation ---
    # 1. Generate IDs
    ids = np.arange(num_samples)

    # 2. Generate airline names
    # Using np.random.choice for efficiency with large arrays
    airlines = np.random.choice(airline_names, num_samples)

    # 3. Generate source and destination airports
    # Generate indices and ensure source != destination
    source_indices = np.random.randint(0, len(airports), num_samples)
    destination_indices = np.random.randint(0, len(airports), num_samples)

    # Ensure source and destination are not the same
    # This loop re-rolls destinations where they match their source
    while np.any(source_indices == destination_indices):
        mask = (source_indices == destination_indices)
        destination_indices[mask] = np.random.randint(0, len(airports), np.sum(mask))

    sources = np.array(airports)[source_indices]
    destinations = np.array(airports)[destination_indices]

    # 4. Generate fares
    # Fares between $50 and $1000, rounded to 2 decimal places
    fares = np.round(np.random.uniform(50.0, 1000.0, num_samples), 2)

    # 5. Generate updated dates
    # Calculate total seconds in the date range
    total_seconds = int((end_date - start_date).total_seconds())

    # Generate random seconds offset for each sample
    random_seconds_offsets = np.random.randint(0, total_seconds, num_samples)

    # Convert seconds offset to actual datetimes
    # Use vectorized operation for efficiency
    updated_dates_raw = start_date + pd.to_timedelta(random_seconds_offsets, unit='s')
    updated_dates = updated_dates_raw.strftime('%Y-%m-%d')

    # --- Create DataFrame ---
    print("Creating DataFrame...")
    data = pd.DataFrame({
        'id': ids,
        'airline_name': airlines,
        'source': sources,
        'destination': destinations,
        'fare': fares,
        'updated_date': updated_dates
    })

    # --- Save to CSV ---
    print(f"Saving data to {filename}...")
    try:
        # Use a smaller chunksize for writing to avoid potential memory issues during write
        # index=False prevents pandas from writing the DataFrame index as a column
        data.to_csv(filename, index=False)
        print(f"Successfully generated '{filename}' with {num_samples:,} entries.")
        print(f"File size: {os.path.getsize(filename) / (1024*1024):.2f} MB")
    except Exception as e:
        print(f"An error occurred while saving the CSV: {e}")

if __name__ == "__main__":
    # You can change the number of samples or the filename here
    generate_airline_fares_csv(num_samples=10_000_000, filename='sample_airline_fares.csv')