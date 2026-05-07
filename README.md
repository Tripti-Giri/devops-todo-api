# DevOps Todo API 🚀

A REST API built with Flask, containerized with Docker, 
and deployed automatically to AWS EC2 via GitHub Actions CI/CD pipeline.

## Architecture
Push to GitHub → Tests Run → Docker Image Built → 
Pushed to DockerHub → Deployed to AWS EC2

## Tech Stack
- **App:** Python, Flask
- **Testing:** pytest (8 test cases)
- **Containerization:** Docker, DockerHub
- **CI/CD:** GitHub Actions
- **Cloud:** AWS EC2 (Ubuntu 22.04)

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /todos | Get all todos |
| POST | /todos | Create a todo |
| PUT | /todos/:id | Mark todo as done |
| DELETE | /todos/:id | Delete a todo |

## How to Run Locally
```bash
docker-compose up
```

## CI/CD Pipeline
Every push to main branch automatically:
1. Runs all pytest tests
2. Builds Docker image
3. Pushes to DockerHub
4. Deploys to AWS EC2 (rememeber to update your ec2 ip before triggering pipelinf)
