import pandas as pd


class SimulationDataCollector:

    def __init__(self):
        self.records = []

    def collect(self, result):
        self.records.append(result)

    def to_dataframe(self):
        return pd.DataFrame(self.records)

    def save_csv(self, filename):
        df = self.to_dataframe()
        df.to_csv(filename, index=False)
        return df
