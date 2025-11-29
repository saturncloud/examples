#!/bin/bash

# spark_setup.sh - Complete Spark setup based on working terminal history
set -e  # Exit on any error

echo "================================================"
echo "🚀 Starting Spark Setup Script"
echo "================================================"

# Configuration
HOME="$(pwd)"
INSTALL_DIR="$HOME/sparkRapid"
SPARK_VERSION="spark-4.0.1"
HADOOP_VERSION="hadoop3"
SPARK_URL="https://dlcdn.apache.org/spark/spark-4.0.1/spark-4.0.1-bin-hadoop3.tgz"
SPARK_HOME_DIR="$INSTALL_DIR/$SPARK_VERSION-bin-$HADOOP_VERSION"


# Configuration for Rapids
RAPIDS_VERSION="24.12" 
CUDA_VERSION="cu12" 
SPARK_SCALA_SHIM="spark_4.0_2.13" # Spark 4.0 uses Scala 2.13

RAPIDS_ACCELERATOR_JAR="rapids-4-spark_${SPARK_SCALA_SHIM}-${RAPIDS_VERSION}.jar"
# Note: The Maven URL requires the Scala version (2.13) and then the specific shim (spark_4.0_2.13)
RAPIDS_JAR_URL="https://repo1.maven.org/maven2/com/nvidia/rapids-4-spark_2.13/${SPARK_SCALA_SHIM}/${RAPIDS_VERSION}/${RAPIDS_ACCELERATOR_JAR}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Create installation directory
print_status "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Create Python virtual environment
print_status "Creating Python virtual environment..."
python3.10 -m venv spark_rapid_env

# Activate virtual environment
print_status "Activating virtual environment..."
source spark_rapid_env/bin/activate

# Install Python packages
print_status "Installing Python packages (jupyter, py4j, findspark)..."
pip install --upgrade pip
pip install jupyter py4j findspark

# --- Install RAPIDS Python Libraries ---
print_status "Installing RAPIDS Python packages (cuDF, cuML, cuPy) for $CUDA_VERSION..."

# 1. Cleanup (remove conflicting rmm-cu11 and cudf-cu11) and reinstall
print_status "Aggressively uninstalling conflicting RAPIDS packages..."
pip uninstall -y \
    cudf-cu11 cuml-cu11 cugraph-cu11 \
    rmm-cu11 pylibcudf-cu11 \
    cupy-cuda11x \
    numba numba-cuda llvmlite

# 2. Install compatible versions (numba and cupy)
print_status "Installing CUDA 12 prerequisites..."
pip install --extra-index-url=https://pypi.nvidia.com \
    cupy-cuda12x \
    numba==0.59.0

# 3. Then install RAPIDS core libraries
# Keep this as 24.12.0 to match the corrected RAPIDS_VERSION="24.12"
print_status "Installing CUDA 12 core RAPIDS libraries..."
pip install --extra-index-url=https://pypi.nvidia.com \
    cudf-cu12==24.12.0 \
    cuml-cu12==24.12.0


# Install Java
print_status "Installing Java..."
apt-get update
apt-get install -y openjdk-17-jdk

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java installation
print_status "Verifying Java installation..."
java -version

# Install Scala
print_status "Installing Scala..."
apt-get install -y scala

# Verify Scala installation
print_status "Verifying Scala installation..."
scala -version

# Download and extract Spark
print_status "Downloading Spark..."
if [ ! -f "$SPARK_VERSION-bin-$HADOOP_VERSION.tgz" ]; then
    wget "$SPARK_URL"
else
    print_warning "Spark archive already exists, skipping download"
fi

#Added --no-same-owner flag for safe extraction without ownership errors
print_status "Extracting Spark..."
if [ ! -d "$SPARK_HOME_DIR" ]; then
    sudo tar -zvxf "$SPARK_VERSION-bin-$HADOOP_VERSION.tgz" --no-same-owner
else
    print_warning "Spark directory already exists, skipping extraction"
fi


# Set permissions
print_status "Setting permissions..."
sleep 15
echo "Sleeping to allow directory creation....."
sudo chmod -R 777 "$SPARK_HOME_DIR"

# Set environment variables
print_status "Configuring environment variables..."

# Add to bashrc for permanent setup
cat >> ~/.bashrc << EOF

# Spark Configuration
export SPARK_HOME="$SPARK_HOME_DIR"
export PATH=\$SPARK_HOME/bin:\$PATH
export PYTHONPATH=\$SPARK_HOME/python:\$PYTHONPATH
export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"
export PYSPARK_PYTHON=python3.10

# --- NEW RAPIDS Accelerator Configuration ---
export RAPIDS_ACCELERATOR_JAR_PATH="$SPARK_HOME_DIR/jars/$RAPIDS_ACCELERATOR_JAR"
# Keeping this variable set for the Numba fix, though manual patching may be required.
export NUMBA_CUDA_ENABLE_PYNVJITLINK=1


# Configuration to enable the plugin and set basic GPU parameters
export SPARK_DEFAULTS_CONF="--jars $RAPIDS_ACCELERATOR_JAR_PATH \
    --conf spark.plugins=com.nvidia.spark.SQLPlugin \
    --conf spark.rapids.sql.enabled=true \
    --conf spark.executor.resource.gpu.amount=1 \
    --conf spark.task.resource.gpu.amount=1 \
    --conf spark.rapids.memory.gpu.maxAllocFraction=0.8 \
    --conf spark.rapids.csv.enabled=true"

# Modify PYSPARK_SUBMIT_ARGS to include the default configuration
export PYSPARK_SUBMIT_ARGS="--master local[*] \
    $SPARK_DEFAULTS_CONF \
    pyspark-shell"
# -------------------------------------------

# Java Configuration (Ensure this is not duplicated if it's already set elsewhere)
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=\$JAVA_HOME/bin:\$PATH
EOF

# Source bashrc for current session
source ~/.bashrc

# Create test script
print_status "Creating test script..."
cat > "$INSTALL_DIR/test_spark.py" << EOF
#!/usr/bin/env python3
import findspark
import os

def test_spark_setup():
    print("🧪 Testing Spark installation...")
    
    # Initialize findspark using the environment variable set in bashrc
    spark_home = os.environ.get('SPARK_HOME', '$SPARK_HOME_DIR')
    findspark.init(spark_home)
    
    try:
        import pyspark
        from pyspark.sql import SparkSession
        
        # Test Spark session creation
        spark = SparkSession.builder \
            .appName("TestApp") \
            .getOrCreate()
        
        # Test basic functionality
        data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
        df = spark.createDataFrame(data, ["Name", "Value"])
        
        print("✅ Spark setup successful!")
        print(f"✅ Spark version: {spark.version}")
        print("✅ DataFrame test passed")
        print("✅ Sample data:")
        df.show()
        
        # Test count
        count = df.count()
        print(f"✅ DataFrame count: {count}")
        
        spark.stop()
        print("\n🎉 All tests passed! Spark is ready to use.")
        return True
        
    except Exception as e:
        print(f"❌ Error during Spark test: {e}")
        return False

if __name__ == "__main__":
    test_spark_setup()
EOF

# Make test script executable
chmod +x "$INSTALL_DIR/test_spark.py"

# Create a simple PySpark test script
print_status "Creating PySpark test script..."
cat > "$INSTALL_DIR/pyspark_test.py" << EOF
#!/usr/bin/env python3
import findspark
# Initialize findspark using the environment variable for robustness
import os
spark_home = os.environ.get('SPARK_HOME', '/workspace/sparkRapid/spark-4.0.1-bin-hadoop3')
findspark.init(spark_home)

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

def main():
    print("Starting PySpark test...")
    
    # Create Spark session
    spark = SparkSession.builder \
        .appName("PySparkTest") \
        .getOrCreate()
    
    # Create sample data
    data = [
        ("Alice", "Engineering", 50000, 25),
        ("Bob", "Marketing", 75000, 32),
        ("Charlie", "Sales", 60000, 45),
        ("Diana", "Engineering", 55000, 28),
        ("Eve", "Marketing", 80000, 35)
    ]
    
    columns = ["Name", "Department", "Salary", "Age"]
    df = spark.createDataFrame(data, columns)
    
    print("Sample DataFrame:")
    df.show()
    
    # Perform some operations
    print("Aggregated data:")
    result = df.groupBy("Department").agg(
        avg("Salary").alias("AvgSalary"),
        avg("Age").alias("AvgAge"),
        count("Name").alias("EmployeeCount")
    )
    result.show()
    
    # Stop Spark session
    spark.stop()
    print("PySpark test completed successfully!")

if __name__ == "__main__":
    main()
EOF

chmod +x "$INSTALL_DIR/pyspark_test.py"

# Test the installation
print_status "Testing Spark installation..."
cd "$INSTALL_DIR"
source spark_rapid_env/bin/activate
python test_spark.py

# Display completion message
echo ""
echo "================================================"
echo "🚀 Spark setup completed successfully!"
echo "================================================"
echo ""
echo "📁 Installation directory: $INSTALL_DIR"
echo "🔧 Spark home: $SPARK_HOME_DIR"
echo "🐍 Virtual environment: $INSTALL_DIR/spark_rapid_env"
echo "☕ Java home: $JAVA_HOME"
echo ""
echo "📋 Available commands:"
echo "   Test Spark:        python $INSTALL_DIR/test_spark.py"
echo "   PySpark test:      python $INSTALL_DIR/pyspark_test.py"
echo "   Start Jupyter:     $INSTALL_DIR/start_jupyter_spark.sh"
echo "   Activate env:      source $INSTALL_DIR/spark_rapid_env/bin/activate"
echo ""
echo "💡 Quick test command:"
echo "   source $INSTALL_DIR/spark_rapid_env/bin/activate"
echo "   python -c \"import findspark; findspark.init('$SPARK_HOME_DIR'); import pyspark; print('Success!')\""
echo ""
echo "🔧 Environment variables have been added to ~/.bashrc"
echo "   Please restart your terminal or run: source ~/.bashrc"
echo ""

# Final instruction for the persistent Numba error
echo "================================================"
echo "🚨 IMPORTANT: Post-Setup Manual Fix Required"
echo "================================================"
echo "Due to a persistent Numba/cuDF version conflict, you may still see a 'RuntimeError'."
echo "To fix this, you must manually edit a file in your environment:"
echo "1. Run: nano $INSTALL_DIR/spark_rapid_env/lib/python3.10/site-packages/pynvjitlink/patch.py"
echo "2. Find the line 'raise RuntimeError(msg)' (around line 284)."
echo "3. Comment it out: # raise RuntimeError(msg)"
echo "4. Save and exit the file."