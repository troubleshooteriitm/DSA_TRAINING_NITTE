# Day 14 -- Cloud Basics, GitHub, Docker, Kubernetes & CI/CD

##  Topics Covered
- Cloud Computing (IaaS/PaaS/SaaS)
- Git & GitHub Workflow
- Docker (Images, Containers, Compose)
- Kubernetes Basics
- CI/CD Pipelines (GitHub Actions, Jenkins)

---

## 1. Cloud Computing Basics

### What is Cloud Computing?
On-demand delivery of computing resources (servers, storage, databases, networking) over the internet with pay-as-you-go pricing.

### Service Models

| Model | What You Manage | Provider Manages | Example |
|-------|----------------|-----------------|---------|
| **IaaS** | OS, Apps, Data | Hardware, Networking, Virtualization | AWS EC2, Azure VMs |
| **PaaS** | Apps, Data | Everything else | Heroku, Google App Engine |
| **SaaS** | Nothing (just use it) | Everything | Gmail, Salesforce, Slack |

### Major Cloud Providers
| Provider | Strengths |
|----------|-----------|
| **AWS** | Largest ecosystem, most services |
| **Azure** | Enterprise integration, .NET |
| **GCP** | ML/AI, Kubernetes (invented K8s) |

---

## 2. Git & GitHub

### Essential Commands
```bash
# Setup
git init                          # Initialize repo
git clone <url>                   # Clone remote repo

# Daily workflow
git status                        # Check status
git add .                         # Stage all changes
git add <file>                    # Stage specific file
git commit -m "message"           # Commit staged changes
git push origin main              # Push to remote
git pull origin main              # Pull latest changes

# Branching
git branch feature-x              # Create branch
git checkout feature-x            # Switch to branch
git checkout -b feature-x         # Create + switch
git merge feature-x               # Merge into current branch
git branch -d feature-x           # Delete branch

# History
git log --oneline -10             # Last 10 commits
git diff                          # Show unstaged changes
git stash                         # Temporarily save changes
git stash pop                     # Restore stashed changes
```

### Merge Conflicts
```bash
# When merge conflicts occur:
<<<<<<< HEAD
your changes
=======
their changes
>>>>>>> feature-branch

# Resolve manually, then:
git add <resolved-file>
git commit -m "Resolved merge conflict"
```

### Pull Request Workflow
1. Create feature branch
2. Make changes & commit
3. Push branch to remote
4. Open Pull Request on GitHub
5. Code review & discussion
6. Merge PR

---

## 3. Docker

### What is Docker?
Containerization platform that packages applications with all dependencies into **containers** -- lightweight, portable, and consistent across environments.

### Docker vs VMs
| Aspect | Docker Container | Virtual Machine |
|--------|-----------------|----------------|
| Size | MBs | GBs |
| Boot time | Seconds | Minutes |
| OS | Shares host kernel | Full guest OS |
| Isolation | Process-level | Hardware-level |
| Performance | Near-native | Overhead |

### Dockerfile
```dockerfile
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run command
CMD ["python", "app.py"]
```

### Common Docker Commands
```bash
# Images
docker build -t myapp:latest .     # Build image
docker images                       # List images
docker pull python:3.11             # Pull from Docker Hub
docker rmi <image>                  # Remove image

# Containers
docker run -d -p 8000:8000 myapp   # Run container (detached)
docker run -it myapp /bin/bash     # Interactive shell
docker ps                           # List running containers
docker ps -a                        # List all containers
docker stop <container>             # Stop container
docker rm <container>               # Remove container
docker logs <container>             # View logs

# Cleanup
docker system prune                 # Remove unused data
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_PASSWORD=secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

```bash
docker-compose up -d        # Start all services
docker-compose down         # Stop all services
docker-compose logs         # View logs
docker-compose ps           # List services
```

---

## 4. Kubernetes (K8s)

### What is Kubernetes?
Container **orchestration** platform that automates deployment, scaling, and management of containerized applications.

### Key Concepts
| Concept | Description |
|---------|-------------|
| **Pod** | Smallest unit -- one or more containers |
| **Deployment** | Manages pod replicas and updates |
| **Service** | Network endpoint to access pods |
| **Namespace** | Virtual cluster isolation |
| **ConfigMap** | Configuration data |
| **Secret** | Sensitive data (passwords, keys) |
| **Ingress** | External HTTP routing |

### K8s Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
```

### Common kubectl Commands
```bash
kubectl get pods                   # List pods
kubectl get services               # List services
kubectl get deployments            # List deployments
kubectl describe pod <name>        # Pod details
kubectl logs <pod>                 # View pod logs
kubectl apply -f deployment.yaml   # Apply config
kubectl delete -f deployment.yaml  # Delete resources
kubectl scale deployment myapp --replicas=5  # Scale
kubectl rollout status deployment/myapp     # Check rollout
kubectl exec -it <pod> -- /bin/bash         # Shell into pod
```

---

## 5. CI/CD Pipelines

### What is CI/CD?
| Term | Meaning | Purpose |
|------|---------|---------|
| **CI** | Continuous Integration | Auto-build & test on every commit |
| **CD** | Continuous Delivery | Auto-deploy to staging |
| **CD** | Continuous Deployment | Auto-deploy to production |

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: Python CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - run: echo "Deploying to production..."
```

### Pipeline Stages
```
Code Push  Lint  Test  Build  Deploy (Staging)  Deploy (Production)
```

---

##  Interview Tips
- **Docker**: Know Dockerfile instructions (FROM, RUN, COPY, CMD, ENTRYPOINT)
- **K8s**: Understand Pod, Deployment, Service relationship
- **Git**: Be ready for merge conflict resolution scenarios
- **CI/CD**: Explain the value of automated testing and deployment
- **Cloud**: Know the difference between IaaS/PaaS/SaaS with examples

##  Practice
| Resource | Link |
|----------|------|
| Git Tutorial | https://learngitbranching.js.org |
| Docker Playground | https://labs.play-with-docker.com |
| K8s Playground | https://killercoda.com |
| GitHub Actions Docs | https://docs.github.com/en/actions |
