# CIMC-KVM
## Description
cimc-kvm is a python tool to connect to old flash-based Cisco UCS CIMC (Cisco Integrated Management Controller) KVM console. Since Flash has been phased out this is the only way to connect.

## Tested
### CIMC side:
 - Cisco UCS C220M3 CIMC firmware v3
 - Should work on any M3 type servers with XML API

### Client side:
 - Windows Server 2019 with standard javaws
 - May not work on MacOS BigSur due to java error (can't help it)
 
 I could add some additional information later based on users input (if any)

## Requirements
1. Python v3 and all required libraries (see script import lines) https://www.python.org/downloads/
2. Java https://www.java.com

## Installation
1. Fulfil requirements
2. clone/download/copy-past script
3. run from terminal window (recommended)

## Other flavors
https://github.com/cdwlabs/cavalier
https://github.com/rohorner/pycimc
https://gist.github.com/ixs/3e305a34bd25e1b57b34cf222d6947e4

## Disclamier
1. This software provided as is and should be used on your own risk
2. I'm not a programmer and this is my first python code
3. Can't help. Especially beyond python side. Java is totally outside of the scope