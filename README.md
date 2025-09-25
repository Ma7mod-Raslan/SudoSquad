# 📌 Project: Monitoring a Containerized URL Shortener Webservice  

## 👥 Team Name: SudoSquad  

### Team Members
- **Mahmoud Raslan** – Team Leader / DevOps & Cloud  
- **Salma Hamed** – Frontend Developer  
- **Mariam Ahmed** – Backend Developer  
- **Mazen Farouk** – DevOps Engineer (Monitoring & Automation)  
- **Rehab Hassan** – Database & Documentation  
- **Omar Hossam** – QA & Testing  

---

## 💡 Project Idea
Our project is to build and monitor a **containerized URL shortener webservice**.  
The application will allow users to shorten long URLs and handle redirects. We will containerize the service using **Docker**, store data with **SQLite**, and expose custom performance metrics.  
**Prometheus** will collect these metrics, and **Grafana** will be used to create dashboards and alerts for monitoring.  
By the end, we will deliver a **fully functional, persistent, and monitored webservice** with complete documentation.  

---

## 🗂 Project Plan  

### **Week 1: Build & Containerize the URL Shortener**
- Develop the webservice with 2 endpoints:  
  - `/shorten` → Accepts a long URL and returns a short code  
  - `/<short_code>` → Redirects to the original URL  
- Use **SQLite** for storing URLs  
- Write a **Dockerfile** & initial `docker-compose.yml`  

### **Week 2: Instrumentation with Prometheus**
- Add custom metrics: shortened count, redirects, 404 errors, request latency  
- Configure **Prometheus** scraping from `/metrics` endpoint  
- Update `docker-compose.yml` to include Prometheus  

### **Week 3: Visualization with Grafana**
- Add **Grafana** to the stack  
- Connect Prometheus as data source  
- Build dashboards: URL creation rate, latency, 404 errors, total counts  

### **Week 4: Alerts, Persistence & Documentation**
- Configure **alerts** in Grafana  
- Use **Docker volumes** for SQLite, Prometheus & Grafana persistence  
- Final testing & verification  
- Write complete **README.md** and API documentation  

---

## 🎯 Roles of Each Member
- **Mahmoud Raslan (Team Leader):** Oversees project flow, manages repo, handles DevOps tasks (Docker, Compose, CI/CD).  
- **Salma Hamed:** Works on Frontend (if any UI needed) and assists in API testing.  
- **Mariam Ahmed:** Implements Backend logic for URL shortening and metrics integration.  
- **Mazen Farouk:** Focuses on monitoring (Prometheus & Grafana), metrics setup, alerting.  
- **Rehab Hassan:** Handles Database (SQLite) integration, ensures data persistence, and leads documentation.  
- **Omar Hossam:** Testing (unit + integration), ensures reliability, assists with bug fixing and QA.  

---
