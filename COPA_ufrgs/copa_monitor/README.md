# COPA monitor 
IMPORTANT: THIS TUTORIAL ASSUMES THAT YOU ALREADY INSTALLED COPA

All the next configuration steps need to be executed in the container-pools

## Install Requirements
First, you need to install psutil and libi2util-dev

psutil serves to passive measure CPU, virtual memory and network throughput.
libi2util-dev gives support to Owamp actively measure network one-way latency and jitter

```bash
sudo pip3 install psutil
sudo apt-get install libi2util-dev
```

## Install Owamp
Now you need to install owamp, that is the tool to measure the network link

Go to a folder where your user can run executables and download the owamp files.
```bash
wget http://software.internet2.edu/sources/owamp/owamp-3.4-10.tar.gz
```

Then, extract, configure, make and install

```bash
tar xzf owamp-3.4-10.tar.gz
cd owamp-3.4
./configure
make
sudo make install
```

## Start Owamp server
The owamp server needs to be started so the other pools can connect and measure the network link

```bash
sudo owampd -c $OWAMP_HOME/conf -v -U $USER -G $USER_GROUP
```

### Owamp server at startup
The owamp server can be set up to start at computer startup

This can be made by adding the command at "/etc/rc.local"

## Running copa monitor
To run copa monitor, first you need to execute COPA Web server at the COPA server.

```bash
cd $COPA_HOME/containers_site
python3 manage.py runserver 0.0.0.0:8000
```

After it, you need to execute at the Container Pools the monitor.py

```bash
cd $COPA_HOME/copa_monitor
python3 monitor.py
```

Now you just need to go at COPA Server and execute the monitor controller.py

```bash
cd $COPA_HOME/copa_monitor
python3 controller.py
```