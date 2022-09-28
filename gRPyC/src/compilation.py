import re
import os
import errno
import sys



PROTO_PATH = "./protos/"
SERVICES_PATH = "./services/"

def stopCompilation():
    print("Compilation stopped.")

def standardPathToMs(path:str):
    return path.replace("/","\\")

def printSeparator():
    print("-----------------------------------")

############################################# FILE CHECKS #############################################

# EXISTANCE
def IsExist(type,path,message_on_error=""):
    if type == 'file' :
        isit = os.path.isfile(path)
    elif type == 'dir':
        isit = os.path.isdir(path)
    else :
        raise ValueError(f"Argument 'type' must be 'dir' or 'file', '{type}' is incorrect")
    
    if not(isit) : raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT) + f" : {message_on_error} ",path)
    return isit

def IsProto(service_name) :
    filename = PROTO_PATH+service_name+".proto"
    return IsExist(type='file',path=filename,message_on_error=f"please make sure that the file '{service_name}.proto' is in the directory {PROTO_PATH}, or check the spelling of '{service_name}'")

def IsService(service_name) :
    filename = SERVICES_PATH+service_name
    return IsExist(type='dir',path=filename,message_on_error=f"please make sure that the service '{service_name}' has its directory at {SERVICES_PATH}{service_name}, or check the spelling of '{service_name}'")

# CREATION

def createDirIfNotExisting(path,autoConvertToMs=True):
    if not(os.path.exists(path)):
        print(f"creating {path} directory...")
        if autoConvertToMs : path = standardPathToMs(path)
        os.system(f'mkdir {path}')

def createFileIfNotExisting(path,autoConvertToMs=True):
    if not(os.path.exists(path)):
        print(f"creating {path} file...")
        if autoConvertToMs : path = standardPathToMs(path)
        os.system(f'type nul > {path}')

def copyFile(startPath,endPath,autoConvertToMs=True) :
    if autoConvertToMs : startPath,endPath = standardPathToMs(startPath),standardPathToMs(endPath)
    os.system(f'copy /y {startPath} {endPath}')

def copyDefaultCompilation(service_name,destination_path) :
    pb2 = f"{SERVICES_PATH}{service_name}/protos/{service_name}_pb2.py"
    pb2_grpc = f"{SERVICES_PATH}{service_name}/protos/{service_name}_pb2_grpc.py"

    print(f"Copying {service_name} pb2 generated files in client : {destination_path}")
    copyFile(pb2,destination_path)
    copyFile(pb2_grpc,destination_path)


# GETTERS
def listFiles(path) :
    fil = []
    obj = os.scandir(path=path)
    for entry in obj:
        if entry.is_file() :
            fil.append(entry)
    return fil

def listDirectories(path):
    dirs = []
    obj = os.scandir(path=path)
    for entry in obj:
        if entry.is_dir() :
            dirs.append(entry)
    return dirs

def listServicesNames(ignoreClient=True):
    dirs = list(map(lambda d: d.name,listDirectories(SERVICES_PATH)))
    if ignoreClient : dirs.remove('client')
    return dirs

def listProtosNames():
    dirs = list(map(lambda d: d.name.replace('.proto',''),listFiles(PROTO_PATH)))
    return dirs

# CHECK IMPORTS

regexp = r"import \"(?:protos\/)?(.*)\.proto\".*"

def findImports(filename:str):
    occ = []
    try :
        with open(filename) as f:
            for line in f:
                results = re.search(regexp, line.strip())
                if results :
                    occ.append(results.groups()[0])
            return occ
    except FileNotFoundError as e :
        raise e

############################################# COMPILATION #############################################

def compileProto(proto_name:str,outPath):
    try :
        IsProto(proto_name)
    except FileNotFoundError as e :
        print(e.strerror)
        stopCompilation()
        return False

    #Adding dependencies
    dependencies = [proto_name]
    dependencies.extend(findImports(PROTO_PATH+proto_name+".proto"))

    for dep in dependencies :
        os.system(f'python -m grpc_tools.protoc -I=. --python_out={outPath} --grpc_python_out={outPath} protos/{dep}.proto')
    
    return True

def compileService(service_name:str):
    try :
        IsService(service_name)
    except FileNotFoundError as e :
        print(e.strerror)
        stopCompilation()
        return False

    servicePath = SERVICES_PATH + service_name

    compileProto(proto_name=service_name,outPath=servicePath)

def compileClient():
    """This function recompile every services and make them usable by the client"""
    #Create client dir if not existing
    createDirIfNotExisting(SERVICES_PATH+'client/')

    #Get services names
    servicesNames = listServicesNames(ignoreClient=True)
    protosNames = listProtosNames()

    
    for service in servicesNames :
        printSeparator()
        #Check if prototype exist
        try :
            IsProto(service)
        except FileNotFoundError :
            print(f"Unable to fetch prototype for the {service} service, skipping...")
            continue
        
        #If prototype exist recompile service
        compileService(service)

        clientProtoPath = f"{SERVICES_PATH}client/"
        #Check if service dir in client exist
        createDirIfNotExisting(clientProtoPath+"protos/")

        #Copy compiled file into client sub folder
        copyDefaultCompilation(service_name=service,destination_path=clientProtoPath+"protos/")
    
    for protos in protosNames :
        if protos not in servicesNames :
            printSeparator()
            compileProto(protos,outPath=clientProtoPath)
            print(f"Compiling {protos}.proto in {clientProtoPath}")

    printSeparator()
    
    print("Done.")

def createService(service_name) :
    if service_name in listServicesNames(ignoreClient=False) :
        print("This service already exist, exiting...")
    
    service_name = service_name.casefold()

    # If service doesn't exist
    createDirIfNotExisting(SERVICES_PATH+service_name)
    createFileIfNotExisting(f"{SERVICES_PATH}{service_name}/{service_name}.py")
    createFileIfNotExisting(f"{PROTO_PATH}{service_name}.proto")



def runService(service_name):
    print(f"Running service {service_name}")
    os.system(f'cd {SERVICES_PATH}{service_name} && python {service_name}.py')