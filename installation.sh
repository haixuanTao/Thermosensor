curl -sfL https://get.k3s.io | sh -
sudo chmod 666 /etc/rancher/k3s/k3s.yaml
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
alias k="kubectl"
echo 'alias k="sudo k3s kubectl"' >> ~/.bashrc
echo 'export KUBECONFIG=/etc/rancher/k3s/k3s.yaml' >> ~/.bashrc


wget https://get.helm.sh/helm-v3.5.4-linux-arm.tar.gz
tar xzvf helm-v3.5.4-linux-arm.tar.gz
sudo mv linux-arm/helm /usr/local/bin/
rm -rf linux-arm && rm helm-v3.5.4-linux-arm.tar.gz


helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus-wakaze prometheus-community/prometheus


helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install grafana-wakaze grafana/grafana

kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.6/manifests/namespace.yaml
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.6/manifests/metallb.yaml
kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"
k delete svc grafana-wakaze
k expose deploy grafana-wakaze --type LoadBalancer
k apply -f https://raw.githubusercontent.com/haixuanTao/Thermosensor/master/grafana-ingress.yaml

sudo modprobe w1-gpio
sudo modprobe w1-therm
sudo sh -c "echo 'w1_gpio' >> /etc/modules"
sudo sh -c "echo 'w1_therm' >> /etc/modules"
cd /sys/bus/w1/devices/
ls


cd ~
git clone https://github.com/haixuanTao/Thermosensor
cd ~/Thermosensor
pip3 install -r requirement.txt
sudo cp thermosensor/client.service /etc/systemd/system/client.service
sudo systemctl start client.service
sudo systemctl enable client.service