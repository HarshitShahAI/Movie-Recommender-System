FROM ubuntu:22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Java 8/11, Python 3, and core utilities
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    python3 \
    python3-pip \
    curl \
    git \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Set Environment Variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$SPARK_HOME/bin:$HADOOP_HOME/bin

# Set Python 3 as default
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy local application files into container work directory
WORKDIR /app
COPY . /app

# Install PySpark / Python dependencies
RUN pip3 install --no-cache-dir pyspark findspark pandas

CMD ["bash"]
