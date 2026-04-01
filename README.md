# learning-minikube-ingress-nginx

## How to run

Environment
- m1 macOs
- minikube version: v1.27.0

Run [./minikube-up.sh](./minikube-up.sh) to spin up and [./minikube-down.sh](./minikube-down.sh) to stop everything.

## Key Concepts

To understand how these pieces fit together, here is the purpose of each resource in the `k8s/` directory:

### 1. Namespace (`1.namespace.yaml`)
- **Purpose**: Creates a logical "box" to isolate your application. 

### 2. UI Deployment (`2.ui-deployment.yaml`)
- **Purpose**: Manages the lifecycle of your **Pods** (the actual containers running your code). It ensures the desired number of containers are running and handles updates/rollbacks.
- **Key Part**: The `template` section defines what the Pod looks like, and the `labels` allow others to find it.

### 3. UI Service (`3.ui-service.yaml`)
- **Purpose**: Provides a **stable entry point** (IP/DNS name) for a group of Pods. Since Pods can die and restart with new IPs, the Service acts as a permanent "front door."
- **How it works**: It uses a **Selector** (e.g., `app: ui`) to find and load-balance traffic across all Pods that have the matching label.

### 6. Ingress (`6.ingress-resource.yaml`)
- **Purpose**: Acts as the **Smart Gateway** (L7 Load Balancer) that allows external traffic from the internet into your cluster.
- **Features**: It handles domain-based routing (e.g., `my-web.com`), SSL/TLS termination, and path-based routing (e.g., `/api` vs `/`).
- **Connection**: It points to the **Service** by its literal `name` (e.g., `svc-web`).

### The "Glue": Labels & Selectors
- **Labels** are key-value pairs (like `app: hello`) attached to resources like Pods.
- **Selectors** are "search queries" used by Deployments and Services to find those labeled Pods.
- **Connection Rule**: For a Service to talk to a Pod, the Service's `selector` **must** match the Pod's `label`. **Note**: Metadata labels on Deployments and Services themselves are optional and often omitted if not needed for organizational purposes.

## Extensions: FastAPI API

We extended the setup with a simple FastAPI application to demonstrate path-based routing in the Ingress. This is a standard **Dockerized** setup.

- **`api/Dockerfile`**: A modern Docker image using **`uv`** (a high-performance Rust-based Python package manager) for near-instant dependency resolution and installation.
- **Deployment (`4.api-deployment.yaml`)**: Runs the `hello-api:latest` image.
- **Service (`5.api-service.yaml`)**: An internal Service (`ClusterIP`) that exposes the API within the cluster.
- **Ingress Update**: The Ingress now routes traffic:
  - `my-web.com/api/*` → `svc-api`
  - `my-web.com/*` → `svc-web`

### Building for Minikube

Since we are running in Minikube, you must build the image directly in the Minikube Docker daemon so that the cluster can find it:

```bash
# Point your shell to Minikube's Docker daemon
eval $(minikube -p minikube docker-env)

# Build the image from the project root
docker build -t hello-api:latest ./api
```

**Available Endpoints**:
- `http://my-web.com/api/users`
- `http://my-web.com/api/payments`

## Learning resources

Ingress learning resources

- https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/
- https://cloud.google.com/kubernetes-engine/docs/tutorials/http-balancer#deploying_a_web_application
- https://www.youtube.com/watch?v=GhZi4DxaxxE&ab_channel=KodeKloud
- https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/tree/main/load-balancing
- https://cloud.google.com/kubernetes-engine/docs/tutorials

Minikube learning resources

- https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns/
- https://medium.com/@Oskarr3/setting-up-ingress-on-minikube-6ae825e98f82#:~:text=any%20other.-,Setup,-Minikube%20v0.14.0%20(and
