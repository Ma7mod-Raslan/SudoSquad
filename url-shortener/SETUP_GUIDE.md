# URL Shortener Service: Full Stack Setup and Monitoring Guide

This document provides a comprehensive guide to setting up and running the URL shortener webservice, complete with a PostgreSQL database, Prometheus for metrics collection, and a custom Grafana dashboard for visualization.

## 1. Prerequisites

To run this project, you must have **Docker** and **Docker Compose** installed on your system.

*   **Docker Engine:** Follow the official installation guide for your operating system [1].
*   **Docker Compose:** The modern Docker installation includes `docker compose` (without the hyphen) by default.

## 2. Project Structure

The project is organized into the following key components:

| Component | Directory/File | Description |
| :--- | :--- | :--- |
| **Webservice** | `app/` | The FastAPI application that handles URL shortening and redirection. It exposes a `/metrics` endpoint for Prometheus. |
| **Database** | Defined in `docker-compose.yaml` | A PostgreSQL container used to store the long URL and short code mappings. |
| **Metrics Collector** | `monitoring/prometheus.yml` | Configuration for Prometheus to scrape metrics from the webservice's `/metrics` endpoint. |
| **Visualization** | `grafana-dashboard.json` | The JSON file containing the definition for the custom Grafana dashboard. |
| **Orchestration** | `docker-compose.yaml` | Defines the four services (`web`, `db`, `prometheus`, `grafana`) and their network configuration. |

## 3. Launching the Stack

Navigate to the root directory of the project (`url-shortener-project/`) in your terminal and run the following command:

```bash
docker compose up --build -d
```

This command will:
1.  **Build** the `web` service image using the provided `Dockerfile`.
2.  **Download** the official images for PostgreSQL, Prometheus, and Grafana.
3.  **Start** all four services in detached mode (`-d`).

Wait a few moments for all services to start up. You can check the status with:

```bash
docker compose ps
```

## 4. Accessing the Services

Once the stack is running, you can access the services at the following local addresses:

| Service | Address | Default Credentials |
| :--- | :--- | :--- |
| **URL Shortener Web App** | `http://localhost:8001` | N/A |
| **Prometheus** | `http://localhost:9090` | N/A |
| **Grafana** | `http://localhost:3000` | **User:** `admin`, **Password:** `admin` (as configured in `docker-compose.yaml`) |

## 5. Importing the Custom Grafana Dashboard

The final step is to import the custom dashboard that provides the clear, actionable insights into the webservice's performance and usage.

1.  **Log in to Grafana** at `http://localhost:3000` using the credentials: **admin/admin**.
2.  On the left-hand menu, hover over the **Dashboards** icon (four squares) and click **Import**.
3.  Click the **Upload JSON file** button.
4.  Select the provided `grafana-dashboard.json` file from the project directory.
5.  On the next screen, ensure the **Prometheus** data source is selected for the dashboard.
6.  Click **Import**.

The dashboard, titled **"URL Shortener Service Dashboard"**, will now be visible.

## 6. Testing and Observing Metrics

To see the metrics change in near real-time, perform the following test:

1.  **Create a Short URL:**
    *   Open the web app at `http://localhost:8001`.
    *   Enter a long URL (e.g., `https://www.example.com`) and click the **Shorten** button.
    *   A short code (e.g., `http://localhost:8001/AbCdE1`) will be displayed.

2.  **Observe Metrics Change:**
    *   Go to the **"URL Shortener Service Dashboard"** in Grafana.
    *   The **"Total Shortened URLs"** panel should immediately update to `1`.
    *   The **"Request Rates"** graph will show a spike in the **Shortening Rate**.

3.  **Test Redirection:**
    *   Click the generated short link (e.g., `http://localhost:8001/AbCdE1`). This will redirect you to the long URL.

4.  **Observe Redirect Metrics:**
    *   Return to the Grafana dashboard.
    *   The **"Total Redirects"** panel should update to `1`.
    *   The **"Request Rates"** graph will show a spike in the **Redirect Rate**.

This confirms that the entire stack is running correctly, and the custom Grafana dashboard is successfully visualizing the webservice's performance and usage metrics in near real-time.

---
## References

[1] [Docker Documentation: Get Docker](https://docs.docker.com/get-docker/)
