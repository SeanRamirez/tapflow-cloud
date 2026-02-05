# 🍺 TapFlow Cloud - Real-Time Brewery Analytics

**TapFlow Cloud** is a full-stack data engineering platform built on Azure. It ingests real-time brewery sales data, processes it through a Medallion Architecture (Bronze/Silver/Gold) using Databricks, and visualizes inventory risks via a custom React Dashboard.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Azure](https://img.shields.io/badge/Azure-Data%20Lake-0078D4)
![Databricks](https://img.shields.io/badge/Databricks-PySpark-FF3621)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Dashboard-61DAFB)

---

## 🏗️ Architecture

```mermaid
graph TD
    subgraph Azure_Cloud [Azure Cloud Environment]
        style Azure_Cloud fill:#f9f9f9,stroke:#333,stroke-width:2px
        
        %% Data Ingestion
        Gen[Data Generator] -->|JSON| Blob_Bronze[(Blob Storage<br>Bronze Layer)]
        
        %% Data Processing
        subgraph Databricks [Azure Databricks ETL]
            style Databricks fill:#ffeae6,stroke:#ff3621
            NB1[Bronze -> Silver<br>Clean & Validate]
            NB2[Silver -> Gold<br>Aggregations]
        end
        
        Blob_Bronze --> NB1
        NB1 --> Blob_Silver[(Blob Storage<br>Silver Layer)]
        Blob_Silver --> NB2
        NB2 --> Blob_Gold[(Blob Storage<br>Gold Layer)]
        
        %% Application Layer
        subgraph App_Layer [Application Layer]
            style App_Layer fill:#e6f7ff,stroke:#0078d4
            API[FastAPI Backend<br>Reads Parquet]
            UI[React Dashboard<br>Real-time Viz]
        end
        
        Blob_Gold --> API
        API -->|JSON| UI
    end