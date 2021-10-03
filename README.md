# CIMC-KVM
## Description
cimc-mgmt is a python tool to connect to old flash-based Cisco UCS CIMC (Cisco Integrated Management Controller) KVM console. Since Flash has been phased out this is the only way to connect.

## Tested
### CIMC side:
 - Cisco UCS C220M3 CIMC firmware v3
 - Should work on any M3 type servers with XML API

### Client side:
 - Windows Server 2019 with standard javaws
 - May not work on MacOS BigSur due to java error (can't help it)

## Requirements
1. Python v3 and all required libraries (see script import lines)
2. Java https://www.java.com

## Installation
1. Fulfil requirements
2. clone/download/copy-past script
3. run from terminal window (recommended)