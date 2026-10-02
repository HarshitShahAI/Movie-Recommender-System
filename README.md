# Enterprise Movie Recommendation System (Apache Spark, Hadoop & Hive SQL)

![PySpark CI/CD Pipeline](https://github.com/<your-username>/movie-recommender-spark-hive/workflows/PySpark%20CI/CD%20Pipeline/badge.svg)
![Docker Supported](https://img.shields.io/badge/Docker-Supported-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A production-ready Big Data recommendation engine and analytics pipeline leveraging **Apache Hadoop HDFS**, **Apache Spark (PySpark SQL & MLlib)**, and **Hive SQL**. Implements Collaborative Filtering via Matrix Factorization (**Alternating Least Squares**) to generate real-time personalized recommendations.

---

## 🏗️ Architecture Overview

```
+---------------------------------------------------------------------------------+
|                                 HDFS CLUSTER                                    |
|   +--------------------------+                  +---------------------------+   |
|   | Raw Movies Metadata CSV  |                  | User Ratings History CSV  |   |
|   +--------------------------+                  +---------------------------+   |
+----------------------------------------+----------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                            SPARK MLLIB ENGINE (YARN)                            |
|   +-------------------------------------------------------------------------+   |
|   | Collaborative Filtering Algorithm: Alternating Least Squares (ALS)     |   |
|   +-------------------------------------------------------------------------+   |
+----------------------------------------+----------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                        HIVE SQL & PYSPARK SQL ANALYTICS                         |
|   +---------------------+   +--------------------------+   +----------------+   |
|   | User Activity Stats |   | Genre MAE Error Profiling|   | Recommendation |   |
|   +---------------------+   +--------------------------+   +----------------+   |
+---------------------------------------------------------------------------------+
```

---

## 🚀 Quick Start with Docker (Recommended)

Run the entire cluster and pipeline locally without installing Hadoop or Spark manually:

```bash
# 1. Clone the repository
git clone [https://github.com/](https://github.com/)<your-username>/movie-recommender-spark-hive.git
cd movie-recommender-spark-hive

# 2. Build and launch the containerized Spark cluster
docker-compose -f docker/docker-compose.yml up -d

# 3. Execute the PySpark analytics job inside the cluster
docker exec -it spark-master spark-submit /app/src/spark_hive_analytics.py
```

Access Spark Master Web UI at `http://localhost:8080`.

---

## 💻 Manual Deployment (Hadoop/YARN Cluster)

```bash
# Submit job directly to an active YARN cluster
spark-submit \
  --master yarn \
  --deploy-mode client \
  --driver-memory 2g \
  --executor-memory 2g \
  src/spark_hive_analytics.py
```

---

## 📊 Analytical Pipeline Features

1. **Schema-Explicit Data Loading**: Direct `StructType` mapping bypassing stale metastore definitions.
2. **Model Error Evaluation**: Computes Mean Absolute Error (MAE) per genre to measure recommendation performance.
3. **Distribution Profiling**: Grouping user engagement metrics via Spark SQL aggregations.

---

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for details.
