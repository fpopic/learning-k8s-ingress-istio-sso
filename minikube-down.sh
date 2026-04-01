#!/bin/bash

set -euo pipefail

kubectl delete -f k8s/1.namespace.yaml
minikube addons disable ingrees
minikube stop
