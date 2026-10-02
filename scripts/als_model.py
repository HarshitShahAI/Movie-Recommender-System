import os
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# 1. Initialize Spark (Configuration agnostic)
spark = SparkSession.builder \
    .appName("Movie_Recommender_ALS") \
    .getOrCreate()

# 2. Base directory relative to project root (where this script resides in /scripts)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if "__file__" in globals() else "."

# Local / GitHub default relative paths
LOCAL_RATINGS = os.path.join(BASE_DIR, "data", "sample_ratings.csv")
LOCAL_OUTPUT = os.path.join(BASE_DIR, "output", "predictions")

# HDFS Cluster Default Paths (Explicit absolute HDFS path)
HDFS_RATINGS = "/home/hadoopuser/dsproject/data/rating.csv"
HDFS_OUTPUT = "/home/hadoopuser/dsproject/data/results"

# 3. Dynamic Path Resolution:
# Checks Environment Variables -> Default Local File (if present) -> HDFS Cluster Path
if os.getenv("RATINGS_PATH"):
    RATINGS_PATH = os.getenv("RATINGS_PATH")
elif os.path.exists(LOCAL_RATINGS):
    RATINGS_PATH = LOCAL_RATINGS
else:
    RATINGS_PATH = HDFS_RATINGS

if os.getenv("OUTPUT_PATH"):
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
elif os.path.exists(os.path.join(BASE_DIR, "output")):
    OUTPUT_PATH = LOCAL_OUTPUT
else:
    OUTPUT_PATH = HDFS_OUTPUT

print("\n" + "="*50)
print(f"--- Loading Ratings Data from: {RATINGS_PATH} ---")
print(f"--- Writing Output to: {OUTPUT_PATH} ---")
print("="*50 + "\n")

# 4. Load Data
ratings = spark.read.csv(RATINGS_PATH, header=True, inferSchema=True)
print(f"Total Rows Loaded: {ratings.count()}")

# 5. Train/Test Split (80% Train, 20% Test)
(train, test) = ratings.randomSplit([0.8, 0.2], seed=1234)
train.cache()
test.cache()

# 6. Train ALS Model
print("--- Training ALS Model ---")
als = ALS(
    maxIter=5, 
    regParam=0.1, 
    userCol="userId", 
    itemCol="movieId", 
    ratingCol="rating", 
    coldStartStrategy="drop"
)
model = als.fit(train)

# 7. Predict & Evaluate
print("--- Predicting on Test Data ---")
predictions = model.transform(test)

evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
rmse = evaluator.evaluate(predictions)

print("="*50)
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print("="*50)

# 8. Write Output
final_output = predictions.select("userId", "movieId", "rating", "prediction")
final_output.coalesce(1).write.mode("overwrite").option("header", "true").csv(OUTPUT_PATH)

print(f"\nSUCCESS! Output written to: {OUTPUT_PATH}")
spark.stop()
