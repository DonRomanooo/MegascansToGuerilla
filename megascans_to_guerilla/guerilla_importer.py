# https://github.com/Quixel/Bridge-Python-Plugin/blob/master/Python%202.7/ms_bridge_importer.py for the reference

#import guerilla 
import os, json, time, threading, socket, sys
from PySide import QtGui
from PySide.QtCore import QThread, Signal

#import guerilla_utils
import quixel_utils

from logger import Logger


host, port = "127.0.0.1", 24981


class MSToGuerillaWorker():

    def process_data(self, data):
    # Utility function to process the array given by the MS importer
        msg = Logger.message("Processing data")
        json_data = json.loads(data)
        imported_assets = []

        for j_data in json_data:
            tex_data = {}
            for item in j_data["components"]:
                if "path" in item:
                    tex_data[item["type"].capitalize()] = item["path"]

            geo_data = []
            for item in j_data["meshList"]:
                if "path" in item:
                    geo_data.append(item["path"])

            new_data = {
                "Name" : j_data["name"],
                "Path" : j_data["path"],
                "Textures" : tex_data,
                "Geometry" : geo_data
            }

            imported_assets.append(new_data)

        return imported_assets
        
      
    def import_data(self, data):
        # Utility function to import the data in guerilla
        # whether it's geometry or a surface
        processed_data = self.process_data(data)
        
        for item in processed_data: 
            msg = Logger.message("Processed %s" % item["Name"])

        msg = Logger.message("Proceeding to Guerilla import")

        # TODO import in guerilla
        
        msg = Logger.message("Restarting Bridge server")
