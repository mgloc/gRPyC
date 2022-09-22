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
    return IsExist(type='file',path=filename,message_on_error='please make sure that the directory protos exist')

def IsService(service_name) :
    filename = SERVICES_PATH+service_name
    return IsExist(type='dir',path=filename,message_on_error=f'please make sure that the service directory {service_name} exist')

# CREATION

def createDirIfNotExisting(path,autoConvertToMs=True):
    if autoConvertToMs : path = standardPathToMs(path)
    os.system(f'if not exist "{path}" mkdir {path}')

def copyFile(startPath,endPath,autoConvertToMs=True) :
    if autoConvertToMs : startPath,endPath = standardPathToMs(startPath),standardPathToMs(endPath)
    os.system(f'copy /y {startPath} {endPath}')

def copyDefaultCompilation(service_name,destination_path) :
    pb2 = f"{SERVICES_PATH}{service_name}/pb2/{service_name}_pb2.py"
    pb2_grpc = f"{SERVICES_PATH}{service_name}/pb2/{service_name}_pb2_grpc.py"

    copyFile(pb2,destination_path)
    copyFile(pb2_grpc,destination_path)


# GETTERS

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

# CHECK IMPORTS

regexp = r"import \"(.*)\.proto\".*"

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

def compileService(service_name:str):
    try :
        IsService(service_name)
        IsProto(service_name)
    except :
        stopCompilation()

    servicePB2Path = SERVICES_PATH + service_name + "/pb2/"
    
    #Create PB2 file if not existing 
    createDirIfNotExisting(servicePB2Path)

    #Adding self to dependencies
    dependencies = [service_name]

    #Adding dependencies
    dependencies.extend(findImports(PROTO_PATH+service_name+".proto"))

    for dep in dependencies :
        os.system(f'python -m grpc_tools.protoc -I={PROTO_PATH} --python_out={servicePB2Path} --grpc_python_out={servicePB2Path} {dep}.proto')

def compileClient():
    """This function recompile every services and make them usable by the client"""
    #Create client dir if not existing
    createDirIfNotExisting(SERVICES_PATH+'client/')

    #Get services names
    servicesNames = listServicesNames(ignoreClient=True)

    for service in servicesNames :

        #Check if prototype exist
        try :
            IsProto(service)
        except FileNotFoundError :
            print(f"Unable to fetch prototype for the {service} service, skipping...")
            continue
        
        #If prototype exist recompile service
        compileService(service)

        clientSubServicePath = f"{SERVICES_PATH}client/{service}/"
        #Check if service dir in client exist
        createDirIfNotExisting(clientSubServicePath)

        #Copy compiled file into client sub folder
        copyDefaultCompilation(service_name=service,destination_path=clientSubServicePath)