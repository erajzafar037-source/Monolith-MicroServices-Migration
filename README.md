# Monolith to Microservices Migration — DevOps Portfolio Project

A small, reproducible demonstration of the **Strangler Fig** migration pattern. An Nginx gateway routes the order workflow to an independently built Flask Order Service, while the monolith remains available for legacy routes.

> This is a learning/portfolio environment, not a production deployment. SQLite is used for local development; PostgreSQL, production secrets management, and Kubernetes are planned follow-up work.

## Architecture

- **Nginx gateway** — exposes the application on host port `8080`.
- **Legacy monolith** — Flask + SQLAlchemy on internal port `5000`.
- **Order Service** — separate Flask + SQLAlchemy process on internal port `5001`, with its own dependency manifest and database file.
- **Named Docker volumes** — preserve local SQLite data across container recreation.
- **GitHub Actions** — runs API regression tests and validates the Compose configuration.

## Quick start

Requirements: Docker Engine and Docker Compose v2.

```bash
git clone https://github.com/erajzafar037-source/Monolith-MicroServices-Migration.git
cd Monolith-MicroServices-Migration
docker compose up --build -d
docker compose ps
```

The gateway is available at `http://localhost:8080`.

Create an order through the gateway:

```bash
curl -i -X POST http://localhost:8080/process \
  -H 'Content-Type: application/json' \
  -d '{"user":"Ada","product":"Book"}'
```

The gateway maps `/process` to the extracted Order Service. The service returns an order ID and HTTP 201 on success.

Check liveness:

```bash
curl -i http://localhost:8080/health/live
```

Stop the stack (named volumes are retained):

```bash
docker compose down
```

To intentionally delete local database data as well:

```bash
docker compose down --volumes
```

## Run tests locally

```bash
python -m pip install -r requirements.txt pytest
pytest -q
```

## Current improvements

- Fixed the Order Service's explicit dependency file so its image can install requirements.
- Uses Gunicorn rather than Flask's development server in containers; debug mode is not enabled.
- Validates JSON request shape and required fields, returns predictable client errors, and rolls back failed database sessions.
- Adds liveness endpoints, Compose health checks, restart policies, and persistent named volumes.
- Adds baseline pytest regression tests and a GitHub Actions workflow.

## Known limitations

- SQLite is suitable for this local demonstration, not a claim of production-grade database operations.
- `/health/live` is a liveness endpoint, not a full dependency-readiness check.
- There is no authentication, rate limiting, distributed tracing, metrics dashboard, Kubernetes deployment, Terraform, or automated traffic-shift/rollback yet.
- The CI workflow has been added to the repository, but its remote run result must be checked in the Actions tab; do not treat code committed as proof that the workflow passed.

## Roadmap

See [docs/FUTURE_WORK.md](docs/FUTURE_WORK.md) for the phased plan: data contracts and migrations, supply-chain security, observability/SLOs, Kubernetes + Helm + Terraform, and a measurable migration/rollback rehearsal.

## Migration principles

1. Preserve the client-facing API contract while moving one capability at a time.
2. Keep data ownership explicit; do not let services write to each other's databases.
3. Add contract and regression tests before shifting traffic.
4. Define rollback triggers before rollout and practice the rollback.
5. Publish latency, throughput, error-rate, and resource measurements only after reproducible tests.

## Attribution

This repository is based on a fork. Preserve upstream attribution and comply with the upstream repository's applicable license before redistributing or reusing its code.
