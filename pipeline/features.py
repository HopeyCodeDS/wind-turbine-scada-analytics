import numpy as np
import pandas as pd
import config

def compute_theoretical_power(wind_speed):
    """Calculates ideal aerodynamic power output based on design standards."""
    if wind_speed < config.CUT_IN_SPEED or wind_speed > config.CUT_OUT_SPEED:
        return 0.0
    if wind_speed >= config.RATED_SPEED:
        return config.RATED_POWER
    fraction = (wind_speed - config.CUT_IN_SPEED) / (config.RATED_SPEED - config.CUT_IN_SPEED)
    return config.RATED_POWER * (fraction ** 3)

def engineering_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # 1. Calculate the Theoretical Power baseline for every individual timestamp
    df['theoretical_power'] = df['wind_speed'].apply(compute_theoretical_power)
    
    # 2. Power Curve Loss Metric: Deviation from the expected physical limit
    df['power_deviation'] = df['theoretical_power'] - df['active_power']
    
    # 3. Rolling Analytics: Detect high-frequency structural shifts
    df = df.sort_values('timestamp').reset_index(drop=True)
    df['wind_speed_rolling_std_1h'] = df['wind_speed'].rolling(window=6, min_periods=1).std()
    df['power_rolling_avg_1h'] = df['active_power'].rolling(window=6, min_periods=1).mean()
    
    # Fill any edge-case NaNs resulting from rolling operations
    df = df.bfill().ffill()
    
    return df