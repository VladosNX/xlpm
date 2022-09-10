# XLPM
Package manager for Linux
***
XLPM is easy package manager for Linux. It can work on all architectures!
## Installation
To install XLPM, run these commands:
> git clone https://github.com/vladosnx/xlpm

> sudo dpkg -i xlpm/xlpm.deb

## Usage
xlpm [OPTIONS]
* xlpm -i <file> - install package from file
* xlpm -r <package> - remove package
* xlpm -I <file> - get information about the package in the file

## Building XLP file
To build XLP-file:
* Create directory
* Add program to this directory
* Add config file to directory
* Run command: xlpm --build <directory-name>

### Creating config file
Config file has two values: package and version. Create file with name **xlp_config.json** and write:
{"name":"package_name","version":"program_version"}
