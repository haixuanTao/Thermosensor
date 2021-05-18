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