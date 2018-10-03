# Setting up COPA Container Pools with Live Migration #

* Tested on Ubuntu 16.04.3 LTS

## Dependencies ##

Make sure your system is up to date:

```bash
sudo apt update
sudo apt dist-upgrade -y
```

### Kernel ###

```bash
sudo apt install -y  linux-headers-4.8.0-54-generic linux-headers-4.8.0-54 linux-image-4.8.0-54-generic linux-image-extra-4.8.0-54-generic
```

### Bridge ###

```bash
sudo apt install -y bridge-utils avahi-daemon -y
```

### Criu ###

```bash
sudo apt install build-essential libc6-dev-i386 gcc-multilib libprotobuf-dev libprotobuf-c0-dev protobuf-c-compiler protobuf-compiler python-protobuf pkg-config python-ipaddr libbsd-dev iproute2 libcap-dev libnl-3-dev libnet-dev asciidoc -y
```

## Setting the Bridge for containers ##

Edit the `/etc/network/interfaces` file, comment (or remove) the main interface declaration and add the following:

```
auto br0
iface br0 inet dhcp
    bridge_ports <MAIN_INTERFACE_NAME>
```

Then edit the `/etc/sysctl.conf` file to enable IPV4 automatic packet forwarding:

```
net.ipv4.ip_forward=1
```

## Setting up LXD and Criu ##
Remove previously installed packages:

```bash
sudo apt purge lxc* lxd* criu* -y

sudo reboot  # To unload kernel features
```
Then find the remaining LXD files and remove them:

```bash
sudo find / -name *lxd*
# REMOVE ALL FILES RELATED TO LXD

sudo find / -name *lxc*
#REMOVE ALL FILES RELATED TO LXC
```

### Compile and install Criu 3.1 ###

```bash
tar -xf criu-3.1.tar.bz2
cd criu-3.1
make clean
make
sudo make install
```

### Install LXD 2.0.9 ###
Find the Debian packages in the copa-dependencies folder and install them using:

```bash
sudo dpkg -i lxd_2.0.9-0ubuntu1-14.04.1_amd64.deb lxd-client_2.0.9-0ubuntu1-14.04.1_amd64.deb  #This will produce an error (missing dependencies).

sudo apt install -f -y  # To fix the dependencies error

sudo dpkg -i lxd_2.0.9-0ubuntu1-14.04.1_amd64.deb lxd-client_2.0.9-0ubuntu1-14.04.1_amd64.deb  # To Downgrade LXD to the correct version.
```

Then do the initial configuration of LXD:

```bash
sudo lxd init
```

* Create new storage pool [dir]
* Make acessible to network
* Create new container bridge
    * Create lxdbr0
    * DO NOT CONFIGURE IP4 or IP6 SUBNET

Edit the default profile of LXC containers with `sudo lxc profile edit default` to use the bridge `br0` created previously. In the end, if should look like this:

```
config: {}
description: Default LXD profile
devices:
  eth0:
    name: eth0
    nictype: bridged
    parent: br0
    type: nic
name: default
```

Now disable the bridge created by the `lxd init` command on the `/etc/default/lxd-bridge` file:

```
USE_LXD_BRIDGE="false"
UPDATE_PROFILE="false"
```
Reboot to apply.

## Adding new container servers ##

```
sudo lxc remote add <SERVER_NAME> <SERVER_IP>
```

## Container live migration ##
### Default image ###

Due to problems with `apparmor`, use the image `ubuntu:315bedd32580` to create your containers.

```
sudo lxc launch ubuntu:315bedd32580 my-container
```

### Live Container Migration ###
To migrate, use the `move` command. Make sure to have both `source` and `destination` servers added to your `lxc remote` list.

```
sudo lxc move <SOURCE>:my-container <DESTINATION>:my-container
```
