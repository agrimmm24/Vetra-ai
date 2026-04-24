# 🧠 Vettra-AI — Livestock Health Intelligence System (LHIS)

[![Next.js](https://img.shields.io/badge/Next.js-14.2-black?logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Expo](https://img.shields.io/badge/Expo-SDK%2054-000020?logo=expo)](https://expo.dev)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost-FF6600?logo=python)](https://xgboost.readthedocs.io)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript)](https://www.typescriptlang.org)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)](https://www.python.org)

> **Vettra-AI** is a full-stack, AI-driven livestock health monitoring platform for Indian dairy farmers. It combines an XGBoost ML model, a rule-based risk engine, and a bilingual (EN/HI) interface across a Next.js web dashboard and Expo React Native mobile app — all backed by a FastAPI async Python backend.

---

## 📁 Repository Structure

```
VETTRA-AI/
├── frontend/          # Next.js 14 Web Dashboard (App Router)
├── mobile/            # Expo + React Native Mobile App
└── vetra/
    └── backend/       # FastAPI Python Backend (Async SQLAlchemy)
        ├── ml/        # ML training scripts & synthetic dataset
        ├── models/    # Trained model artifacts (.pkl)
        ├── routes/    # API route handlers
        ├── schemas/   # Pydantic request/response schemas
        ├── services/  # Business logic & ML inference layer
        └── utils/     # Shared utilities
```

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                         CLIENTS                              │
│   ┌─────────────────┐            ┌───────────────────────┐   │
│   │  Next.js Web    │            │  Expo Mobile App      │   │
│   │  (App Router)   │            │  (React Native)       │   │
│   └────────┬────────┘            └──────────┬────────────┘   │
└────────────┼─────────────────────────────────┼───────────────┘
             │ REST + JWT                       │ REST + Fallback
             ▼                                 ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Async)                    │
│                                                             │
│   /auth   /predict   /simulate   /animals   /health        │
│                                                             │
│  ┌──────────────────┐   ┌──────────────────────────────┐   │
│  │  Rule Engine     │   │  XGBoost ML Model            │   │
│  │  (40% weight)    │◄──┤  (50% weight)                │   │
│  └──────────────────┘   └──────────────────────────────┘   │
│            │                          │                     │
│            └──────────┬───────────────┘                     │
│                       ▼                                     │
│              Risk Fusion Engine                             │
│            (Composite 0–100 score)                          │
│                       │                                     │
│            ┌──────────▼──────────┐                         │
│            │  SQLite via Async   │                         │
│            │  SQLAlchemy ORM     │                         │
│            └─────────────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Tech Stack

### Backend (`vetra/backend/`)
| Layer | Technology |
|-------|-----------|
| Framework | FastAPI (async) |
| ORM | SQLAlchemy (AsyncSession) |
| Database | SQLite (dev) |
| ML | XGBoost + scikit-learn + joblib |
| Auth | JWT (python-jose) + Firebase OTP |
| Feature Eng. | numpy + custom pipeline |
| Explainability | SHAP-lite custom logic |

### Frontend (`frontend/`)
| Layer | Technology |
|-------|-----------|
| Framework | Next.js 14 (App Router) |
| Styling | Tailwind CSS v3 + custom "Organic" tokens |
| UI Components | Custom design system |
| Charts | Recharts |
| Animations | Framer Motion |
| Forms | React Hook Form |
| Icons | Lucide React |
| Language | TypeScript 5 |

### Mobile (`mobile/`)
| Layer | Technology |
|-------|-----------|
| Framework | Expo SDK 54 + React Native 0.81 |
| Navigation | Expo Router (file-based) |
| 3D / GL | React Three Fiber + Three.js + expo-gl |
| Fonts | Fraunces + Nunito (Google Fonts) |
| Network | urql (GraphQL client) + native fetch |
| Language | TypeScript 5.9 |

---

## 🧠 ML Pipeline

### Model: XGBoost Classifier

**Training Data:** 10,000 synthetic samples generated to mirror real bovine vitals.

**Features (7-dimensional input vector):**

| Feature | Description | Normal Range |
|---------|-------------|-------------|
| `milk_drop_pct` | % drop from baseline milk yield | 0.0 (no drop) |
| `feed_score` | Categorical: low=0.0, medium=0.5, high=1.0 | 1.0 |
| `activity_score` | Categorical: low=0.0, medium=0.5, high=1.0 | 1.0 |
| `temp_risk` | Binary: 1.0 if temp > 39.5°C | 0.0 |
| `temp_deviation` | Normalized abs deviation from 38.5°C | < 0.2 |
| `ph_score` | Normalized pH deviation from 6.6 | < 0.2 |
| `hr_score` | Normalized heart rate deviation from 70 BPM | < 0.2 |

**Sick label logic (training):**
```python
is_sick = (
    (milk_drop > 0.15) & (temp_risk == 1.0) |
    (feed <= 0.5) & (activity <= 0.5) & (temp_deviation > 0.5) |
    (ph_score > 0.6) |
    (hr_score > 0.7) |
    (temp_deviation > 1.8)
)
```

**Risk Fusion (3-source weighted composite):**
```
Final Score = (Rule Engine × 0.40) + (ML Model × 0.50) + (Voice × 0.10)
```
- `LOW` if score < 40
- `MEDIUM` if 40 ≤ score < 70
- `HIGH` if score ≥ 70

**Train the model:**
```bash
cd vetra
python -m backend.ml.train
```
Model saved to: `vetra/backend/models/trained/random_forest_model.pkl`

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm / npx
- Expo CLI (`npm install -g expo-cli`)

---

### 1. Backend Setup

```bash
cd vetra

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy aiosqlite python-jose[cryptography] \
            passlib[bcrypt] xgboost scikit-learn pandas numpy joblib shap

# Train the ML model (first time only)
python -m backend.ml.train

# Start the development server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

API will be live at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

---

### 2. Frontend Setup (Next.js Web)

```bash
cd frontend

npm install
npm run dev
```

Web dashboard at: `http://localhost:3000`

---

### 3. Mobile Setup (Expo)

```bash
cd mobile

npm install

# Start Expo dev server
npx expo start

# Platform-specific
npx expo start --ios       # iOS Simulator
npx expo start --android   # Android Emulator
npx expo start --web       # Browser (Expo Web)
```

> **Important:** Update the backend URL in `mobile/src/lib/mock-api.ts`:
> ```ts
> const BACKEND_URL = "http://<YOUR_LOCAL_IP>:8000/api/v1";
> ```
> Use your machine's LAN IP (not `localhost`) so the device/emulator can reach the backend.

---

## 🌐 API Reference

Base URL: `http://localhost:8000/api/v1`

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/signup` | Register a new farmer account |
| `POST` | `/auth/login/request-otp` | Trigger Firebase OTP to phone |
| `POST` | `/auth/login/verify-otp` | Verify OTP, returns JWT token |

**Signup Request:**
```json
{
  "name": "Ramesh Kumar",
  "phone": "+919876543210",
  "farm_name": "Ramesh Dairy"
}
```

---

### Predict (Risk Assessment)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/predict/` | Submit daily vitals → get risk score |

**Request Body (`DailyHealthInput`):**
```json
{
  "animal_id": "COW-12",
  "milk_yield": 14.5,
  "feed_intake": "low",
  "activity_level": "medium",
  "temperature": 39.8,
  "pH": 6.4,
  "heart_rate": 85
}
```

**Response (`RiskAssessment`):**
```json
{
  "animal_id": "COW-12",
  "score": 73.4,
  "level": "HIGH",
  "health_rank": "critical",
  "reasons": [
    { "en": "Temperature is abnormally high (39.8°C)", "hi": "तापमान असामान्य रूप से अधिक है" }
  ],
  "actions": [
    { "en": "Contact a veterinarian for urgent examination.", "hi": "पशु चिकित्सक से संपर्क करें।" }
  ],
  "feature_importance": { "temp_risk": 0.45, "milk_drop_pct": 0.30 },
  "timestamp": "2026-04-19T07:45:00"
}
```

---

### Simulate (What-If Scenarios)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/simulate/` | Compare current vs modified animal state |

**Request Body:**
```json
{
  "animal_id": "COW-12",
  "modified_inputs": {
    "animal_id": "COW-12",
    "milk_yield": 18.0,
    "feed_intake": "high",
    "activity_level": "high",
    "temperature": 38.6
  }
}
```

---

### Animals

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/animals/` | List all registered animals |
| `POST` | `/animals/` | Register a new animal |

---

## 📱 Mobile — Offline-First Architecture

The mobile app uses a **graceful fallback strategy**:

```
Request → Backend API (3s timeout)
              ↓ (if unreachable)
       Local Rule Engine (calculateRiskFallback)
```

This means the app is **fully functional without internet** using `mock-api.ts` — its built-in rule engine mirrors the backend logic exactly. Results are **bilingual (EN/HI)** for rural farmer accessibility.

---

## 🗂️ Key Files Reference

### Backend
| File | Purpose |
|------|---------|
| `vetra/backend/services/feature_engineering.py` | Raw vitals → 7D feature vector |
| `vetra/backend/services/rule_engine.py` | Threshold-based rule scoring (40% weight) |
| `vetra/backend/services/prediction.py` | XGBoost inference wrapper |
| `vetra/backend/services/risk_fusion.py` | Composite score + action generation |
| `vetra/backend/services/explainability.py` | Feature importance explanations |
| `vetra/backend/services/simulation.py` | What-if scenario comparison |
| `vetra/backend/ml/train.py` | Synthetic data generation + XGBoost training |

### Frontend
| File | Purpose |
|------|---------|
| `frontend/src/app/page.tsx` | Dashboard home — animal health overview |
| `frontend/src/app/track/page.tsx` | Daily health log form |
| `frontend/src/app/simulate/page.tsx` | What-if risk simulator |
| `frontend/src/app/history/page.tsx` | Historical health trend charts |
| `frontend/src/context/AuthContext.tsx` | JWT auth state management |

### Mobile
| File | Purpose |
|------|---------|
| `mobile/app/(tabs)/index.tsx` | Home dashboard tab |
| `mobile/app/(tabs)/track.tsx` | Daily log submission |
| `mobile/app/(tabs)/simulate.tsx` | Risk scenario simulator |
| `mobile/app/(tabs)/history.tsx` | Health trend history |
| `mobile/app/(tabs)/profile.tsx` | Farmer profile & animal management |
| `mobile/src/lib/mock-api.ts` | API client + offline fallback engine |

---

## 🔐 Authentication Flow

```
1. Farmer signs up → phone stored in DB
2. Login → Server triggers Firebase OTP to phone number
3. Farmer submits OTP → Server verifies with Firebase
4. On success → JWT access token (30 min expiry) returned
5. All protected routes require: Authorization: Bearer <token>
```

---

## 🌿 Design System — "Organic" Theme

The UI follows a premium **Organic / Earth-toned** design language:

| Token | Value |
|-------|-------|
| Background | `#F5F0E8` (warm parchment) |
| Primary | `#3D6B4F` (forest green) |
| Accent | `#C68B3A` (warm amber) |
| Critical | `#B5483A` (deep terracotta) |
| Font | Fraunces (serif headings) + Nunito (body) |

---

## 🧪 Running Tests

```bash
# Backend tests
cd vetra
source venv/bin/activate
pytest backend/tests/ -v

# Frontend lint
cd frontend
npm run lint

# ML model evaluation
cd vetra
python -m backend.ml.evaluate
```

---

## 📦 Environment Variables

### Backend (create `vetra/backend/.env`):
```env
SECRET_KEY=your-jwt-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite+aiosqlite:///./vettra.db
FIREBASE_API_KEY=your-firebase-api-key
```

### Frontend (create `frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 🗺️ Roadmap

- [ ] Real Firebase SMS OTP integration (replace mock)
- [ ] Push notifications for HIGH risk alerts
- [ ] Multi-farm / multi-user support
- [ ] Voice note analysis for distress detection (10% weight slot ready)
- [ ] PostgreSQL migration for production
- [ ] Docker Compose for one-command startup
- [ ] Offline data sync queue for mobile

---

## 👥 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit with clear messages: `git commit -m "feat: add XYZ"`
4. Push and open a Pull Request

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ for India's dairy farmers — <strong>Vettra-AI LHIS</strong>
</p>
