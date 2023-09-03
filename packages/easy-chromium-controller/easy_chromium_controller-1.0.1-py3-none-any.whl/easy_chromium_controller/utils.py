import psutil

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
def Log(*args, **kwargs):
    print("🌍   >> " + "".join(map(str, args)), **kwargs)

def Input(start_of_line: str = ""):
    return input("🌍   >> " + start_of_line)

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