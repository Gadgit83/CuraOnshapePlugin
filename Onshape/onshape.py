import sys
import requests
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QDialog, QPushButton,QLabel
from PyQt6.QtGui import QIcon, QPixmap
from UM.Logger import Logger #Adding messages to the log.

from UM.Extension import Extension #The PluginObject we're going to extend.

class Onshape(QDialog,Extension):
    
    # Initialise the UI window, the API, the widget tree, and variables
    def __init__(self, onshape_api):
        super().__init__()
        self._onshape_api = onshape_api
        self._tree = QTreeWidget()
        self._folder_items = {}
        self._part_studio_items = {}
        self._part_items = {}
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._tree)
        self.setLayout(self._layout)
        self.setWindowTitle("Onshape")
        self._tree.itemExpanded.connect(self._handle_item_double_clicked)
        #self._tree.itemActivated.connect(self._handle_item_expanded)
        self._tree.itemDoubleClicked.connect(self._handle_item_double_clicked)
        self._tree.setHeaderHidden(True)
        self._populate_root_folders()
        self.resize(500,600)
        #self.show()
        
        self.setMenuName("Onshape")
        self.addMenuItem("Browse Parts", self.show_gui)
        
    # Display the UI window
    def show_gui(self):
        self.show()

    # Populate all the folders from the root into the tree
    def _populate_root_folders(self):
        folders = self._onshape_api.get_top_level_folders()
        for folder in folders:
            folder_item = QTreeWidgetItem([folder["name"]])
            folder_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, {"type": "folder", "id": folder["id"]})
            folder_item.setIcon(0, QIcon("folder.svg")) # set the folder icon
            folder_item.setExpanded(False)
            #folder_item.itemDoubleClicked.connect(self._handle_item_expanded)
            self._tree.addTopLevelItem(folder_item)
            self._folder_items[folder["id"]] = folder_item
            
        part_studios = self._onshape_api.get_top_level_parts()
        for partstudio in part_studios:
            partstudio_item = QTreeWidgetItem([partstudio["name"]])
            partstudio_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, {"type": "partstudio", "id": partstudio["id"], "default_workspace": partstudio["default_workspace"]})
            #partstudio_item.itemDoubleClicked.connect(self._handle_item_double_clicked)
            self._tree.addTopLevelItem(partstudio_item)
            self._part_studio_items[partstudio["id"]] = partstudio_item

    # Handle expanding an item (typically after double clicking)
    def _handle_item_expanded(self, item):
        item_data = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if "type" not in item_data:
            return
        item_type = item_data["type"]
        #Logger.log("i","Handle Item Expanded{item_type}")
        if item_type == "folder":
            folder_id = item_data["id"]
            
            folders = self._onshape_api.get_folders(folder_id)
            for folder in folders:
                folder_item = QTreeWidgetItem([folder["name"]])
                folder_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, {"type": "folder", "id": folder["id"]})
                folder_item.setExpanded(False)
                folder_item.setIcon(0, QIcon(":/folder.svg")) # set the folder icon
                #folder_item.itemDoubleClicked.connect(self._handle_item_expanded)
                item.addChild(folder_item)
                self._folder_items[folder["id"]] = folder_item
            
            part_studios = self._onshape_api.get_part_studios_in_folder(folder_id)
            for partstudio in part_studios:
                partstudio_item = QTreeWidgetItem([partstudio["name"]])
                partstudio_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, {"type": "partstudio", "id": partstudio["id"], "default_workspace": partstudio["default_workspace"]})
                #partstudio_item.itemDoubleClicked.connect(self._handle_item_double_clicked)
                item.addChild(partstudio_item)
                self._part_studio_items[partstudio["id"]] = partstudio_item
                
        
    # Hanlder for double click on an item
    def _handle_item_double_clicked(self, item):
        item_data = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        
        item.takeChildren()
        
        if "type" not in item_data:
            return
        item_type = item_data["type"]
        #Logger.log("i","Handle Item double clicked{item_type}")
        
        if item_type == "folder":
            folder_id = item_data["id"]
            
            folders = self._onshape_api.get_folders(folder_id)
            for folder in folders:
                folder_item = QTreeWidgetItem([folder["name"]])
                folder_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, {"type": "folder", "id": folder["id"]})
                folder_item.setExpanded(False)
                folder_item.setIcon(0, QIcon(":/folder.svg")) # set the folder icon - does not appear to work - help!
                #folder_item.itemDoubleClicked.connect(self._handle_item_expanded)
                item.addChild(folder_item)
                self._folder_items[folder["id"]] = folder_item
            
            part_studios = self._onshape_api.get_part_studios_in_folder(folder_id)
            for partstudio in part_studios:
                partstudio_item = QTreeWidgetItem([partstudio["name"]])
                partstudio_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, {"type": "partstudio", "id": partstudio["id"], "default_workspace": partstudio["default_workspace"]})
                #partstudio_item.itemDoubleClicked.connect(self._handle_item_double_clicked)
                item.addChild(partstudio_item)
                self._part_studio_items[partstudio["id"]] = partstudio_item
                
        if item_type == "partstudio":
            partstudio_id = item_data["id"]
            parts = self._onshape_api.get_parts_in_partstudio(partstudio_id,item_data["default_workspace"])
            for part in parts:
                
                if part["deterministicId"] is None:
                    part_item = QTreeWidgetItem(["All Parts"])
                else:
                    part_item = QTreeWidgetItem([part["partName"]])
                    
                part_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, {"type": "part", "id": part["deterministicId"], "element_id": part["elementId"], "document_id": part["documentId"],"workspace_id": part["workspaceId"]})
                item.addChild(part_item)
                self._part_items[part["id"]] = part_item
                # export_button = QPushButton("Export STL")
                # export_button.clicked.connect(lambda: self._handle_export_stl_clicked(part_item))
                # export_button.setFixedSize(100, 30)
                # export_button.setVisible(True)
                #Logger.log("d",f"button visible: {export_button.isVisible()}")

                #self._tree.setItemWidget(part_item, 1, export_button)
                
                #part_img = "https://cad.onshape.com/api/thumbnails/{part['thumbnailUri']}/s/70x40"
                #self._tree.setItemWidget(part_item, 2, part_img)
                
        if item_type == "part":
            self._handle_export_stl_clicked(item)
    
    # Add the part to the print bed if clicked
    def _handle_export_stl_clicked(self, part_item):
        #Logger.log("i","Handle Export STL {item_type}")
        part_data = part_item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if "type" not in part_data or part_data["type"] != "part":
            return
        part_id = part_data["id"]
        part_stl = self._onshape_api.export_part_stl(part_data["document_id"],part_data["workspace_id"],part_data["element_id"],part_data["id"])
        self._onshape_api.add_part_to_printbed(part_stl)

