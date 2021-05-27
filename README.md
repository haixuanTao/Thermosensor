# Summary
![dashboard](https://user-images.githubusercontent.com/22787340/119837720-231f6800-bf03-11eb-8004-db2c35e4462c.png)
![alerting](https://user-images.githubusercontent.com/22787340/119837712-2155a480-bf03-11eb-8efb-8da4848e4896.png)

This is a guide to install kubernetes, prometheus and grafana onto the raspberry-pi in
order to monitor temperature and ph for sake brewing.

- This setup can have up to 26 Temperature sensors and 8 PH sensor on one raspberry pi.

# Materials

- Raspberry Pi 4 - 8 Gb Ram
- DS18B20 Temperature sensor
- Blue PH Sensor 
- MCP3008 Analogic to Digital converter

# Modus Operandi

## SD Card

- Flash Raspberry image into SD Card from: https://www.raspberrypi.org/software/
- Change WIFI configuration following this: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
  - Consisting of creating a file called: `wpa_supplicant.conf` to `boot`.
  - Adding the following line:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=FR

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```

- Add an empty file called `ssh` to `boot` as well.
- Add `cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory` to the end of the file `/boot/cmdline.txt`
- Connect SD Card to Raspberry pi.

## WIFI

- Wait 5 Minutes.
- Check network with:

```
ping raspberrypi.local
```

- If it doesn't work, you have a network problem.
- If it works, it will look like this:

```
PING raspberrypi.local (192.168.43.87) 56(84) bytes of data.
64 bytes from raspberrypi (192.168.43.87): icmp_seq=1 ttl=64 time=7.51 ms
```

## SSH

- Connect on ssh with:

```
ssh pi@raspberrypi.local
```

- Password is: `raspberry` (to change password type `passwd`)
- If you see something like`pi@raspberrypi: ~ $`, Congrats, you're now developing on the raspberry-pi. 👯‍♀️👯‍♀️👯‍♀️

- Connect on ssh to raspberry-pi.
- type: `sudo raspi-config` in ssh console.
- Select Interfacing Options
- Select 1-Wire
- Select Yes
- Select Interfacing Options
- Select SPI
- Select Yes

The rest can be done directly by copying the content of `installation.sh` into the command line.

## Kubernetes

- Run the following cmd:

```bash
curl -sfL https://get.k3s.io | sh -
```

- check if eveything works with

```bash
sudo k3s kubectl get all
```

- To go faster, we will setup the alias `k`:

```bash
sudo chmod 666 /etc/rancher/k3s/k3s.yaml
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
alias k="kubectl"
echo 'alias k="sudo k3s kubectl"' >> ~/.bashrc
echo 'export KUBECONFIG=/etc/rancher/k3s/k3s.yaml' >> ~/.bashrc
```

- Check

```bash
k get all
```

- If it works, you now have kube 😛😛😛

## Helm

- Install helm:

```bash
wget https://get.helm.sh/helm-v3.5.4-linux-arm.tar.gz
tar xzvf helm-v3.5.4-linux-arm.tar.gz
sudo mv linux-arm/helm /usr/local/bin/
rm -rf linux-arm && rm helm-v3.5.4-linux-arm.tar.gz
```

- That's all 🍉🍉🍉

## Prometheus

- Install prometheus

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus-wakaze prometheus-community/prometheus
```

- To check access, let run the following command:

```
export POD_NAME=$(k get pods --namespace default -l "app=prometheus,component=server" -o jsonpath="{.items[0].metadata.name}")
k --namespace default port-forward $POD_NAME 9090
```

- Do an ssh port forwarding on a new local terminal:

```
ssh pi@raspberrypi.local -L 9090:localhost:9090
```

- And go to [localhost:9090](http://localhost:9090). If it works you now have a running prometheus instance. 🚀🚀🚀

- Configure prometheus with:

```
k edit configmap prometheus-wakaze-server
```

and add after `scrape_configs:` using the raspberry pi IP

```
    - job_name: sensor
      static_configs:
      - targets:
        - 192.168.1.29:8000
```

- then rescale prometheus:

```
k scale deploy prometheus-wakaze-server --replicas 0
k scale deploy prometheus-wakaze-server --replicas 1
```

## Grafana

```
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install grafana-wakaze grafana/grafana
```

- Then do this to get your password:

```
sudo iptables -w -P FORWARD ACCEPT
k get secret --namespace default grafana-wakaze -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

- This will print like so:

```
GKEuKnsmQm4NcoleieTXgauKt6VQhkIoME6Gtnpk
```

- Optionally add Metallb:

```
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.6/manifests/namespace.yaml
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.6/manifests/metallb.yaml
kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"
k delete svc grafana-wakaze
k expose deploy grafana-wakaze --type LoadBalancer
```

- Do an ingress forwarding with:

```
k apply -f https://raw.githubusercontent.com/haixuanTao/Thermosensor/master/grafana-ingress.yaml
```

- Try : raspberry.local on your browser and you should have a working Grafana 🍭🍭🍭

## Adding Prometheus DataSources

- Add a Data Source Prometheus. The http address is prometheus-wakaze-server.default.svc.cluster.local

## Temperature sensor

- Connect the red wire with `VCC` of breakout board.
- Connect the yellow wire with `DAT` of breakout board.
- Connect the black wire with `GND` of breakout board.
- You can add as many as 26 Thermo sensors in parallel.
- Connect breakout board with Raspberry as such:

  - VCC -> 3.3 V Pin
  - DAT -> GPIO4 Pin
  - GND -> GND Pin

- Connect on ssh to raspberry-pi.
- type: `sudo raspi-config` in ssh console.
- Select Interfacing Options
- Select 1-Wire
- Select Yes
- Select Interfacing Options
- Select SPI
- Select Yes
- `sudo reboot`

> Instructions at: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20

- Paste the following in the ssh console:

```bash
sudo modprobe w1-gpio
sudo modprobe w1-therm
sudo sh -c "echo 'w1_gpio' >> /etc/modules"
sudo sh -c "echo 'w1_therm' >> /etc/modules"
cd /sys/bus/w1/devices/
ls
# Check the name of the devices
cat /sys/bus/w1/devices/28-3c01d075f67c/w1_slave
```

- Expected output:

```
46 01 55 05 7f a5 81 66 52 : crc=52 YES
46 01 55 05 7f a5 81 66 52 t=20375
```

- If it work you now have a working thermo sensor 🔥🔥🔥

> For more details you can check instructions at: https://tutorials-raspberrypi.com/raspberry-pi-temperature-sensor-1wire-ds18b20/

## PH sensor

- To use the ph sensor you need an MCP3008 Analog to Digital converter.

- You should connect the MCP3008 as follows:

  - MCP3008 VDD to Raspberry Pi 3.3V
  - MCP3008 VREF to Raspberry Pi 3.3V
  - MCP3008 AGND to Raspberry Pi GND
  - MCP3008 DGND to Raspberry Pi GND
  - MCP3008 CLK to Raspberry Pi SCLK
  - MCP3008 DOUT to Raspberry Pi MISO
  - MCP3008 DIN to Raspberry Pi MOSI
  - MCP3008 CS/SHDN to Raspberry Pi CE0

- You should then connect the PH Sensor Pin as follows:

  - Red cable to RPI 5V
  - Black cable to RPI GND
  - Yellow cable to MCP3008 CH0

- Then do:

```bash
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus python-pip
sudo pip3 install adafruit-mcp3008
```

- To check if it was setupped properly you can paste the following

```
python3

# Wait for python to fire up

import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

print('Reading MCP3008 values, press Ctrl-C to quit...')
while True:
    values = mcp.read_adc(0)
    print(values)
    time.sleep(0.5)
```

> For more details you can check instructions at: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008

## Python Script

- Git clone the repo thermosensor and run it:

```
cd ~
git clone https://github.com/haixuanTao/Thermosensor
cd ~/Thermosensor
pip3 install -r requirement.txt
sudo cp thermosensor/client.service /etc/systemd/system/client.service
sudo systemctl start client.service
sudo systemctl enable client.service
```

- Check:
```
curl localhost:8000
lsof -i TCP:8000
```

- Everything is now set 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥

- Go to grafana
- Create a new dashboard and a new panel
- In metrics, type `phs`
- In an another panel, type `temperatures`
- You should now see data pouring in.
