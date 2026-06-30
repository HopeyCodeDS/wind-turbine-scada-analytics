import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import config

def generate_scada_stream(days=30, interval_mins=10):
    np.random.seed(42)
    start_time = datetime(2026, 1, 1, 0, 0, 0)
    total_records = (days * 24 * 60) // interval_mins
    
    timestamps = [start_time + timedelta(minutes=interval_mins * i) for i in range(total_records)]
    
    # 1. Simulate Wind Speed (m/s) with a diurnal/random pattern
    wind_speed = np.random.weibull(a=2, size=total_records) * 8.5
    wind_speed = np.clip(wind_speed, 0, 30) # Hard caps
    
    # 2. Simulate Theoretical Power Generation (Ideal Power Curve)
    active_power = np.zeros(total_records)
    for i, speed in enumerate(wind_speed):
        if speed < config.CUT_IN_SPEED or speed > config.CUT_OUT_SPEED:
            active_power[i] = 0.0
        elif speed >= config.RATED_SPEED:
            active_power[i] = config.RATED_POWER
        else:
            # Cubic generation phase between cut-in and rated speed
            fraction = (speed - config.CUT_IN_SPEED) / (config.RATED_SPEED - config.CUT_IN_SPEED)
            active_power[i] = config.RATED_POWER * (fraction ** 3)
            
    # Add minor measurement noise to active power
    active_power += np.random.normal(0, 15, total_records)
    active_power = np.clip(active_power, 0, config.RATED_POWER)
    
    # 3. Simulate Generator/Gearbox Temperature (°C) - highly correlated to power output
    base_temp = 20.0
    gearbox_temperature = base_temp + (active_power / config.RATED_POWER) * 55.0 + np.random.normal(0, 2.5, total_records)
    
    # 4. Inject Operational Anomalies (The "Real-World" Faults)
    # Fault Type A: Curtailment / Pitch System Fault (High wind speed, zero power output)
    curtailment_indices = np.random.choice(range(total_records), size=int(total_records * 0.015), replace=False)
    for idx in curtailment_indices:
        if wind_speed[idx] > 8.0:
            active_power[idx] = np.random.uniform(0, 50) # Mechanical breakdown drop
            
    # Fault Type B: Overheating Components (High temp anomaly unrelated to power)
    overheat_indices = np.random.choice(range(total_records), size=int(total_records * 0.015), replace=False)
    for idx in overheat_indices:
        gearbox_temperature[idx] += np.random.uniform(20, 35) # Spikes past safety threshold
        
    df = pd.DataFrame({
        'timestamp': timestamps,
        'wind_speed': wind_speed,
        'active_power': active_power,
        'gearbox_temperature': gearbox_temperature
    })
    
    return df

if __name__ == "__main__":
    df = generate_scada_stream()
    print(f"Generated {len(df)} SCADA records successfully.")