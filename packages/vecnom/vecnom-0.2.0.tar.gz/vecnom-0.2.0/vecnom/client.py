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


    def get_usage(self) -> dict:
        return self._request("GET", "/usage")

    def get_sources(self) -> List[str]:
        return self._request("GET", "/sources")

    def get_agents(self) -> List[str]:
        return self._request("GET", "/agents")

    def get_models(self) -> List[str]:
        return self._request("GET", "/models")

    def upload_file(self, source_name: str, local_file_path: str):
        file_name = os.path.basename(local_file_path)
        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        presigned_url = self._request("POST", "/upload-url", data)
        print(presigned_url)
        try:
            with open(local_file_path, 'rb') as file:
                files = {'file': file}
                response = requests.put(presigned_url, data=file)

            if response.status_code != 200:
                print(f"Failed to upload file. HTTP Status code: {response.status_code}")
                return False

            data = {
                'source_name': source_name,
                'file_name': file_name
            }
            print(data)
            self._request("POST", "/upload-sync", data)
            print('upload done!')
            return True
        except FileNotFoundError:
            print(f"The file {local_file_path} does not exist.")
            return False
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
            return False
    

    def delete_file(self, source_name: str, file_name: str):
        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        presigned_url = self._request("POST", "/delete-url", data)
        response = requests.delete(presigned_url)

        if response.status_code != 204:
            print(f"Failed to delete file. HTTP Status code: {response.status_code}")

        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        print(data)
        self._request("POST", "/delete-sync", data)
        print('delete done!')
        return True


    def download_file(self, source_name: str, file_name: str, local_file_path: str):
        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        presigned_url = self._request("POST", "/download-url", data)
        response = requests.get(presigned_url)
        if response.status_code == 200:
            with open(local_file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded file to {local_file_path}")
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
