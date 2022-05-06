# M1if20_IDEFIX

Projet transversal innovant 

## Requirements
#### On Raspberry Pi
- PiCamera
- Python 3
- CV2 (for Python)
- Camera Module

#### On PC
- Python3

... and (of course) an Internet connection.

## How to use
First, change the IP address and port of the PC and the Raspberry Pi in `raspi.py` and `config-manager.py`, respectively.

Second, use these commands to run the scripts:
#### On Raspberry Pi
```bash
python3 raspi.py
```

#### On PC
```bash
python3 config-manager.py
```

## How to connect to your Raspberry Pi using SSH
To access your Raspberry Pi remotly using SSH follow these instructions :
- Enable SSH in `raspi-config`
- Use the following command to find out the IP address of your Raspberry Pi:
```bash
hostname -I
```
- Type the following command in your terminal : 
```bash
ssh [username]@[ip address]
``` 
- Enter your `username` and `password`
- Use `-Y` with the SSH command to have access to the Camera Module 

## Project structure (WIP)
```
.
├── config-manager.py               (Main script PC side)
├── raspi.py                        (Main script Raspberry Pi side)
├── doc                             (Project documentation)
├── src                             (Core source code)
│       ├── com                     (Manages tcp communication between PC and Raspberry Pi)
│       │       ├── camserver.py    
│       │       ├── receiver.py
│       │       └── tcpcom          (TCP communincation library)
│       ├── entity                  (Manages placements and strategies of robots)
│       │       ├── chat.py
│       │       ├── robot.py
│       │       └── souris.py
│       ├── config.py               (Contains the values for Camera Module configuration)
│       └── utils.py                (Contains utility fonctions)
└── tdm-python                      (TDM client Python module)
├── README.md
```

## Developers : 
* ABDRABO Khaled p1713323
* BOUDJEMA Bilal p2111858
* GUILLARDEL Thomas p1612078
* SERVAGENT Anthony p1709447

