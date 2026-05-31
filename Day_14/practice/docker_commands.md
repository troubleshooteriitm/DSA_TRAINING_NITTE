# Docker Commands Reference

##  Image Commands
```bash
docker build -t myapp:latest .          # Build image from Dockerfile
docker images                            # List all images
docker pull python:3.11-slim            # Pull image from Docker Hub
docker tag myapp:latest myapp:v1.0      # Tag an image
docker rmi <image_id>                    # Remove image
docker image prune                       # Remove unused images
```

##  Container Commands
```bash
docker run -d -p 8000:8000 myapp        # Run detached, map port
docker run -it myapp /bin/bash          # Interactive shell
docker run --name mycontainer myapp     # Run with custom name
docker run -e DB_HOST=localhost myapp    # Pass env variable
docker run -v ./data:/app/data myapp    # Mount volume

docker ps                                # List running containers
docker ps -a                             # List all containers
docker stop <container>                  # Stop container
docker start <container>                 # Start stopped container
docker restart <container>               # Restart container
docker rm <container>                    # Remove container
docker logs <container>                  # View logs
docker logs -f <container>              # Follow logs (tail)
docker exec -it <container> bash        # Shell into running container
docker inspect <container>              # Detailed info
```

##  Docker Compose
```bash
docker-compose up                        # Start all services
docker-compose up -d                     # Start detached
docker-compose up --build                # Rebuild and start
docker-compose down                      # Stop and remove
docker-compose ps                        # List services
docker-compose logs                      # View all logs
docker-compose logs <service>            # View specific service logs
docker-compose exec <service> bash      # Shell into service
docker-compose restart <service>        # Restart service
```

##  Cleanup
```bash
docker system prune                      # Remove unused data
docker system prune -a                   # Remove ALL unused (including images)
docker volume prune                      # Remove unused volumes
docker container prune                   # Remove stopped containers
```

##  Dockerfile Instructions
```dockerfile
FROM python:3.11-slim                    # Base image
WORKDIR /app                             # Set working directory
COPY requirements.txt .                  # Copy file
COPY . .                                 # Copy everything
RUN pip install -r requirements.txt     # Run command during build
ENV PORT=8000                            # Set environment variable
EXPOSE 8000                              # Document port (doesn't publish)
CMD ["python", "app.py"]                # Default command
ENTRYPOINT ["python"]                    # Fixed executable
ARG VERSION=1.0                          # Build-time variable
HEALTHCHECK CMD curl -f http://localhost:8000/health
```

##  Networking
```bash
docker network ls                        # List networks
docker network create mynet              # Create network
docker run --network mynet myapp        # Connect to network
docker network connect mynet container  # Connect existing container
```
