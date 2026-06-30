import pandas as pd
from sklearn.ensemble import IsolationForest
import config

class SCADAAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            contamination=config.ANOMALY_CONTAMINATION,
            random_state=42,
            n_estimators=100
        )
        # Train model using multivariate features representing asset stress
        self.feature_cols = [
            'wind_speed', 
            'active_power', 
            'gearbox_temperature', 
            'power_deviation', 
            'wind_speed_rolling_std_1h'
        ]

    def fit(self, df: pd.DataFrame):
        self.model.fit(df[self.feature_cols])
        return self

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # Isolation Forest outputs -1 for anomalies, 1 for normal profiles
        predictions = self.model.predict(df[self.feature_cols])
        df['is_anomaly'] = (predictions == -1).astype(int)
        
        # Calculate an anomaly score for finer priority filtering
        df['anomaly_score'] = self.model.score_samples(df[self.feature_cols]) * -1
        return df