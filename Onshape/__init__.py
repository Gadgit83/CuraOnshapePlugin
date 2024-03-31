from cura.CuraApplication import CuraApplication
from .onshape import Onshape
from .OnshapeAPI import OnshapeAPI
from .Settings import Settings

def getMetaData() -> dict:
    return {
        "plugin": {
            "name": "Onshape",
            "author": "Gadgit",
            "version": "1.0",
            "description": "A Cura plugin for importing parts from Onshape",
            "api": 2
        }
    }

def register(app: CuraApplication) -> None:

    # Register the extension with OnShape
    onshape_api = OnshapeAPI(Settings.ONSHAPE_API_TOKEN, Settings.ONSHAPE_API_SECRET, app)
    return {
        "extension": Onshape(onshape_api)
    }