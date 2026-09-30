# AWS Fargate + Neo4j Skill Knowledge Graph & Outlier Parser

Production-grade automated pipeline for deploying Neo4j to AWS Fargate with Terraform, ingesting candidate skill trees, and processing skill outliers via Graph algorithms and statistical percentage distributions.

---

## Quick Start How-To Guide

### 1. Provision AWS Fargate Infrastructure
```bash
cd terraform
terraform init
terraform apply -auto-approve
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Ingestion & Outlier Analytics Pipeline
```bash
export NEO4J_URI="bolt://<YOUR_ECS_FARGATE_IP>:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="Password123!"

# Step 1: Extract DOM skills from index.html & build Neo4j Graph
python scripts/parse_and_ingest.py

# Step 2: Run outlier detection and calculate ATS qualification score
python scripts/process_outliers.py
```
