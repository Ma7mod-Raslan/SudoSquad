# URL Shortener Webservice  
A complete, containerized URL-shortening service with monitoring, dashboards, alerting, and full AWS deployment.

This project was built following the DevOps Engineer structured roadmap and includes:

- Containerized FastAPI application  
- PostgreSQL persistence  
- Prometheus metrics  
- Grafana dashboards  
- Grafana alerting + Slack integration  
- Terraform IaC for AWS deployment  
- Automated provisioning (Prometheus, Grafana, datasources, dashboards)

---

## 🚀 Features

### 🔗 URL Shortening Service  
- Shortens long URLs  
- Redirects using unique short codes  
- Persists data using PostgreSQL  

### 📊 Monitoring & Metrics  
- `/metrics` endpoint exposing Prometheus metrics  
- Custom counters & histograms:
  - `urls_shortened_total`
  - `redirects_total`
  - `lookups_404_total`
  - `request_latency_seconds`

### 📈 Grafana Dashboard  
- URL creation rate  
- Redirect rate  
- 404 lookup rate  
- P95 latency  
- Real-time visual updates

### 🚨 Alerting  
Grafana alerts:
- High 404 lookup rate  
- High P95 latency  
- Redirect traffic dropped to zero  

Alerts are sent to Slack via webhook.

---

## 📂 Project Structure

url-shortener/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
├── grafana/
│   ├── dashboards_json/
│   └── provisioning/
│       ├── dashboards/
│       ├── datasources/
│       └── alerting/
├── monitoring/
│   └── prometheus.yml
├── infra/
│   ├── vpc/
│   ├── ec2/
│   ├── ecr/
│   ├── security/
│   ├── providers.tf
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
└── README.md
---

## **Project Files**

You can find the full project files and source code in the repository.  
🔗 **Google Drive Folder:** [Access Project Files](https://drive.google.com/drive/u/1/folders/1o8fsaWSIWtQyC2S6PNpufnIceuu74w9_)

---

## 🐳 Running Locally (Docker Compose)

```bash
docker-compose up --build
