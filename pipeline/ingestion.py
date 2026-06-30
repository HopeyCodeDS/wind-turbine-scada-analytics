# pipeline/ingestion.py
import pandas as pd
from data_simulator import generate_scada_stream

def load_scada_data(days=14) -> pd.DataFrame:
    """
    In production, this function would connect to a database or SCADA API.
    For this demo, it pulls from our physics-based simulator.
    """
    # 1. Fetch raw data
    df = generate_scada_stream(days=days)
    
    # 2. Basic Ingestion Data Cleansing (Standard Industrial Practice)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.dropna(subset=['timestamp'])
    
    # Ensure chronological order
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    return df