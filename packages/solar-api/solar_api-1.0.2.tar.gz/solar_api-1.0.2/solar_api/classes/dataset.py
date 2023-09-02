import json
from urllib.parse import urlencode
from typing import List, IO
from .httpclient import HttpClient
from .datasetfile import DatasetFile
from ..util.upload_helper import upload
import pandas as pd

class Dataset:
    """
    Class to represent and access a Tonic workspace.

    Parameters
    ----------
    id: str
        Dataset id.

    name: str
        Dataset name.

    client: HttpClient
        The http client to use.
    """
    def __init__(self, id: str, name: str, files: List[DatasetFile], client: HttpClient):
        self.id = id
        self.name = name
        self.client = client
        self.files = [DatasetFile(f['fileId'],f['fileName'],f.get('numRows'),f['numColumns'], f['processingStatus'], f.get('processingError')) for f in files]

        if len(self.files) > 0:
            self.num_columns = max([f.num_columns for f in self.files])
        else:
            self.num_columns = None

        self.num_rows_per_request = 35
        self.total_rows_fetched = 0
        self._finished = False


        self._total_rows_fetched_in_current_file = 0
        self._cur_file_idx = 0
        
    def reset(self):
        self._finished = False
        self.total_rows_fetched = 0
        self._cur_file_idx = 0


    def add_file(self, file_id: str):
        """
        Adds a file to the dataset, if the file is not found an error is returned

        Parameters
        ---------
        file_name : str
        The name of the file
        """
        new_dataset = self.client.http_put("/api/dataset", data={"id":self.id, "name":self.name, "generatorSetup": {}, "fileIds": [file_id] + [f.id for f in self.files]})
        self.files = [DatasetFile(f['fileId'],f['fileName'],f.get('numRows'),f['numColumns'], f['processingStatus'], f.get('processingError')) for f in new_dataset["files"]]

    def upload_then_add_file(self, file_path: str, file_name:str):
        """
        Uploads a file to the dataset.

        Parameters
        --------
        file_path: str
        The absolute path of the file to be uploaded
        

        file_name: IO[bytes]
        The name of the file to be saved to Solar
        """
        uploadFile = upload(file_path, file_name, self.client)
        new_dataset = self.client.http_put("/api/dataset", data={"id":self.id, "name":self.name, "generatorSetup": {}, "fileIds": [uploadFile.id] + [f.id for f in self.files]})
        self.files = [DatasetFile(f['fileId'],f['fileName'],f.get('numRows'),f['numColumns'], f['processingStatus'], f.get('processingError')) for f in new_dataset["files"]]

    def fetch_df(self) -> pd.DataFrame:
        """
        Fetch data in next batch as pandas dataframe
        
        Returns
        -------
        pd.DataFrame
            Data in pandas dataframe
        """
        data = self._fetch()

        columns = ['col'+str(x) for x in range(self.num_columns)]

        if len(data)==0:
            return pd.DataFrame(columns=columns)
        else:
            return pd.DataFrame(data, columns=columns)
        
    def fetch_json(self) -> str:
        """
        Fetch data in next batch as json
        
        Returns
        -------
        Dataset
            Data in json format
        """
        return json.dumps(self._fetch())
    
    def _fetch(self) -> List[List[str]]:
        """
        Fetch the next batch of data from the dataset.

         Returns
        -------
        List[List[str]]
            The data.
        """

        if(self._cur_file_idx >= len(self.files)):
            self._finished = True
            return []

        response = []
        while True:
            response += self._fetch_current_file()
            if self.total_rows_fetched == self.num_rows_per_request:
                self.total_rows_fetched = 0
                break
            if self._cur_file_idx>=len(self.files):
                break
        return response
        
    
    def _fetch_current_file(self) -> List[List[str]]:
        if(self._cur_file_idx>=len(self.files)):
            return []
        file = self.files[self._cur_file_idx]
        
        
        params = {'datasetId': self.id, 'fileId': file.id, 'startingRow': self._total_rows_fetched_in_current_file, 'numRows': self.num_rows_per_request - self.total_rows_fetched}
        response = self.client.http_get("/api/datasetfiles/get_data?" + urlencode(params))
        self.total_rows_fetched += len(response)
        self._total_rows_fetched_in_current_file += len(response)            
        
        if self.total_rows_fetched!=self.num_rows_per_request:
            self._total_rows_fetched_in_current_file = 0
            self._cur_file_idx += 1
                    
        return response
        

    def fetch_all_df(self) -> pd.DataFrame:
        """
        Fetch all data in the dataset as pandas dataframe
        
        Returns
        -------
        pd.DataFrame
            Data in pandas dataframe
        """
        data = self._fetch_all()

        if self.num_columns is None:
            return pd.DataFrame()

        #RAW file, not CSV
        if self.num_columns == 0:
            if len(data)==0:
                return pd.DataFrame(columns=["text"])
            return pd.DataFrame(data, columns=["text"])

        columns = ['col'+str(x) for x in range(self.num_columns)]
        if len(data)==0:
            return pd.DataFrame(columns=columns)
        else:
            return pd.DataFrame(data, columns=columns)
        
    def fetch_all_json(self) -> str:
        """
        Fetch all data in the dataset as pandas json
        
        Returns
        -------
        str
            Data in json format
        """
        return json.dumps(self._fetch_all())

    def _fetch_all(self) -> List[List[str]]:
        """
        Fetch all data from the dataset.

        Returns
        -------
        List[List[str]]
            The data.
        """
        response = []
        for file in self.files:
            params = {'datasetId': self.id, 'fileId': file.id}
            response += self.client.http_get("/api/datasetfiles/get_data?" + urlencode(params))
        return response

    def describe(self):
        """
        Print the dataset name, id, and list of files.

        Examples
        --------
        >>> workspace.describe()
        Dataset: your_dataset_name [dataset_id]
        Number of Files: 2
        Number of Rows: 1000
        """

        print("Dataset: " + self.name + " [" + self.id + "]")
        print("Number of Files: " + str(len(self.files)))
        print("Number of Rows: " + str(sum([x.num_rows if x.num_rows is not None else 0 for x in self.files])))
        print("Number of rows fetched: " + str(self.total_rows_fetched))
