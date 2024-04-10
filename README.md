# MPLS Network Automatic Configuration Project

## Project Introduction
This project implements automatic configuration of network devices in an MPLS network environment simulated by GNS3, using a Python script. The `conf.py` script is primarily used, based on the network configuration parameters defined in `config.json`, to automate the configuration of routers.

## Features
- **Automation**: By reading the `config.json` configuration file, configuration scripts for routers within the network are generated automatically.
- **Support for Multiple Network Devices**: Capable of configuring various network services according to the role of different routers (such as PE, P, CE) and their interfaces, including OSPF, BGP, VRF, etc.
- **Configuration Backup**: The generated configuration scripts are saved in corresponding files for easy tracking and management.

## How to Use
1. Ensure that Python and the necessary libraries are installed in your environment.
2. Prepare `config.json` by filling in the configuration parameters according to your network design.
3. Run the `conf.py` script.

## Network Architecture
The supported network architecture includes, but is not limited to:

- A main AS containing PE and P routers, connected to VPN and internet clients.
- Configuration of OSPF, MPLS, BGP VPNv4, and VRFs on VPN client interfaces for VPN traffic transmission.

## File Descriptions
- `conf.py`: The main Python script for automating the configuration of routers. It reads the configuration parameters from `config.json` and generates router configuration scripts accordingly.
- `config.json`: Contains the configuration parameters for routers within the network, serving as the input for `conf.py` to automate the network setup.
- `i1_startup-config.cfg` to `i8_startup-config.cfg`: These are the generated configuration files for each router (from i1 to i8) in the network. The `conf.py` script produces these files based on the specifications provided in `config.json`, automating the setup process for each router.
- `Topology.png`: A screenshot image that visually represents the network topology. This aids in understanding the network layout and how different network devices are interconnected.

## Contributors
This project was made possible thanks to the efforts and contributions of the following individuals:
- AHRIOUI Younes
- BARTOSIK Johan
- BENDIMERED Fadia
- MORTIER Paul
- VAUDEY Rémy
- ZHU Kuangyun

