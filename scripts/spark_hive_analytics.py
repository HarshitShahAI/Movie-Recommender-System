import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType

# 1. Initialize SparkSession (Configuration agnostic)
spark = SparkSession.builder \
    .appName("Movie_Recommender_Analytics") \
    .getOrCreate()

# 2. Base directory relative to project root (where this script resides in /scripts)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if "__file__" in globals() else "."

# Local / GitHub default relative paths
LOCAL_MOVIES = os.path.join(BASE_DIR, "data", "sample_movies.csv")
LOCAL_RESULTS = os.path.join(BASE_DIR, "output", "sample_predictions.csv")

# HDFS Cluster Default Paths (Explicit absolute HDFS path)
HDFS_MOVIES = "/home/hadoopuser/dsproject/data/movies.csv"
HDFS_RESULTS = "/home/hadoopuser/dsproject/data/results/predictions.csv"

# 3. Dynamic Path Resolution:
# Checks Environment Variables -> Default Local File (if present) -> HDFS Cluster Path
if os.getenv("MOVIES_PATH"):
    MOVIES_PATH = os.getenv("MOVIES_PATH")
elif os.path.exists(LOCAL_MOVIES):
    MOVIES_PATH = LOCAL_MOVIES
else:
    MOVIES_PATH = HDFS_MOVIES

if os.getenv("RESULTS_PATH"):
    RESULTS_PATH = os.getenv("RESULTS_PATH")
elif os.path.exists(LOCAL_RESULTS):
    RESULTS_PATH = LOCAL_RESULTS
else:
    RESULTS_PATH = HDFS_RESULTS

print("\n" + "="*50)
print(f"--- Loading Movies Data from: {MOVIES_PATH} ---")
print(f"--- Loading Results Data from: {RESULTS_PATH} ---")
print("="*50 + "\n")

# 4. Define Explicit Schemas
movies_schema = StructType([
    StructField("movieId", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("genres", StringType(), True)
])

recommendations_schema = StructType([
    StructField("userId", IntegerType(), True),
    StructField("movieId", IntegerType(), True),
    StructField("rating", FloatType(), True),
    StructField("prediction", FloatType(), True)
])

# 5. Read Datasets using resolved paths
movies_df = spark.read \
    .option("header", "true") \
    .schema(movies_schema) \
    .csv(MOVIES_PATH)

recs_df = spark.read \
    .option("header", "true") \
    .schema(recommendations_schema) \
    .csv(RESULTS_PATH)

# 6. Register In-Memory Views
movies_df.createOrReplaceTempView("movies")
recs_df.createOrReplaceTempView("movie_recommendations")

# 7. Execute Analytical Queries
print("\n=== Query 1: User Rating Activity ===")
spark.sql("""
SELECT 
    userId, 
    COUNT(*) AS total_ratings, 
    ROUND(AVG(rating), 2) AS avg_given_rating
FROM movie_recommendations
GROUP BY userId
ORDER BY total_ratings DESC
LIMIT 10
""").show()

print("\n=== Query 2: Model Error Performance Across Movie Genres ===")
spark.sql("""
SELECT 
    m.genres,
    COUNT(*) AS total_predictions,
    ROUND(AVG(ABS(r.rating - r.prediction)), 4) AS mean_absolute_error
FROM movie_recommendations r
JOIN movies m ON r.movieId = m.movieId
GROUP BY m.genres
HAVING COUNT(*) > 5
ORDER BY mean_absolute_error ASC
LIMIT 10
""").show()

print("\n=== Query 3: Top Recommended Movies Across All Users ===")
spark.sql("""
SELECT 
    m.title,
    m.genres,
    ROUND(AVG(r.prediction), 2) AS avg_predicted_rating,
    COUNT(*) AS recommendation_count
FROM movie_recommendations r
JOIN movies m ON r.movieId = m.movieId
WHERE r.prediction >= 4.0
GROUP BY m.title, m.genres
ORDER BY avg_predicted_rating DESC, recommendation_count DESC
LIMIT 10
""").show()

spark.stop()
