# Todo App Helm Chart

This Helm chart deploys the AI-ready full-stack todo app to Kubernetes.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
helm install my-release ./todo-app --namespace todo-app-prod --create-namespace
```

## Upgrading the Chart

```bash
helm upgrade my-release ./todo-app --namespace todo-app-prod
```

## Uninstalling the Chart

```bash
helm uninstall my-release --namespace todo-app-prod
```

## Configuration

The following table lists the configurable parameters of the todo-app chart and their default values.

| Parameter                     | Description                                           | Default                      |
|-------------------------------|-------------------------------------------------------|------------------------------|
| `frontend.replicaCount`       | Number of frontend pods                               | `2`                          |
| `frontend.image.repository`   | Frontend image repository                             | `todo-frontend`              |
| `frontend.image.tag`          | Frontend image tag                                    | `latest`                     |
| `frontend.service.type`       | Frontend service type                                 | `ClusterIP`                  |
| `frontend.service.port`       | Frontend service port                                 | `80`                         |
| `backend.replicaCount`        | Number of backend pods                                | `2`                          |
| `backend.image.repository`    | Backend image repository                              | `todo-backend`               |
| `backend.image.tag`           | Backend image tag                                     | `latest`                     |
| `backend.service.type`        | Backend service type                                  | `ClusterIP`                  |
| `backend.service.port`        | Backend service port                                  | `80`                         |
| `config.apiBaseUrl`           | Base URL for API calls                                | `https://todo.example.com/api` |
| `namespace.name`              | Namespace to deploy the application                   | `todo-app-prod`              |

## Secrets

This chart expects the following secrets to be created in the target namespace:

- `db-secret` with key `url` containing the database connection string
- `auth-secret` with key `secret` containing the auth secret

Example:
```bash
kubectl create secret generic db-secret --from-literal=url=<DATABASE_URL> --namespace todo-app-prod
kubectl create secret generic auth-secret --from-literal=secret=<AUTH_SECRET> --namespace todo-app-prod
```

## Ingress

The chart supports ingress configuration. See `values.yaml` for ingress settings.