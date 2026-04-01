# [kubernetes_project_template](https://github.com/europanite/kubernetes_project_template "kubernetes_project_template")

[![Validate Kubernetes Manifests](https://github.com/europanite/kubernetes_project_template/actions/workflows/validate-k8s-manifests.yml/badge.svg)](https://github.com/europanite/kubernetes_project_template/actions/workflows/validate-k8s-manifests.yml)
[![pages](https://github.com/europanite/kubernetes_project_template/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/europanite/kubernetes_project_template/actions/workflows/pages/pages-build-deployment)

A small project that supports both **Docker Compose** and **Kubernetes**.

[![Validate Kubernetes Manifests](https://github.com/europanite/kubernetes_project_template/actions/workflows/validate-k8s-manifests.yml/badge.svg)](https://github.com/europanite/kubernetes_project_template/actions/workflows/validate-k8s-manifests.yml)
[![pages](https://github.com/europanite/kubernetes_project_template/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/europanite/kubernetes_project_template/actions/workflows/pages/pages-build-deployment)

## Stack

- **backend**: FastAPI
- **frontend**: Nginx serving static files and proxying `/api` to `backend`
- **local development** and **Kubernetes**

## Prerequisites

For local use:

- Docker
- Docker
- kind
- kubectl

## Run with Docker Compose

Normal run:

```bash
docker compose -f docker-compose.yaml up --build
```

Test-style override run:

```bash
docker compose -f docker-compose.yaml -f docker-compose.test.yaml up --build
```

Open:

```text
http://localhost:8080/
```

Test the backend through the frontend proxy:

```bash
curl http://localhost:8080/api/
curl http://localhost:8080/api/healthz
```

Stop everything:

```bash
docker compose -f docker-compose.yaml down
```

If you started the test override stack, stop it with:

```bash
docker compose -f docker-compose.yaml -f docker-compose.test.yaml down
```

## Run with Kubernetes (kind)

Build images:

```bash
docker build -t backend:local ./backend
docker build -t frontend:local ./frontend
```

Create the cluster:

```bash
kind create cluster --name cluster --config kind-config.yaml
```

Load images into kind:

```bash
kind load docker-image backend:local --name cluster
kind load docker-image frontend:local --name cluster
```

Apply manifests:

```bash
kubectl apply -k k8s/overlays/local
```

Check resources:

```bash
kubectl get all -n app
```

Open:

```text
http://localhost:8080/
```

Delete the cluster:

```bash
kind delete cluster --name cluster
```

