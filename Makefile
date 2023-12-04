# Default target
all: install-helm init-helm-repo install-python-packages

# Target for installing dependencies
deps: install-helm init-helm-repo install-python-packages
    # Add other dependency installation commands here

# Target for installing HELM
install-helm:
	curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
	sudo apt-get install apt-transport-https --yes
	echo "deb [arch=$$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
	sudo apt-get update
	sudo apt-get install helm

# Target for initializing Helm chart repository and installing Fluent Bit
init-helm-repo:
	helm repo add fluent https://fluent.github.io/helm-charts
	helm upgrade --install fluent-bit fluent/fluent-bit

# Target for installing Python packages
install-python-packages:
	pip install requests
	pip install kubernetes

# Target for cleaning up
clean:
	rm -f $(OBJS) $(TARGET)

# Phony targets
.PHONY: all deps install-helm init-helm-repo install-python-packages clean

