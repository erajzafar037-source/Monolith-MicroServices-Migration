# Future work: migration to production-grade microservices

## Phase 1 — Stabilize
- Fix the Order Service image build by adding its own dependency manifest.
- Validate JSON input and return predictable 4xx responses.
- Disable Flask debug mode and serve containers through Gunicorn.
- Persist SQLite data with named volumes for local development.
- Add health endpoints, regression tests, and CI.

## Phase 2 — Data and contracts
- Move from SQLite to PostgreSQL when service boundaries and schemas are stable.
- Give each service exclusive ownership of its data; do not share tables or database credentials.
- Add schema migrations (Alembic/Flask-Migrate), API contract tests, idempotency keys, and bounded request timeouts.
- Specify how the legacy `/process` contract maps to the extracted Order Service.

## Phase 3 — Delivery and security
- Add linting, dependency and secret scanning, SBOM generation, image scanning, and image publishing.
- Use immutable image tags and separate build from deploy; use environment-specific configuration and secret stores.
- Run non-root containers, pin base images by digest where practical, and define resource limits.

## Phase 4 — Observability and reliability
- Add structured JSON logs, request/correlation IDs, metrics, traces, and dashboards.
- Define SLOs for availability, error rate, and p95 latency; alert on user-visible symptoms.
- Exercise timeouts, dependency outages, database failures, and recovery in repeatable tests.

## Phase 5 — Kubernetes and infrastructure as code
- Add Kubernetes Deployments, Services, startup/readiness/liveness probes, resource requests/limits, and rolling updates.
- Package manifests with Helm and provision cloud infrastructure with Terraform.
- Keep credentials out of Git; use least-privilege IAM and document cost cleanup.

## Phase 6 — Prove the Strangler migration
- Add contract/regression tests proving old and new route behavior.
- Switch traffic in controlled increments using gateway routing or a feature flag.
- Define measurable rollback triggers before rollout and rehearse rollback.
- Publish reproducible load-test results (p50/p95/p99 latency, throughput, error rate, CPU/memory); never claim gains without measured evidence.

## Definition of done
A clean checkout can build and start the stack; tests and CI pass; data survives container restarts; service failures are observable; and another developer can reproduce the migration and rollback from documented commands.
