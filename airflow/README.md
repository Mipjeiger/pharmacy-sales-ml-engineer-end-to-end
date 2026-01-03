# Airflow Setup - Pharmacy Sales ML Pipeline

## 📋 Overview
Airflow orchestration untuk pipeline ML pharmacy sales, termasuk:
- Feature engineering pipeline (daily)
- Model training pipeline (weekly)  
- Monitoring pipeline (daily)

## 🚀 Quick Start

### 1. Start Airflow UI (Port 8080)

```bash
# Option 1: Menggunakan script (recommended)
cd /Users/miftahhadiyannoor/Documents/pharma_sales/airflow
./start_airflow.sh

# Option 2: Manual command
cd /Users/miftahhadiyannoor/Documents/pharma_sales
source .venv/bin/activate
airflow standalone
```

### 2. Access Airflow UI
- URL: http://localhost:8080
- Default credentials akan ditampilkan di terminal output
- Username: `admin`
- Password: cek di terminal atau file `~/airflow/standalone_admin_password.txt`

## 📁 Project Structure

```
airflow/
├── dags/
│   ├── pharmacy_feature_pipeline.py      # Daily feature engineering
│   ├── pharmacy_model_pipeline.py        # Weekly model training
│   └── pharmacy_monitoring_pipeline.py   # Daily monitoring
├── plugins/
│   └── __init__.py
└── start_airflow.sh                      # Helper script
```

## 🔌 Database Connections

### PostgreSQL Connection (pharmacy_db)
Connection telah dikonfigurasi dengan detail:
- **Connection ID**: `pharmacy_db`
- **Connection Type**: PostgreSQL
- **Host**: localhost
- **Port**: 5432
- **Schema**: pharmacy
- **Username**: postgres
- **Password**: postgres

### Mengubah Connection (jika perlu)

**Via CLI:**
```bash
source .venv/bin/activate

# Delete connection lama
airflow connections delete pharmacy_db

# Tambah connection baru dengan detail Anda
airflow connections add 'pharmacy_db' \
    --conn-type 'postgres' \
    --conn-host 'YOUR_HOST' \
    --conn-schema 'YOUR_DATABASE' \
    --conn-login 'YOUR_USERNAME' \
    --conn-password 'YOUR_PASSWORD' \
    --conn-port '5432'
```

**Via UI:**
1. Buka http://localhost:8080
2. Admin → Connections
3. Edit connection `pharmacy_db`
4. Update host, schema, login, password sesuai kebutuhan

## 📊 DAGs Overview

### 1. pharmacy_feature_pipeline
- **Schedule**: Daily (@daily)
- **Purpose**: Feature engineering untuk sales data
- **Tasks**:
  - `check_raw_pharmacy_sales`: Validasi data quality
  - `refresh_pharmacy_sales_features`: Generate sales features
  - `refresh_sales_llm_context`: Update LLM context

### 2. pharmacy_model_pipeline  
- **Schedule**: Weekly (@weekly)
- **Purpose**: Model training voting regressor
- **Tasks**:
  - `train_voting_regressor_model`: Train model (bash command)
  - `generate_llm_insights`: Generate insights (bash command)

### 3. pharmacy_monitoring_pipeline
- **Schedule**: Daily (@daily)
- **Purpose**: Model quality monitoring
- **Tasks**:
  - `check_model_quality`: Validate model performance
  - `publish_feature_store`: Publish to feature store

## 🛠️ Troubleshooting

### DAGs tidak muncul di UI
```bash
# Force reserialize DAGs
source .venv/bin/activate
airflow dags reserialize

# Verify DAGs detected
airflow dags list | grep pharmacy
```

### Connection error
```bash
# Test connection
airflow connections test pharmacy_db

# List all connections
airflow connections list
```

### Port 8080 sudah digunakan
Edit `~/airflow/airflow.cfg`:
```ini
[webserver]
web_server_port = 8081  # Ganti port
```

## 🔧 Configuration

### Airflow Config Location
- Global config: `~/airflow/airflow.cfg`
- Key settings:
  - `dags_folder`: `pharma_sales/airflow/dags`
  - `plugins_folder`: `pharma_sales/airflow/plugins`

### Database Location
- SQLite DB: `~/airflow/airflow.db`
- Logs: `~/airflow/logs/`

## 📝 Notes

- Airflow 3.1.0 digunakan (breaking changes dari 2.x)
- Menggunakan `SQLExecuteQueryOperator` (bukan PostgresOperator)
- Schedule menggunakan parameter `schedule` (bukan `schedule_interval`)
- Auth manager: Default (no authentication untuk development)

## 🔐 Security Warning

⚠️ **Development Mode**: 
- Saat ini menggunakan SQLite dan tanpa encryption key
- Untuk production:
  - Gunakan PostgreSQL/MySQL untuk metadata database
  - Set `fernet_key` di airflow.cfg
  - Enable authentication & RBAC

## 📚 Resources

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow 3.x Migration Guide](https://airflow.apache.org/docs/apache-airflow/stable/migration-guide.html)
- [PostgreSQL Provider Docs](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/)
