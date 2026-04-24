# VETTRA-AI: Livestock Health Intelligence System (LHIS)

VETTRA-AI LHIS is a proactive health monitoring system for livestock, using a hybrid approach that combines veterinary expertise (Rule Engine) and Machine Learning (Random Forest) to detect early signs of illnesses or heat stress.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- SQLite (built-in)
- Docker (optional, for deployment)

### Local Setup
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. **Train initial models**:
   ```bash
   python backend/ml/train.py
   ```
4. **Start the server**:
   ```bash
   uvicorn backend.main:app --reload
   ```
5. **API Documentation**: Visit `http://127.0.0.1:8000/docs`

### Docker Deployment
```bash
docker-compose up --build
```

## 📂 Project Structure
- `backend/`: Core FastAPI application
  - `routes/`: API endpoints
  - `services/`: Business logic, Risk Fusion, and ML Inference
  - `models/`: Database models and trained artifacts
  - `ml/`: Training and evaluation scripts
- `tests/`: Unit and integration test suite

## 🧠 Core Technologies
- **Backend**: FastAPI, SQLAlchemy (Async), Pydantic
- **Data Science**: Scikit-Learn, Pandas, NumPy, SHAP, Librosa
- **Database**: SQLite (Production suggested: PostgreSQL)

## ⚖️ License
MIT
# vetra
