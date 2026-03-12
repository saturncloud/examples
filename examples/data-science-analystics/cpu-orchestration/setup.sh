#!/bin/bash
set -e  # Exit immediately if any command fails

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🚀 Starting Conflict-Free Orchestration Setup...${NC}"

# 1. Clean up previous failed installs
rm -rf miniconda_dist airflow_home

# 2. Install System Dependencies
echo -e "${BLUE}📦 Installing system libraries...${NC}"
sudo apt update -y
sudo apt install -y libmariadb-dev libssl-dev libkrb5-dev build-essential wget

# 3. Setup Project Structure
mkdir -p data scripts airflow_home/dags

# 4. Download Miniconda
if [ ! -d "miniconda_dist" ]; then
    echo -e "${BLUE}📥 Downloading Python 3.11 Manager...${NC}"
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p "$(pwd)/miniconda_dist"
    rm miniconda.sh
else
    echo -e "${GREEN}✅ Python Manager already installed.${NC}"
fi

# 5. Create Virtual Environment
ENV_PATH="$(pwd)/miniconda_dist/envs/airflow_env"
CONDA_BIN="$(pwd)/miniconda_dist/bin/conda"

echo -e "${BLUE}🔨 Creating Virtual Environment at: $ENV_PATH ...${NC}"
# Use conda-forge and override channels to avoid ToS errors
"$CONDA_BIN" create -y -p "$ENV_PATH" python=3.11 -c conda-forge --override-channels

# 6. Define Executable Paths
ENV_PIP="$ENV_PATH/bin/pip"
ENV_AIRFLOW="$ENV_PATH/bin/airflow"

# 7. Install Libraries with STRICT Pins (The Fix)
# We pin SQLAlchemy < 2.0 to satisfy Airflow
# We pin Prefect < 3.0 because Prefect 3 forces incompatible libraries
AIRFLOW_VERSION="2.10.4"
PYTHON_VERSION="3.11"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

echo -e "${BLUE}🐍 Installing Airflow ${AIRFLOW_VERSION} and Prefect 2.x...${NC}"

# Install Airflow using the official constraints
"$ENV_PIP" install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Install Prefect 2.x and other tools, forcing them to respect Airflow's limits
# "sqlalchemy<2.0" ensures Prefect doesn't upgrade the DB driver and break Airflow
"$ENV_PIP" install "prefect<3.0.0" "sqlalchemy<2.0" pandas scikit-learn plotly

# 8. Initialize Database
export AIRFLOW_HOME=$(pwd)/airflow_home
echo -e "${BLUE}💾 Initializing Airflow Database...${NC}"
"$ENV_AIRFLOW" db migrate  # 'db init' is deprecated, 'db migrate' is the new standard

# 9. Create Admin User
"$ENV_AIRFLOW" users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org \
    --password admin

echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo "-------------------------------------------------------"
echo "To activate your environment:"
echo "   source $(pwd)/miniconda_dist/bin/activate $ENV_PATH"
echo ""
echo "To Start Airflow:"
echo "   export AIRFLOW_HOME=$(pwd)/airflow_home"
echo "   airflow standalone"
echo "-------------------------------------------------------"