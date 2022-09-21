# gRPyC : A lightweight framework to ease developpment of multiple-services using gRPC with python

(Support windows only for now)

## **File structuration :**

```
project
│   README.md
│   compilation.py   <- Main script to simplify gRPC for python
│   requirements.txt <- Dependencies for this project developpment
│
└───services
│   └───service1
│   │   └───data                <- Sample database
│   │   └───pb2                 <- Where the pb2 generated files will be
│   │   │   service1.py         <- The servicer class file
│   │   │   Dockerfile          <- To easily deploy the service later
│   │   │   requirements.txt    <- same
│   │
│   └───service2
│   └───...
│   │
│   └───client <- The client to rapidly test services
│       └───service1,2,...      <- pb2 for each service to be imported
│       │   client.py           <- The client to make requests
│
└───protos
│   │   service1.proto <- Proto files for service1
│   │   service2.proto
│   │   ...NB : A service name's is defined by the proto file name
│
└───venv <- We suggest you to use a virual environment

```

## **How to start :**

- Clone this repository
- Run these commands at the root of the project
- `python -m venv venv` (create a virtual environment)
- Get in your freshly made virtual environment, then execute :
- `python -m pip install -r requirements.txt` (install dependancies)
- #TODO specify commands to run using the scripts
