from torch.utils.data import Dataset
import pandas as pd
from sklearn.model_selection import train_test_split

class TimeSeriesDataset(Dataset):
    def __init__(self, data: pd.DataFrame, target_column: str, sequence_length: int):
        self.data = data
        self.target_column = target_column
        self.sequence_length = sequence_length
        self.features = data.drop(columns=[target_column]).values
        self.targets = data[target_column].values

    def __len__(self):
        return len(self.data) - self.sequence_length

    def __getitem__(self, index: int):
        x = self.features[index:index + self.sequence_length]
        y = self.targets[index + self.sequence_length]
        return x, y

    @classmethod
    def create_datasets(cls, data: pd.DataFrame, target_column: str, sequence_length: int, test_size: float = 0.2):
        train_data, test_data = train_test_split(data, test_size=test_size, shuffle=False)
        train_dataset = cls(train_data, target_column, sequence_length)
        test_dataset = cls(test_data, target_column, sequence_length)
        return train_dataset, test_dataset