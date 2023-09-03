import requests
import os
from urllib.parse import unquote
from typing import List, Optional, Any

class VectifyClient:

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'api_key': self.api_key
        }

    def _request(self, method: str, endpoint: str, data: Optional[dict] = None):
        url = f"{self.base_url}{endpoint}"

        if method == "GET":
            response = requests.get(url, headers=self.headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=self.headers)
        
        response.raise_for_status()  # This will raise an exception for HTTP error codes.
        return response.json()


    def usage(self) -> dict:
        return self._request("GET", "/usage")

    def list_sources(self) -> List[str]:
        return self._request("GET", "/sources")
    
    def list_files(self, source_name: str = 'default') -> List[str]:
        data = {
            'source_name': source_name
        }
        return self._request("POST", "/files", data)
    
    def list_models(self) -> List[str]:
        return self._request("GET", "/models")

    def list_agents(self) -> List[str]:
        return self._request("GET", "/agents")


    def upload_file(self, source_name: str, local_path: str):
         
        file_name = os.path.basename(local_path)
        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        presigned_url = self._request("POST", "/files/upload-url", data)

        path_splits = presigned_url.split('/')
        last_part = path_splits[-1].split('?')[0]
        file_name = unquote(last_part)
        data['file_name'] = file_name
        
        try:
            with open(local_path, 'rb') as file:
                files = {'file': file}
                response = requests.put(presigned_url, data=file)

            if response.status_code != 200:
                print(f"Failed to upload file. HTTP Status code: {response.status_code}")
                return False

            self._request("POST", "/files/upload-sync", data)
            print(f"File '{file_name}' was uploaded to source '{source_name}'.")
            return True
        except FileNotFoundError:
            print(f"The file {local_path} does not exist.")
            return False
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
            return False


    def delete_file(self, source_name: str, file_name: str):

        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        presigned_url = self._request("POST", "/files/delete-url", data)
        if presigned_url == None:
            print(f"File '{file_name}' does not exist in source '{source_name}'.")
            return False
        
        response = requests.delete(presigned_url)
        if response.status_code == 204:
            self._request("POST", "/files/delete-sync", data)
            print(f"File '{file_name}' was deleted from source '{source_name}'.")
            return True
        else:
            print(f"Failed to delete file. HTTP Status code: {response.status_code}")
            return False
    

    def download_file(self, source_name: str, file_name: str, local_path: str):

        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        presigned_url = self._request("POST", "/files/download-url", data)
        if presigned_url == None:
            print(f"File '{file_name}' does not exist in source '{source_name}'.")
            return False
        
        response = requests.get(presigned_url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"File '{file_name}' from source '{source_name}' was downloaded to '{local_path}'.")
            return True;
        else:
            print(f"Failed to download file. HTTP Status Code: {response.status_code}. Reason: {response.text}")
            return False;

    
    def retrieve(self, query: str, top_k: int, sources: List[str]) -> dict:
        data = {
            'query': query,
            'top_k': top_k,
            'sources': sources
        }
        return self._request("POST", "/retrieve", data)


    def chat(self, query: Optional[str], agent: str, model: Optional[str], chat_history: Optional[List[Any]]) -> dict:
        data = {
            'query': query,
            'agent': agent,
            'model': model,
            'chat_history': chat_history
        }
        return self._request("POST", "/chat", data)