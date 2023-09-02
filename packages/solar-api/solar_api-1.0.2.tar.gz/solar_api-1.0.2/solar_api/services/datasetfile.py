from ..classes.datasetfile import DatasetFile
from urllib.parse import urlencode
from typing import List

class DatasetFileService:
    def __init__(self, client):
        self.client = client

    def get_files(self) -> List[DatasetFile]:
        files = self.client.http_get("/api/datasetfiles")
        return [DatasetFile(f['fileId'],f['fileName'],f.get('numRows'),f['numColumns'], f['processingStatus'], f.get('processingError')) for f in files]
