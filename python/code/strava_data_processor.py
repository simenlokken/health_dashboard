import polars as pl
from pathlib import Path

class StravaDataProcessor:

    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.raw_data_path = self.root / "data" / "raw" / "raw_data.csv"
        self.processed_data = self.root / "data" / "processed" / "processed_data.csv"
        self.columns_to_keep = [
            "id",
            "name",
            "sport_type",
            "start_date_local",
            "distance",
            "moving_time",
            "elapsed_time",
            "average_speed",
            "average_watts",
            "weighted_average_watts",
            "average_cadence",
            "average_heartrate",
            "kilojoules",
            "average_temp",
            "max_speed",
            "max_watts",
            "max_heartrate",
            "total_elevation_gain",
            "suffer_score",
        ]

    def read_raw_data(self):

        return pl.read_csv(self.raw_data_path)
    
    def process_data(self, data):

        data_processed = data.select(self.columns_to_keep)
        data_processed = data_processed.with_columns([
            (pl.col("average_speed") * 3.6).round(2).alias("average_speed_kmh"),
            pl.col("start_date_local").str.strptime(pl.Datetime, fmt="%Y-%m-%dT%H:%M:%SZ").alias("start_date"),
            pl.col("start_date_local").str.strptime(pl.Datetime, fmt="%Y-%m-%dT%H:%M:%SZ").dt.hour().alias("start_hour"),
        ])

        return data_processed
    
    def save_processed_data(self, data):
        self.processed_data_path.parent.mkdir(parents=True, exist_ok=True)
        data.write_csv(self.processed_data_path)
        print(f"Processed data saved to {self.processed_data_path}")

    def process_and_save_data(self):
        raw_data = self.read_raw_data()
        processed_data = self.process_data(raw_data)
        self.save_processed_data(processed_data)