Modus Operandi

## SD Card

- Flash Raspberry image into SD Card from: https://www.raspberrypi.org/software/
- Change WIFI configuration following this: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
  - Consisting of creating a file called: `wpa_supplicant.conf` to `boot`.
  - Adding the following line:

```
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

- Password is: `raspberry`
- If you see something like`pi@raspberrypi: ~ $`, Congrats, you're now developing on the raspberry-pi. 👯‍♀️👯‍♀️👯‍♀️

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

## Grafana

```
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install grafana-wakaze grafana/grafana
```

- Then do this to get your password:

```
k get secret --namespace default grafana-wakaze -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

- This will print like so:

```
SKoOd6Lm3QISd9nfpyeTT9SfzjyOkwyZJ7ujaE6r
```

- Do an ssh port forwarding tp

```
export POD_NAME=$(k get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana-wakaze" -o jsonpath="{.items[0].metadata.name}")
k --namespace default port-forward $POD_NAME 3000
```

- Working Grafana 🍭🍭🍭

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
- `sudo reboot`

> Instructions at: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20

- Paste the following in the ssh console:

```bash
sudo modprobe w1-gpio
sudo modprobe w1-therm
sudo nano /etc/modules
echo 'w1_gpio' >> /etc/modules
echo 'w1_therm' >> /etc/modules
cd /sys/bus/w1/devices/
# Check the name of the devices
ls
cat /sys/bus/w1/devices/28-3c01d075f67c/w1_slave
```

- Expected output:

```
46 01 55 05 7f a5 81 66 52 : crc=52 YES
46 01 55 05 7f a5 81 66 52 t=20375
```

- If it work you now have a working thermo sensor 🔥🔥🔥

> For more details you can check instructions at: https://tutorials-raspberrypi.com/raspberry-pi-temperature-sensor-1wire-ds18b20/
