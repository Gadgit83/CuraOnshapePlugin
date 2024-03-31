import requests
import tempfile
from io import BytesIO
from UM.Logger import Logger #Adding messages to the log.
from PyQt6.QtCore import QUrl

class OnshapeAPI:
    # Initialise the plugin 
    def __init__(self, access_token: str, access_secret:str, app):
        self.access_token = access_token
        self.access_secret = access_secret
        self.base_url = "https://cad.onshape.com"
        self.app = app

    # Use the Onshape API to get the top level folders for this user
    def get_top_level_folders(self):
        url = f"{self.base_url}/api/globaltreenodes/magic/1"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, auth=(self.access_token,self.access_secret),headers=headers)
        #Logger.log("d",url)
        #Logger.log("d",headers)
        #Logger.log("d",response.json())
        if response.status_code != 200:
            raise ValueError(f"Failed to get top level folders. HTTP status code: {response.status_code}")
            
        response_json = response.json()
        items = response_json['items']
        folders = []
        for item in items:
            if item['jsonType'] == 'folder':
                folder = {'name': item['name'], 'id': item['id']}
                folders.append(folder)
        return folders

    # Use the Onshape API to get any parts which are located at the top level
    def get_top_level_parts(self):
        url = f"{self.base_url}/api/globaltreenodes/magic/1?offset=0&limit=50"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, auth=(self.access_token,self.access_secret),headers=headers)
        #Logger.log("d",url)
        #Logger.log("d",headers)
        
        if response.status_code != 200:
            raise ValueError(f"Failed to get part studios in folder. HTTP status code: {response.status_code}, Content: {response.content}")

        #Logger.log("d",response.json())
        response_json = response.json()
        items = response_json['items']
        
        part_studios = []
        for item in items:
            if item['resourceType'] == 'document':
                part_studio = {'name': item['name'], 'id': item['id'], 'default_workspace': item['defaultWorkspace']['id']}
                part_studios.append(part_studio)
                
        return part_studios
    
    # For the given folder, get the Part Studios in that folder
    def get_part_studios_in_folder(self, folder_id: str):
        url = f"{self.base_url}/api/globaltreenodes/folder/{folder_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, auth=(self.access_token,self.access_secret),headers=headers)
        #Logger.log("d",url)
        #Logger.log("d",headers)
        #Logger.log("d",response.json())
        if response.status_code != 200:
            raise ValueError(f"Failed to get part studios in folder. HTTP status code: {response.status_code}")

        response_json = response.json()
        items = response_json['items']
        
        part_studios = []
        for item in items:
            if item['resourceType'] == 'document':
                part_studio = {'name': item['name'], 'id': item['id'], 'default_workspace': item['defaultWorkspace']['id']}
                part_studios.append(part_studio)
                
        return part_studios

    # Get all the documents in a folder - Not currently used
    def get_documents(self):
        url = f"{self.base_url}/api/documents"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url,auth=(self.access_token,self.access_secret), headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Failed to get documents. HTTP status code: {response.status_code}")
        return response.json()
    
    # Get folders in a folder
    def get_folders(self, parent_id):
        url = f"{self.base_url}/api/globaltreenodes/folder/{parent_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url,auth=(self.access_token,self.access_secret), headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Failed to get folders. HTTP status code: {response.status_code}")
            
        response_json = response.json()
        items = response_json['items']
        
        folders = []
        for item in items:
            if item['jsonType'] == 'folder':
                folder = {'name': item['name'], 'id': item['id']}
                folders.append(folder)
        return folders

    # Get all the 'parts' in a 'Part Studio'
    def get_parts_in_partstudio(self, partstudio_id: str, default_workspace_id: str):
        url = f"{self.base_url}/api/documents/d/{partstudio_id}/w/{default_workspace_id}/insertables?includeParts=true"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, auth=(self.access_token,self.access_secret),headers=headers)
        #Logger.log("d",url)
        #Logger.log("d",headers)
        #Logger.log("d",response.json())
        if response.status_code != 200:
            raise ValueError(f"Failed to get parts in workspace. HTTP status code: {response.status_code}")

        response_json = response.json()
        parts = response_json['items']
        return parts
        
    # class initializer and other methods here
    def get_part_studio_image(self, part_studio_id, width=100, height=100):
        url = f"{self.base_url}/api/partstudios/{part_studio_id}/thumbnail?width={width}&height={height}"
        headers = {"Authorization": f"Bearer {self.access_token}", "Accept": "image/jpeg"}
        response = requests.get(url,auth=(self.access_token,self.access_secret), headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Failed to get part studio image. HTTP status code: {response.status_code}")
        return BytesIO(response.content)

    # Export a given part STL
    def export_part_stl(self, document_id: str, workspace_id: str, entity_id:str, part_id: str):
        url = f"{self.base_url}/api/partstudios/d/{document_id}/w/{workspace_id}/e/{entity_id}/stl?mode=binary&grouping=true&units=millimeter"
        if part_id is not None:
            url = url + f"&partIds={part_id}"
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "accept": "application/vnd.onshape.v1+octet-stream"
        }
        response = requests.get(url, auth=(self.access_token,self.access_secret), headers=headers, allow_redirects=False)
        #Logger.log("d",url)
        #Logger.log("d",headers)
        #Logger.log("d",response.content)
        if response.status_code == 307:
            location = response.headers["location"]
            
            headers["accept"] = "application/vnd.onshape.v1+json"
            response = requests.get(location, auth=(self.access_token,self.access_secret), headers=headers)
        
        if response.status_code != 200:
            raise ValueError(f"Failed to export part to STL. HTTP status code: {response.status_code}")
        # Saving the file locally
        with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp_file:
            tmp_file.write(response.content)
            tmp_file_name = tmp_file.name
        return tmp_file_name
       
    # Put the given file on to the print bed
    def add_part_to_printbed(self, part_stl_file_path):
        self.app.readLocalFile(QUrl.fromLocalFile(part_stl_file_path))
