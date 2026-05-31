"""
Cloud Native Python Microservices Deployment Pipeline
=======================================================
Corporate Use Case: Simulated microservices architecture with service
registry, load balancer, CI/CD pipeline, and Dockerfile/K8s manifest generation.
"""

import json
import random
import time
from collections import defaultdict
from datetime import datetime

random.seed(42)


# ============================================================
# MICROSERVICE DEFINITIONS
# ============================================================

class MicroService:
    """Base microservice with health check and request processing."""

    def __init__(self, name, port, version="1.0.0"):
        self.name = name
        self.port = port
        self.version = version
        self.status = "running"
        self.request_count = 0
        self.error_count = 0

    def health_check(self):
        """Check service health."""
        is_healthy = random.random() > 0.05  # 95% uptime
        return {
            "service": self.name,
            "status": "healthy" if is_healthy else "unhealthy",
            "version": self.version,
            "port": self.port,
            "uptime": f"{random.randint(1, 720)}h",
        }

    def process_request(self, request):
        """Process an incoming request."""
        self.request_count += 1
        success = random.random() > 0.1  # 90% success rate
        if not success:
            self.error_count += 1
            return {"status": "error", "code": 500, "message": "Internal server error"}
        return {"status": "success", "code": 200, "data": f"Processed by {self.name}"}

    def get_metrics(self):
        success_rate = ((self.request_count - self.error_count) / self.request_count * 100
                        if self.request_count > 0 else 100)
        return {
            "service": self.name,
            "requests": self.request_count,
            "errors": self.error_count,
            "success_rate": f"{success_rate:.1f}%",
        }


class UserService(MicroService):
    def __init__(self):
        super().__init__("user-service", 8001)
        self.users = {"U001": "Alice", "U002": "Bob", "U003": "Charlie"}

    def process_request(self, request):
        self.request_count += 1
        action = request.get("action", "get")
        if action == "get":
            user_id = request.get("user_id")
            if user_id in self.users:
                return {"status": "success", "code": 200, "user": self.users[user_id]}
            return {"status": "error", "code": 404, "message": "User not found"}
        return super().process_request(request)


class OrderService(MicroService):
    def __init__(self):
        super().__init__("order-service", 8002)

    def process_request(self, request):
        self.request_count += 1
        return {"status": "success", "code": 201,
                "order_id": f"ORD-{random.randint(1000, 9999)}"}


class PaymentService(MicroService):
    def __init__(self):
        super().__init__("payment-service", 8003)

    def process_request(self, request):
        self.request_count += 1
        success = random.random() > 0.15  # 85% success
        if success:
            return {"status": "success", "code": 200,
                    "transaction_id": f"TXN-{random.randint(10000, 99999)}"}
        self.error_count += 1
        return {"status": "error", "code": 402, "message": "Payment failed"}


# ============================================================
# SERVICE REGISTRY
# ============================================================

class ServiceRegistry:
    """Service discovery -- register and find services."""

    def __init__(self):
        self.services = {}

    def register(self, service):
        self.services[service.name] = service
        print(f"   Registered: {service.name} (port {service.port})")

    def discover(self, name):
        return self.services.get(name)

    def get_all(self):
        return list(self.services.values())


# ============================================================
# LOAD BALANCER
# ============================================================

class LoadBalancer:
    """Round-robin load balancer."""

    def __init__(self):
        self.instances = defaultdict(list)
        self.counters = defaultdict(int)

    def add_instance(self, service_name, instance):
        self.instances[service_name].append(instance)

    def get_next(self, service_name):
        """Round-robin selection."""
        instances = self.instances[service_name]
        if not instances:
            return None
        idx = self.counters[service_name] % len(instances)
        self.counters[service_name] += 1
        return instances[idx]


# ============================================================
# CI/CD PIPELINE
# ============================================================

class CICDPipeline:
    """Simulated CI/CD pipeline stages."""

    def __init__(self, service_name):
        self.service_name = service_name
        self.stages = []

    def run(self):
        """Execute pipeline: build  test  deploy."""
        print(f"\n   Pipeline for {self.service_name}")

        stages = [
            (" Build", self._build),
            (" Test", self._test),
            (" Package", self._package),
            (" Deploy", self._deploy),
        ]

        for name, func in stages:
            success = func()
            status = " PASSED" if success else " FAILED"
            self.stages.append({"stage": name, "passed": success})
            print(f"     {name}: {status}")
            if not success:
                print(f"      Pipeline halted at {name}")
                return False

        return True

    def _build(self):
        return random.random() > 0.05  # 95% success

    def _test(self):
        return random.random() > 0.1   # 90% success

    def _package(self):
        return random.random() > 0.02  # 98% success

    def _deploy(self):
        return random.random() > 0.05  # 95% success


# ============================================================
# CONFIG GENERATORS
# ============================================================

def generate_dockerfile(service):
    """Generate Dockerfile content for a service."""
    return f"""# Dockerfile for {service.name}
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE {service.port}
HEALTHCHECK --interval=30s CMD curl -f http://localhost:{service.port}/health || exit 1
CMD ["python", "app.py"]
"""


def generate_k8s_deployment(service, replicas=3):
    """Generate Kubernetes deployment YAML content."""
    return f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service.name}
  labels:
    app: {service.name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {service.name}
  template:
    metadata:
      labels:
        app: {service.name}
        version: "{service.version}"
    spec:
      containers:
      - name: {service.name}
        image: registry.company.com/{service.name}:{service.version}
        ports:
        - containerPort: {service.port}
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: {service.name}
spec:
  selector:
    app: {service.name}
  ports:
  - port: {service.port}
    targetPort: {service.port}
  type: ClusterIP
"""


# ============================================================
# MAIN DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 65)
    print("    CLOUD NATIVE MICROSERVICES DEPLOYMENT PIPELINE")
    print("=" * 65)

    # Create services
    user_svc = UserService()
    order_svc = OrderService()
    payment_svc = PaymentService()

    # Register services
    print(f"\n{''*65}")
    print("   SERVICE REGISTRY")
    print(f"{''*65}")
    registry = ServiceRegistry()
    for svc in [user_svc, order_svc, payment_svc]:
        registry.register(svc)

    # Health checks
    print(f"\n{''*65}")
    print("   HEALTH CHECKS")
    print(f"{''*65}")
    for svc in registry.get_all():
        health = svc.health_check()
        icon = "" if health["status"] == "healthy" else ""
        print(f"  {icon} {health['service']:<20} {health['status']:<10} "
              f"v{health['version']}  port:{health['port']}  uptime:{health['uptime']}")

    # Simulate traffic
    print(f"\n{''*65}")
    print("   SIMULATING TRAFFIC (20 requests)")
    print(f"{''*65}")
    services = [user_svc, order_svc, payment_svc]
    for i in range(20):
        svc = random.choice(services)
        resp = svc.process_request({"action": "process", "user_id": "U001"})

    # Metrics
    print(f"\n  {'Service':<20} {'Requests':>9} {'Errors':>8} {'Success Rate':>13}")
    print(f"  {''*50}")
    for svc in services:
        m = svc.get_metrics()
        print(f"  {m['service']:<20} {m['requests']:>9} {m['errors']:>8} {m['success_rate']:>13}")

    # CI/CD Pipelines
    print(f"\n{''*65}")
    print("   CI/CD PIPELINE EXECUTION")
    print(f"{''*65}")
    for svc in services:
        pipeline = CICDPipeline(svc.name)
        pipeline.run()

    # Generated Configs
    print(f"\n{''*65}")
    print("   GENERATED DOCKERFILE (user-service)")
    print(f"{''*65}")
    print(generate_dockerfile(user_svc))

    print(f"{''*65}")
    print("   GENERATED K8S DEPLOYMENT (user-service)")
    print(f"{''*65}")
    print(generate_k8s_deployment(user_svc))

    print(f"{'='*65}")
