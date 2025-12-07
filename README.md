# 🏠 EstateIQ | AI-Powered Real Estate Valuation Platform

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Deployed-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)

**EstateIQ** is an enterprise-grade, full-stack AI application designed to predict real estate prices with high precision. Built with a focus on **MLOps** and **Scalable Architecture**, it bridges the gap between Data Science and Production Engineering.

---

## 🚀 Key Features

* **🧠 Advanced AI Engine:** Utilizes a `RandomForestRegressor` trained on California Housing data to provide instant property valuations.
* **🔒 Secure Authentication:** Robust User Management system using **JWT (JSON Web Tokens)** and password hashing (Bcrypt).
* **💾 Persistent History:** Automatically saves user predictions to a **PostgreSQL** database for future reference.
* **📊 Interactive Dashboard:** A modern, responsive frontend (Glassmorphism design) for managing predictions.
* **🐳 Fully Dockerized:** Optimized **Multi-stage Docker builds** ensuring a lightweight (<200MB) and secure runtime environment.
* **☁️ Cloud Native:** Deployed and running on **AWS EC2** with production-grade configuration.

---

## 🛠️ Tech Stack

### Backend & AI
* **Framework:** FastAPI (High performance, easy to learn, fast to code).
* **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib.
* **Database ORM:** SQLAlchemy (with Pydantic schemas for validation).
* **Security:** Passlib (Bcrypt), Python-Jose (JWT).

### Frontend
* **Core:** HTML5, CSS3 (Modern Flexbox & Grid), Vanilla JavaScript (ES6+).
* **Design:** Custom Glassmorphism UI/UX.

### DevOps & Infrastructure
* **Containerization:** Docker & Docker Compose.
* **Cloud Provider:** AWS (EC2, Security Groups).
* **OS:** Ubuntu Server 24.04 LTS.

---

## 🏗️ System Architecture

The project follows **Clean Architecture** principles to ensure maintainability and scalability:

```text
estate-iq/
├── app/
│   ├── api/            # Route Controllers (Auth, Prediction)
│   ├── core/           # Config & Security (JWT, Hash)
│   ├── db/             # Database Connection (Session)
│   ├── db_models/      # SQLAlchemy Models (Tables)
│   ├── schemas/        # Pydantic Schemas (Validation)
│   ├── services/       # Business Logic & AI Inference
│   └── static/         # Frontend Assets (HTML, CSS, JS)
├── models/             # Serialized ML Models (.pkl)
├── scripts/            # Training Pipelines
├── Dockerfile          # Multi-stage Build Configuration
└── docker-compose.yml  # Orchestration (App + DB)
