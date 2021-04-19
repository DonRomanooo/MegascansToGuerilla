import os, sys, json

from utils.logger import Logger


def initialize_preferences(bridge_path, megascans_folder_path):
    # Initializes the pref file with different utilities path
    # and an empty list for last used assets
    preferences = { 
        "bridge_app_path" : bridge_path, 
        "megascans_folder_path" : megascans_folder_path,
        "last_used" : []
    }


def load_quixel_folders(megascans_path):
    # Load all the available folders for each category
    # of scanned data
    download_folder = megascans_path + "/Downloaded"
    data = []

    if not os.path.exists(download_folder):
        Logger.error("Download folder not found")
        return

    for folder in os.listdir(download_folder):
        if os.path.isdir(os.path.join(download_folder, folder)):
            folder_data = { 
                "Name" : folder,
                "Data" : [] 
                }
        
            for subfolder in os.listdir(os.path.join(download_folder, folder)):
                # we want to manipulate the string to get rid of the id character chain at the end
                if os.path.isdir(os.path.join(download_folder, folder, subfolder)):
                    asset_name = subfolder.split("_")
                    asset_name = "{0} {1}".format(asset_name[0].capitalize(), asset_name[1].capitalize())

                    asset_path = os.path.join(download_folder, folder, subfolder)

                    asset_preview = ""

                    for file in os.listdir(asset_path):
                        if "Preview" in file:
                            asset_preview = asset_path + "/" + file

                    if asset_preview == "":
                        Logger.warning("No preview found for %s" % asset_name)    
                    
                    folder_data["Data"].append({
                        "Name" : asset_name,
                        "Path" : asset_path,
                        "Preview" : asset_preview
                    })

            data.append(folder_data)

    return data        


def load_textures(folder_path):
    # Load all textures from a directory
    # into a dict with maps types and paths
    tex_dict = {
        "Albedo" : "",
        "Bump" : "",
        "Displacement" : "",
        "Normal" : "",
        "Roughness" : "",
        "Translucency" : "",
        "AO" : "",
        "Cavity" : "",
        "Gloss" : "",
        "Opacity" : "",
        "Specular" : "",
        }

    for item in os.listdir(folder_path):
        
        if "Albedo" in item:
            tex_dict["Albedo"] = os.path.join(folder_path, item)
        if "Displacement" in item and "exr" in item:
            tex_dict["Displacement"] = os.path.join(folder_path, item)
        if "Normal" in item:
            tex_dict["Normal"] = os.path.join(folder_path, item)
        if "Roughness" in item:
            tex_dict["Roughness"] = os.path.join(folder_path, item)
        if "Translucency" in item:
            tex_dict["Translucency"] = os.path.join(folder_path, item)
        if "Opacity" in item:
            tex_dict["Opacity"] = os.path.join(folder_path, item)
     
    return tex_dict

