import os
import shutil
import requests
import webbrowser

# Color codes for console output
GREEN, RED, DEFAULT = '\033[32m', '\033[31m', '\033[0m'

# URLs for fetching data
ASSETS_URL = 'https://raw.githubusercontent.com/CroppingFlea479/Fleasion/main/assets.json'

def fetch_json(url):
    """Fetch JSON data from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"{RED}Error fetching data from {url}: {e}{DEFAULT}")
        return {}

def replace_files(files_to_delete, file_to_replace, folder_path):
    """Replace files in a specified folder."""
    try:
        copy_file_path = os.path.join(folder_path, file_to_replace)
        if os.path.exists(copy_file_path):
            for file_to_delete in files_to_delete:
                delete_file_path = os.path.join(folder_path, file_to_delete)
                if os.path.exists(delete_file_path):
                    os.remove(delete_file_path)
                else:
                    print(f"{RED}{file_to_delete} not found.{DEFAULT}")

            new_file_path = os.path.join(folder_path, file_to_replace)
            shutil.copy(copy_file_path, new_file_path)
            print(f"{GREEN}{file_to_delete} has been replaced with {file_to_replace}.{DEFAULT}")
        else:
            print(f"{RED}{file_to_replace} not found.{DEFAULT}")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{DEFAULT}")

def create_bloxstrap_folders(base_path, folders):
    """Create necessary Bloxstrap folders."""
    for folder in folders:
        path = os.path.join(base_path, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created folder: {path}")
        else:
            print(f"Folder already exists: {path}")
    print(f"All folders created successfully! Import your skyboxes into the opened folder.")
    os.startfile(path)

def clear_cache(folder_path):
    """Delete all files in the specified folder."""
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"{RED}The directory {folder_path} does not exist.{DEFAULT}")

# Fetch asset data
data = fetch_json(ASSETS_URL)
folder_path = os.path.join(os.getenv('TEMP'), 'roblox', 'http')

while True:
    # Check for required cache files
    mod_cache_path = os.path.join(folder_path, '016a313606e2f99a85bb1a91083206fc')
    pf_cache_path = os.path.join(folder_path, '8a7090ac9b2e858f4aee9e19a0bfd562')

    mod_cache = os.path.exists(mod_cache_path)
    pf_cache = os.path.exists(pf_cache_path)

    if not mod_cache:
        print(f"{RED}Modding cache missing.{DEFAULT}")
        webbrowser.open_new_tab("https://www.roblox.com/games/18504289170/texture-game")
    if not pf_cache:
        print(f"{RED}PF cache missing.{DEFAULT}")
        webbrowser.open_new_tab("https://www.roblox.com/games/292439477/Phantom-Forces")

    if not (mod_cache and pf_cache):
        continue

    menu = input(
        f"Enter the number corresponding to what you'd like to do:\n"
        f"1: {GREEN}Change Skyboxes{DEFAULT}\n"
        f"2: {GREEN}Clear Cache{DEFAULT}\n"
        f"3: {GREEN}Exit{DEFAULT}\n: "
    ).strip()

    if menu == '1':
        base_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Bloxstrap', 'Modifications')
        folders = ["PlatformContent", "pc", "textures", "sky"]
        create_bloxstrap_folders(base_path, folders)
        replace_files(data.get("skyboxes", []), 'd625adff6a3d75081d11b3407b0b417c', folder_path)

    elif menu == '2':
        confirm = input(
            f"\n{RED}Warning: This will fully reset all tweaks and anything loaded from any game.\n"
            f"Type 'done' to proceed, anything else will cancel.{DEFAULT}"
        ).strip()
        if confirm.lower() == "done":
            clear_cache(folder_path)
            print(f"Cache cleared. Please rejoin the relevant experiences.\n")
        else:
            print(f"Operation cancelled.")

    elif menu == '3':
        print(f"\nExiting the program.")
        break

    else:
        print(f"Invalid option, please enter a corresponding number!")
