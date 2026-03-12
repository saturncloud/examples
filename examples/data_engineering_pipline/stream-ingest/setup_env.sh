# === Phase 1: Environment Setup Script ===

# --- 1. Define Spark Variables (Targeting 3.5.1) ---
SPARK_VERSION="spark-3.5.1"
SPARK_ARCHIVE="${SPARK_VERSION}-bin-hadoop3.tgz"
INSTALL_PATH="./spark" # Standard installation path

echo "--- 1. Downloading and installing Apache Spark 3.5.1 binary ---"
# Download Spark 3.5.1
wget https://archive.apache.org/dist/spark/spark-3.5.1/$SPARK_ARCHIVE

# Extract and move
tar -xzf $SPARK_ARCHIVE --no-same-owner
mv ${SPARK_VERSION}-bin-hadoop3 $INSTALL_PATH
rm $SPARK_ARCHIVE

# --- 2. Set Environment Variables ---
echo "--- 2. Setting environment variables ---"
export SPARK_HOME=$INSTALL_PATH
export PATH=$PATH:$SPARK_HOME/bin
export PYSPARK_PYTHON="/usr/bin/python3"

# --- 3. Install Python Dependencies ---
echo "--- 3. Installing PySpark 3.5.1 and supporting libraries ---"
pip install pyspark==3.5.1

echo "✅ Environment configured. You can proceed to Phase 2."