# M1if20_IDEFIX

Projet transversal innovant 

## Requirements
#### On PC
- Python3

#### On Raspberry Pi
- PiCamera
- Python 3
- OpenCV2 (for Python)
- Camera Module

... and (of course) an Internet connection.

## How to use
First, change the IP address and port of the PC and the Raspberry Pi in `raspi.py` and `main.py` (or `config-manager.py`), respectively.

Second, use these commands to run the scripts:
#### On PC
```bash
python3 main.py
```

#### On PC 
(if you are testing sending coordinates from raspi to pc without robot connection))
```bash
python3 config-manager.py
```

#### On Raspberry Pi
```bash
python3 raspi.py
```
The PC and Raspberry Pi will connect using the Wi-Fi connection.
The PC will start by sending the Configuration Json. The Raspberry Pi proceeds to respond either positively or negatively depending on the
format of the Json Object. If the Configuration Json is correctly formatted, the camera feed (with the robot detection) will open 
on your Raspberry Pi. Then, it will start transmitting the coordinates of the detected robots to your PC.


## How to connect to your Raspberry Pi using SSH
To access your Raspberry Pi remotely using SSH follow these instructions :
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

In our case (example) :
```bash
ssh -Y pi@[ip address]
```


## Project structure (WIP)
```

.
├── main.py                         (Main script PC side)
├── config-manager.py               (Camera and connection test script PC side)
├── raspi.py                        (Main script Raspberry Pi side)
├── src                             (Core source code)
│       ├── com                     (Manages tcp communication between PC and Raspberry Pi)
│       │       ├── camserver.py    (using Camera Module with OpenCV to detect Robots) 
│       │       ├── receiver.py     (Receive configuration raspi side and coordinates on pc) 
│       │       └── tcpcom          (TCP communincation library)
│       ├── Coord.py                
│       ├── old                     
│       │   ├── multiCo.py
│       │   └── test.py
│       ├── config.py               (Contains the values for Camera Module configuration)
│       ├── IA.py                   (Manages placements and strategies of robots)
│       ├── Robot.py                (Robot Entity)
│       ├── TestCoord.py            
│       └── utils.py                (Contains utility fonctions)
├── doc                             (Project 'draft' documentation)
├── tdm-python                      (TDM client Python module)
└── README.md                       (You're here!)
```


## Developers : 
* ABDRABO Khaled p1713323
* GUILLARDEL Thomas p1612078
* SERVAGENT Anthony p1709447
