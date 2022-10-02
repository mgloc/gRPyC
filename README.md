# gRPyC : A lightweight framework to ease developpment of multiple-services using gRPC with python

(Support windows only for now)

## **File structuration :**

```
sample project
│   requirements.txt <- Dependencies for this project developpment
│
└───services
│   └───service1
│   │   └───data                <- Sample database .json
│   │   └───pb2                 <- Where the pb2 generated files will be
│   │   │   service1.py         <- The servicer class file
│   │   │   Dockerfile          <- To easily deploy the service later with Docker
│   │   │   requirements.txt    <- Used by Docker to install dependencies
│   │
│   └───service2
│   └───...
│   │
│   └───client  <- The client folder, NB : It is not a service, and you can't name a service 'client'
│       │          It is for testing your services only, you can delete it if you test your service with something else
│       └───protos              <- pb2 for each service will be also generated here
│       │   client.py           <- The client main script used to make requests to our services to test them
│
└───protos
│   │   service1.proto <- Proto file for service1
│   │   service2.proto <- Proto file for service2
│   │   base.proto     <- Proto file imported in other proto files, not representing a service
│   │   ...NB : A the service name should be the same than its proto file name
│
└───venv <- We suggest you to use a virual environment

```

## **How to start :**

- Create your 'protos' & 'services' directories
- Then run these commands (at the root of the project)
- `python -m venv venv` (create a virtual environment)
- Get in your freshly made virtual environment, then install grpyc :
- `pip install grpyc` ([PYPI](https://pypi.org/project/grpyc/))
- Now you can run `grpyc -ns myService1` to create a new service 

## Commands list

|Command|Description|
|---|---|
|-c, --compile-client         | Will compile all protos for each service and copy them into the client|
|-cs, --compile-service TEXT  | Will compile the given service|
|-s, --run-service TEXT       | Will run the given service|
|-ns, --new-service TEXT      | Will create a proto file and a dir for the service, run it with no text to create a client service|
|--help                       | Show help |

NB : These command must be executed at the root of your project, where your services and protos directories stand
