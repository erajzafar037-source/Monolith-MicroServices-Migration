# Messy to Micro: Professional DevOps Migration
 
This repository tracks the evolution of a software system from a **"Big Ball of Mud" Monolith** to a **Decoupled Microservices Architecture** using the **Strangler Fig Pattern**.
 
## Project Architecture
 
The system is composed of three primary layers:
 
1.  **Nginx API Gateway (Entry Point):** Acts as a reverse proxy, routing traffic to either the legacy monolith or the new microservices based on the URL path.
2.  **The Monolith (Legacy):** A Flask application where logic is traditionally tangled. It is being "strangled" as features are moved out.
3.  **Order Service (Microservice):** A standalone Python service with its own isolated database, handling order processing independently.
## Quick Start (WSL / Linux)
 
### 1. Clone & Setup
```bash
git clone <repo-url>
cd messy-to-micro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
 
### 2. Launch with Docker Compose
```bash
# Build and start all services in the background
docker compose up --build -d
```
 
### 3. Verify the Cluster
```bash
docker compose ps
```
 
---
 
## 🛠 DevOps Workflows
 
### Infrastructure as Code
The entire environment is defined in `docker-compose.yml`. We use **Docker Networks** for service discovery, allowing Nginx to find services by name (e.g., `http://monolith:5000`) rather than IP.
 
### The Strangler Fig Implementation
We migrated the `/process` logic without changing the frontend's target URL. This was achieved by updating the Gateway configuration (`gateway/nginx.conf`):
 
```nginx
# Requests to /process are now transparently handled by the new Order Service
location /process {
    proxy_pass http://order-service:5001/orders;
}
```
 
### Zero-Downtime Configuration Reload
To update routing rules without stopping the containers:
```bash
docker compose exec gateway nginx -s reload
```
 
---
 
## Testing the Migration
 
Use these `curl` commands from your terminal to verify the routing:
 
**Test the legacy-turned-microservice path:**
```bash
curl -X POST http://localhost/process \
     -H "Content-Type: application/json" \
     -d '{"user": "jawad_devops", "product": "mechanical_keyboard"}'
```
 
**Test the direct microservice endpoint:**
```bash
curl -X POST http://localhost/orders \
     -H "Content-Type: application/json" \
     -d '{"user": "jawad_devops", "product": "mechanical_keyboard"}'
```
 
---
 
## Project Structure
```text
.
├── gateway/
│   ├── Dockerfile          # Nginx image build
│   └── nginx.conf          # Reverse Proxy & Routing Rules
├── order-service/
│   ├── app.py              # Decoupled Order logic
│   └── Dockerfile          # Python-slim environment
├── app.py                  # The Monolith (Legacy logic)
├── docker-compose.yml      # Orchestration & Volumes
├── .gitignore              # Pro-grade exclusions (venv, db, pycache)
└── requirements.txt        # Shared dependencies
```
 
## Best Practices Implemented
* **Database per Service:** No shared database between the monolith and the microservice.
* **Environment Parity:** Docker ensures the code runs identically in WSL and production.
* **Non-Root Binding:** Services bind to `0.0.0.0` to allow cross-container communication.
* **Persistent Volumes:** Database files are mapped to the host to prevent data loss on container restart.
