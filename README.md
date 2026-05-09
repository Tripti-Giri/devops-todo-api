---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| API | Python, Flask |
| Testing | pytest |
| Containerization | Docker, DockerHub |
| CI/CD | GitHub Actions |
| Cloud | AWS EC2 (Ubuntu 22.04), IAM, Security Groups |
| OS | Ubuntu 22.04 |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/todos` | Get all todos |
| POST | `/todos` | Create a new todo |
| PUT | `/todos/<id>` | Update a todo |
| DELETE | `/todos/<id>` | Delete a todo |

---

## 🧪 Tests

8 unit tests written with pytest covering all routes, edge cases, and error handling.

Tests act as a **pipeline gate** — deployment is blocked if any test fails.

```bash
pip install -r requirements.txt
pytest
```

---

## 🐳 Run with Docker

```bash
docker build -t devops-todo-api .
docker run -p 5000:5000 devops-todo-api
```

Or with Docker Compose:

```bash
docker-compose up
```

---

## 🚀 CI/CD Pipeline

The GitHub Actions pipeline triggers on every push to `main` and:

1. Installs dependencies
2. Runs all pytest tests — **blocks deployment on failure**
3. Builds and pushes Docker image to DockerHub
4. SSHs into AWS EC2 and performs zero-downtime container swap

All credentials are stored in **GitHub Secrets** — zero hardcoded values in the codebase.

---

## 🔐 Security

- AWS Security Groups configured for port-level access control
- IAM roles follow least-privilege principle
- All secrets managed via GitHub Secrets

<!--DISCLAIMER :: IT MIGHT NOT WORK BECAUSE EC2 INSTANCE HAS BEEN STOPPED TO AVOID AWS BILL -->