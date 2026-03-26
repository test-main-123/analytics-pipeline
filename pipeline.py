"""Core pipeline processing module."""

import yaml
import pandas as pd
import numpy as np


class Pipeline:
    """Data processing pipeline."""

    def __init__(self, config_path: str) -> None:
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.data: pd.DataFrame | None = None

    def extract(self) -> pd.DataFrame:
        """Extract data from configured sources."""
        frames = []
        for source in self.config["sources"]:
            if source["type"] == "csv":
                df = pd.read_csv(source["path"])
                frames.append(df)
        self.data = pd.concat(frames, ignore_index=True)
        return self.data

    def transform(self) -> pd.DataFrame:
        """Apply configured transformations."""
        if self.data is None:
            raise ValueError("No data loaded. Run extract() first.")

        for t in self.config["transformations"]:
            if t["name"] == "clean_nulls":
                self.data = self.data.dropna()
            elif t["name"] == "normalize":
                for col in t["columns"]:
                    if col in self.data.columns:
                        min_val = self.data[col].min()
                        max_val = self.data[col].max()
                        self.data[col] = (self.data[col] - min_val) / (max_val - min_val)
        return self.data

    def load(self) -> str:
        """Write processed data to the configured output."""
        output = self.config["output"]
        path = output["path"]
        fmt = output.get("format", "parquet")

        if fmt == "csv":
            self.data.to_csv(path, index=False)
        elif fmt == "parquet":
            self.data.to_parquet(path, partition_cols=[output.get("partition_by")])
        else:
            raise ValueError(f"Unsupported output format: {fmt}")

        return path
