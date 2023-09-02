from ..classes.dataset import Dataset
from ..classes.datasetfile import DatasetFile
from urllib.parse import urlencode


class DatasetService:
    def __init__(self, client):
        self.client = client

    def get_dataset(self, dataset_name):
        params = { "datasetName": dataset_name}
        dataset = self.client.http_get("/api/dataset/get_dataset_by_name?" + urlencode(params))
        return Dataset(
            dataset["id"],
            dataset["name"],
            dataset["files"],
            self.client,
        )
