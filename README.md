# MCI Server

A small FastAPI project for creating, deleting, and finding groups.

## Requirements

- Python 3.12+
- Docker (optional)
- Kubernetes (optional)

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will be available at:

```text
http://localhost:8000
```

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/v1/group` | Create a group |
| `DELETE` | `/v1/group` | Delete a group |
| `GET` | `/v1/group/{groupId}` | Get a group |

Example request body:

```json
{
  "groupId": "group1"
}
```

## Run with Docker

Build the image:

```bash
docker build -t mci-server:latest .
```

Run three server instances:

```bash
docker compose up --build
```

## Tests

Run tests with:

```bash
pytest
```

## Kubernetes

Deploy the application:

```bash
kubectl apply -f deploy.yaml
```

The Kubernetes manifest creates three server replicas and a `ClusterIP` service.
