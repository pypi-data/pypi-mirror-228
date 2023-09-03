import requests
import os
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

    def _file_exists(self, source_name: str, file_name: str):
        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        response = self._request("POST", "/files/exists", data)
        return response

    def get_usage(self) -> dict:
        return self._request("GET", "/usage")

    def get_sources(self) -> List[str]:
        return self._request("GET", "/sources")
    
    def get_files(self, source_name: str) -> List[str]:
        data = {
            'source_name': source_name
        }
        return self._request("POST", "/files", data)

    def get_agents(self) -> List[str]:
        return self._request("GET", "/agents")

    def get_models(self) -> List[str]:
        return self._request("GET", "/models")

    def upload_file(self, source_name: str, local_path: str):
         
        file_name = os.path.basename(local_path)
        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        if self._file_exists(source_name, file_name):
            file_name = self._request("POST", "/files/unique-name", data)
            data["file_name"] = file_name

        presigned_url = self._request("POST", "/files/upload-url", data)
        
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

        if not self._file_exists(source_name, file_name):
            print(f"File '{file_name}' does not exist in source '{source_name}'.")
            return False

        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        presigned_url = self._request("POST", "/files/delete-url", data)
        response = requests.delete(presigned_url)

        if response.status_code != 204:
            print(f"Failed to delete file. HTTP Status code: {response.status_code}")
            return False

        self._request("POST", "/files/delete-sync", data)
        print(f"File '{file_name}' was deleted from source '{source_name}'.")
        return True


    def download_file(self, source_name: str, file_name: str, local_path: str):
        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        presigned_url = self._request("POST", "/files/download-url", data)
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