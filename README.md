# kubernetes-two-service-template

A small **two-service Kubernetes sample project** for job hunting and portfolio use.

This template uses only these local tools:

- **Docker**
- **kind**
- **kubectl**

The project contains two services:

- **backend**: FastAPI API
- **frontend**: Nginx-based static web app that calls the backend through `/api`

The frontend is exposed to your host machine. The backend stays inside the cluster and is reached through the frontend's reverse proxy.

## What this project demonstrates

- building separate Docker images for frontend and backend
- running multiple services in Kubernetes
- internal service-to-service communication
- exposing only the frontend to the host with `NodePort`
- using `ConfigMap` and `Secret`
- organizing manifests with Kustomize `base` and `overlays`
- using health checks for the backend

## Prerequisites

Install these tools locally:

- Docker
- kind
- kubectl

No local Python installation is required.

## Docker-only local run

Create a dedicated Docker network:

```bash
docker network create project_network
```

Build both images:

```bash
docker build -t backend:local ./backend
docker build -t frontend:local ./frontend
```

Run the backend first:

```bash
docker run -d   --name backend   --network project_network   -e APP_NAME=backend   -e APP_ENV=docker   -e APP_VERSION=0.1.0   -e GREETING="Hello from Docker backend"   -e API_TOKEN=local-token   backend:local
```

Run the frontend next:

```bash
docker run -d   --name frontend   --network project_network   -e FRONTEND_API_ORIGIN=http://backend:8000   -p 8080:80   frontend:local
```

Open the app:

```text
http://localhost:8080/
```

The frontend sends `/api/*` requests to the backend through Nginx.

Stop and remove the containers when you are done:

```bash
docker rm -f frontend backend
docker network rm project_network
```

## Kubernetes local run with kind

### 1. Build both images

```bash
docker build -t backend:local ./backend
docker build -t frontend:local ./frontend
```

### 2. Create the kind cluster

```bash
kind create cluster --name k8s-sample --config kind-config.yaml
```

### 3. Load both images into kind

```bash
kind load docker-image backend:local --name k8s-sample
kind load docker-image frontend:local --name k8s-sample
```

### 4. Apply the manifests

```bash
kubectl apply -k k8s/overlays/local
```

### 5. Check the resources

```bash
kubectl get all -n sample-app
kubectl get configmap,secret -n sample-app
kubectl describe deployment backend -n sample-app
kubectl describe deployment frontend -n sample-app
```

### 6. Access the frontend

This template maps kind `NodePort 30080` to host port `8080`.

```text
http://localhost:8080/
```

You can also test the proxied backend route:

```bash
curl http://localhost:8080/api/
curl http://localhost:8080/api/healthz
```

## Delete the cluster

```bash
kind delete cluster --name k8s-sample
```
