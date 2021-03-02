# https://github.com/Quixel/Bridge-Python-Plugin/blob/master/Python%202.7/ms_bridge_importer.py for the reference

#import guerilla 
import os, json, time, threading, socket, sys
from PySide import QtGui
from PySide.QtCore import QThread

#import guerilla_utils
import quixel_utils

from logger import Logger


host, port = "127.0.0.1", 24981


class MSToGuerillaWorker(QThread):


    def __init__(self):
        QThread.__init__(self)


    def __del__(self):
        self.wait()


    def process_data(self, data):
    # Utility function to process the array given by the MS importer
        Logger.message("Processing data")
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
        
        for item in processed_data : Logger.message("Processed %s" % item["Name"])

        Logger.message("Proceeding to Guerilla import")

        # TODO import in guerilla
        
        Logger.message("Restarting Bridge server")


    def run(self):
        time.sleep(0.1)

        try:
            Logger.message("Waiting for Bridge export")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, port))

            while True:
                sock.listen(5)
                client, addr = sock.accept()
                data = ""
                size = 4096*2
                data = client.recv(size)

                if data != "":
                    Logger.message("Receiving data")
                    self.TotalData = b""
                    self.TotalData += data

                    while True:
                        data = client.recv(4096*2)

                        if data : self.TotalData += data
                        else: break

                    Logger.message("Received data")
                    self.import_data(self.TotalData)
                    self.finished.emit()
                    break

        except:
            pass


class MSToGuerillaWindow():

    def __init__(self):
        
        app = QtGui.QApplication.instance()
        if app is None:
            app = QtGui.QApplication(sys.argv)
        thread = MSToGuerillaWorker()
        thread.start()