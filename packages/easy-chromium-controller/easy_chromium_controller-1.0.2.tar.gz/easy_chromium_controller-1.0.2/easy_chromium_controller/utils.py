import os
import wget
import psutil
import zipfile

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
def Log(*args, **kwargs):
    print("🌐  >> " + "".join(map(str, args)), **kwargs)

def Input(start_of_line: str = ""):
    return input("🌐  >> " + start_of_line)

def KillAllChromiumProcessOnWindows():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if 'chromium.exe' in process.info['name']:
            try:
                psutil.Process(process.info['pid']).terminate()
            except Exception as e:
                pass

def KillAllChromiumProcessOnLinux():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if 'chromium' in process.info['name']:
            try:
                psutil.Process(process.info['pid']).terminate()
            except Exception as e:
                pass

def check_binary_files_istalled(binary_folder: str, path_to_driver : str):
    try:
        with open(binary_folder+path_to_driver, "r") as f:
            pass
    except Exception as e:
        try:
            Log("Binary files not installed, installing...")
            if os.path.isdir(binary_folder):
                os.rmdir(binary_folder)
            os.mkdir(binary_folder)
            # Descargar de github el archivo .zip
            if "linux" in path_to_driver:
                wget.download("https://github.com/gonfdez/easy_chromium_controller/releases/download/bin/linux.zip", binary_folder+"/linux.zip")
            else:
                wget.download("https://github.com/gonfdez/easy_chromium_controller/releases/download/bin/win.zip", binary_folder+"/win.zip")
            # Descomprimir el archivo .zip
            with zipfile.ZipFile(binary_folder+"/win.zip", 'r') as zip_ref:
                zip_ref.extractall(binary_folder)
            # Eliminar el archivo .zip
            os.remove(binary_folder+"/win.zip")
            print('')
            Log("¡ Binary files installed !")
        except FileNotFoundError as e:
            raise Exception("Binary folder path is not valid.")
        