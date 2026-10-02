FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Java, Python, curl, and core utilities
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    python3 \
    python3-pip \
    curl \
    git \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# --- ADD THIS: Download and Install Apache Spark 3.5.0 ---
RUN curl -O https://apache.org && \
    tar -xzf spark-3.5.0-bin-hadoop3.tgz && \
    mv spark-3.5.0-bin-hadoop3 /opt/spark && \
    rm spark-3.5.0-bin-hadoop3.tgz

# Set Environment Variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$SPARK_HOME/bin:$HADOOP_HOME/bin

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir pyspark findspark pandas

CMD ["bash"]
