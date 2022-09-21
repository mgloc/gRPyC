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
│   │   └───data                <- Sample database .json
│   │   └───pb2                 <- Where the pb2 generated files will be
│   │   │   service1.py         <- The servicer class file
│   │   │   Dockerfile          <- To easily deploy the service later with Docker
│   │   │   requirements.txt    <- Used by Docker to install dependencies
│   │
│   └───service2
│   └───...
│   │
│   └───client                  <- The client folder, NB : It is not a service, and you can't also name a service client
│       └───service1,2,...      <- pb2 for each service to be imported
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

- Clone this repository
- Run these commands at the root of the project
- `python -m venv venv` (create a virtual environment)
- Get in your freshly made virtual environment, then execute :
- `python -m pip install -r requirements.txt` (install dependancies)
- #TODO specify commands to run using the scripts
