# 🧠 VETTRA-AI: Livestock Health Intelligence System (LHIS) — Full Cognitive Analysis

> **Source Documents Analyzed:**
> 1. [🧠 LHIS Tech Stack Report](file:///Users/divyanshdusad/Documents/VETTRA-AI/🧠%20Livestock%20Health%20Intelligence%20System%20(LHIS)%20(1).pdf) — Open-source tech stack & project structure
> 2. [🧠 LHIS Technical Report (Final)](file:///Users/divyanshdusad/Documents/VETTRA-AI/🧠%20Livestock%20Health%20Intelligence%20System%20(LHIS).pdf) — Developer + system design level detail (22 sections)
> 3. [🧠 Product Requirements Document (FINAL)](file:///Users/divyanshdusad/Documents/VETTRA-AI/🧠%20Product%20Requirements%20Document%20(FINAL).pdf) — Product-level requirements & success criteria

---

## 1. 🎯 Problem Domain & Vision

### 1.1 The Problem

Livestock health management today is **fundamentally reactive**. Farmers detect illness only *after* visible symptoms appear, leading to:

| Impact Area | Current State | LHIS Target State |
|---|---|---|
| **Detection** | Post-symptom (reactive) | Pre-symptom (proactive) |
| **Data Model** | Fragmented (milk, feed, behavior tracked separately or not at all) | Unified multi-signal fusion |
| **Insights** | None — guess-based | Personalized, per-animal, data-driven |
| **Decision Support** | Manual intuition | Simulation-driven what-if analysis |
| **Tracking** | Sporadic | Continuous daily monitoring |

### 1.2 The Vision

> *"LHIS transforms livestock health management from reactive observation to proactive, data-driven decision-making."*

**Three paradigm shifts:**
- **Reactive → Proactive** — Early risk detection before visible illness
- **Static → Interactive** — Simulation engine for what-if scenarios
- **Guess-based → Data-driven** — Multi-signal ML-powered risk assessment

### 1.3 Target Users

- 🧑‍🌾 **Dairy farmers** — Primary users, daily health tracking
- 📋 **Livestock managers** — Fleet-level oversight
- 🏘️ **Rural agricultural communities** — Accessible design philosophy

---

## 2. 🏗 High-Level System Architecture

```mermaid
graph TB
    subgraph "👤 User Layer"
        F["🧑‍🌾 Farmer / Manager"]
    end

    subgraph "🖥 Frontend — Next.js + Tailwind CSS"
        UI["📊 Dashboard UI"]
        FORMS["📝 Daily Input Forms"]
        CHARTS["📈 Trend Visualizations (Recharts)"]
        SIM_UI["🔮 Simulation Interface"]
    end

    subgraph "🌐 API Layer — FastAPI (Python)"
        VALIDATE["✅ Validation (Pydantic)"]
        ROUTES["🛣 Routes: /predict, /simulate, /health"]
        SWAGGER["📄 Swagger Auto-Docs"]
    end

    subgraph "🧠 Core Processing Engine"
        FE["⚙ Feature Engineering"]
        CTX["🎯 Context Detection (Animal State)"]
        
        subgraph "🤖 Risk Engine (Hybrid)"
            RULE["📏 Rule Engine"]
            ML["🧪 ML Model (LR / RF)"]
            VOICE["🔊 Voice Module (Librosa)"]
        end
        
        FUSION["🔥 Risk Fusion Engine"]
        EXPLAIN["🔍 Explainability (SHAP)"]
        SIM["🔮 Simulation Engine"]
    end

    subgraph "🗄 Storage Layer"
        DB["💾 SQLite (MVP) / PostgreSQL (Scale)"]
        MODEL_STORE["📦 Model Store (joblib .pkl)"]
    end

    F --> UI
    UI --> FORMS
    UI --> CHARTS
    UI --> SIM_UI
    FORMS --> VALIDATE
    SIM_UI --> ROUTES
    VALIDATE --> ROUTES
    ROUTES --> FE
    FE --> CTX
    CTX --> RULE
    CTX --> ML
    CTX --> VOICE
    RULE --> FUSION
    ML --> FUSION
    VOICE --> FUSION
    FUSION --> EXPLAIN
    EXPLAIN --> SIM
    SIM --> ROUTES
    ROUTES --> UI
    ML -.-> MODEL_STORE
    ROUTES -.-> DB
    
    style FUSION fill:#FF6B6B,stroke:#333,color:#fff
    style CTX fill:#4ECDC4,stroke:#333,color:#fff
    style SIM fill:#A855F7,stroke:#333,color:#fff
    style EXPLAIN fill:#F59E0B,stroke:#333,color:#fff
```

---

## 3. 🔄 End-to-End Workflow Flowchart

This is the **master flowchart** showing the complete system pipeline from farmer input to actionable output.

```mermaid
flowchart TD
    START(["🧑‍🌾 Farmer Opens App"]) --> SELECT["Select Animal by ID"]
    SELECT --> INPUT["Enter Daily Data"]
    
    INPUT --> MILK["🥛 Milk Yield (optional, numeric)"]
    INPUT --> FEED["🌾 Feed Intake (low/medium/high)"]
    INPUT --> ACTIVITY["🏃 Activity Level (low/medium/high)"]
    INPUT --> TEMP["🌡 Temperature (°C)"]
    
    MILK --> SUBMIT["📤 Submit"]
    FEED --> SUBMIT
    ACTIVITY --> SUBMIT
    TEMP --> SUBMIT
    
    SUBMIT --> VAL{"✅ Validation"}
    VAL -->|"Invalid"| ERR_422["⛔ 422: Invalid Input"]
    VAL -->|"Missing Data"| ERR_400["⛔ 400: Missing Data"]
    VAL -->|"Valid ✓"| FE_STEP["⚙ Feature Engineering"]
    
    FE_STEP --> DERIVE["Derive Signals:<br/>• milk_drop %<br/>• activity_score<br/>• feed_score<br/>• temp_risk"]
    DERIVE --> VECTOR["📊 Feature Vector"]
    
    VECTOR --> CTX_CHECK{"🎯 Context Check:<br/>Animal State?"}
    CTX_CHECK -->|"Lactating"| LACT["Use ALL signals<br/>(milk + feed + activity + temp)"]
    CTX_CHECK -->|"Dry"| DRY["Ignore milk signals<br/>(behavior + health only)"]
    
    LACT --> RISK_ENGINE["🤖 Risk Engine"]
    DRY --> RISK_ENGINE
    
    RISK_ENGINE --> RULE_CALC["📏 Rule-Based Score"]
    RISK_ENGINE --> ML_CALC["🧪 ML Prediction<br/>model.predict(features)"]
    RISK_ENGINE --> VOICE_CALC["🔊 Voice Score<br/>(optional, low weight)"]
    
    RULE_CALC --> FUSE["🔥 Risk Fusion"]
    ML_CALC --> FUSE
    VOICE_CALC --> FUSE
    
    FUSE --> SCORE["Risk Score: 0-100"]
    SCORE --> LEVEL{"Risk Level?"}
    LEVEL -->|"0-39"| LOW["🟢 LOW"]
    LEVEL -->|"40-69"| MED["🟡 MEDIUM"]
    LEVEL -->|"70-100"| HIGH["🔴 HIGH"]
    
    LOW --> EXPLAIN_STEP["🔍 Explainability<br/>(SHAP Feature Importance)"]
    MED --> EXPLAIN_STEP
    HIGH --> EXPLAIN_STEP
    
    EXPLAIN_STEP --> REASONS["📋 Top Risk Factors:<br/>• Milk decreased<br/>• Activity low<br/>• Temperature high"]
    REASONS --> ACTIONS["💊 Suggested Actions:<br/>• Improve diet<br/>• Monitor closely<br/>• Veterinary check"]
    
    ACTIONS --> RESPONSE["📤 Response to Dashboard"]
    RESPONSE --> SIM_Q{"🔮 Run Simulation?"}
    SIM_Q -->|"Yes"| SIM_MOD["User Modifies Inputs"]
    SIM_Q -->|"No"| DISPLAY["📊 Display Results"]
    
    SIM_MOD --> RECOMPUTE["Recompute Features"]
    RECOMPUTE --> RERUN["Re-run Model"]
    RERUN --> COMPARE["Compare: Before vs After"]
    COMPARE --> DELTA["Δ Delta:<br/>Before: 70 → After: 52<br/>Improvement: -18"]
    DELTA --> DISPLAY
    
    DISPLAY --> STORE["💾 Store in History (SQLite)"]
    STORE --> TREND["📈 Update Trend Charts"]
    TREND --> END_STATE(["✅ Complete"])

    style START fill:#10B981,stroke:#333,color:#fff
    style FUSE fill:#FF6B6B,stroke:#333,color:#fff
    style CTX_CHECK fill:#4ECDC4,stroke:#333,color:#fff
    style SIM_Q fill:#A855F7,stroke:#333,color:#fff
    style HIGH fill:#EF4444,stroke:#333,color:#fff
    style MED fill:#F59E0B,stroke:#333,color:#fff
    style LOW fill:#10B981,stroke:#333,color:#fff
    style END_STATE fill:#6366F1,stroke:#333,color:#fff
```

---

## 4. 🧠 Core Innovation Deep-Dives

### 4.1 🎯 Context-Aware Risk Engine (Key Innovation #1)

The system doesn't apply a single static model. It **adapts based on the animal's lifecycle stage**, which is critical for accuracy.

```mermaid
flowchart LR
    subgraph "Animal Profile"
        PROFILE["🐄 Animal<br/>ID: COW-12<br/>Breed: Holstein<br/>Age: 4yrs"]
    end
    
    PROFILE --> STATE{"Lifecycle<br/>State?"}
    
    STATE -->|"🍼 Lactating"| LACT_SIGNALS["Full Signal Set:<br/>✅ Milk Yield<br/>✅ Feed Intake<br/>✅ Activity Level<br/>✅ Temperature<br/>✅ Behavior<br/>✅ Voice (opt)"]
    
    STATE -->|"☀️ Dry Period"| DRY_SIGNALS["Reduced Signal Set:<br/>❌ Milk Yield (ignored)<br/>✅ Feed Intake<br/>✅ Activity Level<br/>✅ Temperature<br/>✅ Behavior<br/>✅ Voice (opt)"]
    
    LACT_SIGNALS --> LACT_WEIGHTS["Weighted Risk Weights:<br/>milk_weight: HIGH<br/>feed_weight: MEDIUM<br/>activity_weight: MEDIUM<br/>temp_weight: HIGH"]
    
    DRY_SIGNALS --> DRY_WEIGHTS["Adjusted Risk Weights:<br/>feed_weight: HIGH<br/>activity_weight: HIGH<br/>temp_weight: HIGH<br/>behavior_weight: HIGH"]
    
    LACT_WEIGHTS --> ENGINE["🤖 Risk Engine"]
    DRY_WEIGHTS --> ENGINE
    
    style STATE fill:#4ECDC4,stroke:#333,color:#fff
    style ENGINE fill:#FF6B6B,stroke:#333,color:#fff
```

### 4.2 🔥 Multi-Signal Risk Fusion (Key Innovation #2)

Three independent scoring pathways are **fused** into a single composite risk score.

```mermaid
flowchart TD
    subgraph "📏 Rule Engine Path"
        R1["IF milk_drop > 15%<br/>AND activity_low → HIGH RISK"]
        R2["IF temp > 39.5°C → FLAG"]
        R3["IF feed_low > 2 days → WARNING"]
        R1 --> RULE_SCORE["Rule Score: 0-100"]
        R2 --> RULE_SCORE
        R3 --> RULE_SCORE
    end
    
    subgraph "🧪 ML Model Path"
        ML_INPUT["Feature Vector"] --> ML_PREDICT["model.predict(features)"]
        ML_PREDICT --> ML_PROB["Probability → Score: 0-100"]
    end
    
    subgraph "🔊 Voice Analysis Path (Optional)"
        AUDIO["Audio Input (.wav)"] --> LIBROSA["Librosa: Extract pitch, energy"]
        LIBROSA --> CLASSIFY["Classify: normal / stress"]
        CLASSIFY --> V_SCORE["Voice Score (low weight)"]
    end
    
    RULE_SCORE --> FUSION["🔥 Risk Fusion Engine<br/>(Weighted Combination)"]
    ML_PROB --> FUSION
    V_SCORE -.->|"optional"| FUSION
    
    FUSION --> FINAL["Final Composite Risk Score"]
    
    style FUSION fill:#FF6B6B,stroke:#333,color:#fff
    style FINAL fill:#6366F1,stroke:#333,color:#fff
```

### 4.3 🔮 Simulation Engine — Unique Selling Proposition (Key Innovation #3)

The simulation engine allows farmers to **ask "what-if" questions** before taking action.

```mermaid
sequenceDiagram
    participant F as 🧑‍🌾 Farmer
    participant UI as 📊 Dashboard
    participant SIM as 🔮 Simulation Engine
    participant ML as 🤖 Risk Model
    
    F->>UI: Views current risk: Score 70 (HIGH)
    F->>UI: Opens Simulation Mode
    F->>UI: Modifies input: feed = "high" (was "low")
    UI->>SIM: Send modified inputs
    SIM->>SIM: Recompute feature vector
    SIM->>ML: Re-run prediction with new features
    ML-->>SIM: New risk probability
    SIM->>SIM: Compare old vs new
    SIM-->>UI: Delta Report
    
    Note over UI: Before: 70 (HIGH)<br/>After: 52 (MEDIUM)<br/>Improvement: -18 points
    
    UI-->>F: "If you improve feed,<br/>risk drops by 18 points"
    F->>F: Makes informed decision ✅
```

---

## 5. 🤖 ML Training Pipeline

```mermaid
flowchart TD
    subgraph "📦 Data Preparation"
        DS["Raw Dataset"] --> CLEAN["🧹 Data Cleaning<br/>(handle nulls, outliers)"]
        CLEAN --> ENCODE["🔢 Encoding<br/>(categorical → numeric)<br/>feed: low=0, med=1, high=2"]
        ENCODE --> NORM["📐 Normalization<br/>(scale features 0-1)"]
    end
    
    subgraph "⚙ Feature Engineering"
        NORM --> FE_CALC["Compute Derived Features:<br/>• milk_drop_pct<br/>• activity_score (0-1)<br/>• feed_score (0-1)<br/>• temp_risk_flag"]
        FE_CALC --> FV["Feature Vector Matrix"]
    end
    
    subgraph "🧪 Model Training"
        FV --> SPLIT["Train/Test Split<br/>(80% / 20%)"]
        SPLIT --> TRAIN_LR["Logistic Regression<br/>(Baseline Model)"]
        SPLIT --> TRAIN_RF["Random Forest<br/>(Advanced Model)"]
        TRAIN_LR --> EVAL["📊 Evaluation<br/>(Accuracy, Precision, Recall, F1)"]
        TRAIN_RF --> EVAL
    end
    
    subgraph "💾 Model Persistence"
        EVAL --> SELECT["Select Best Model"]
        SELECT --> SAVE["joblib.dump(model, 'model.pkl')"]
        SAVE --> DEPLOY["Deploy to FastAPI<br/>prediction service"]
    end
    
    subgraph "🔍 Explainability Layer"
        DEPLOY --> SHAP["SHAP Analysis"]
        SHAP --> IMPORTANCE["Feature Importance Rankings"]
        IMPORTANCE --> REASONS["Human-Readable Reasons"]
    end
    
    style TRAIN_LR fill:#3B82F6,stroke:#333,color:#fff
    style TRAIN_RF fill:#10B981,stroke:#333,color:#fff
    style SHAP fill:#F59E0B,stroke:#333,color:#fff
```

---

## 6. 📁 Project Structure & Module Map

```mermaid
graph TD
    subgraph "📁 backend/"
        MAIN["main.py<br/>(FastAPI app entry)"]
        
        subgraph "routes/"
            R_PREDICT["predict.py"]
            R_SIMULATE["simulate.py"]
            R_HEALTH["health.py"]
        end
        
        subgraph "schemas/"
            S_INPUT["input_schema.py<br/>(Pydantic models)"]
            S_OUTPUT["output_schema.py"]
        end
        
        subgraph "services/"
            SVC_FE["feature_engineering.py"]
            SVC_PRED["prediction.py"]
            SVC_SIM["simulation.py"]
            SVC_EXP["explainability.py"]
        end
        
        subgraph "models/"
            M_PKL["model.pkl<br/>(trained model)"]
        end
        
        subgraph "utils/"
            U_CONTEXT["context_logic.py"]
            U_VOICE["voice_analysis.py"]
        end
    end
    
    subgraph "📁 frontend/"
        subgraph "pages/"
            P_INDEX["index.js (Dashboard)"]
            P_TRACK["track.js (Daily Input)"]
            P_SIM["simulate.js (What-If)"]
        end
        
        subgraph "components/"
            C_RISK["RiskCard.jsx"]
            C_TREND["TrendChart.jsx"]
            C_FORM["InputForm.jsx"]
        end
        
        subgraph "hooks/"
            H_API["useAPI.js"]
            H_FORM["useFormState.js"]
        end
    end
    
    MAIN --> R_PREDICT
    MAIN --> R_SIMULATE
    MAIN --> R_HEALTH
    R_PREDICT --> S_INPUT
    R_PREDICT --> SVC_FE
    SVC_FE --> SVC_PRED
    SVC_PRED --> M_PKL
    SVC_PRED --> SVC_EXP
    R_SIMULATE --> SVC_SIM
    SVC_FE --> U_CONTEXT
    SVC_PRED --> U_VOICE
```

---

## 7. 🌐 API Contract

```mermaid
graph LR
    subgraph "📥 Endpoints"
        EP1["POST /predict"]
        EP2["POST /simulate"]
        EP3["GET /health"]
    end
    
    subgraph "📤 /predict Response"
        RES1["risk_score: 72<br/>risk_level: 'HIGH'<br/>reasons: ['Milk decreased', 'Activity low']<br/>actions: ['Improve diet', 'Monitor closely']"]
    end
    
    subgraph "📤 /simulate Response"
        RES2["before_score: 70<br/>after_score: 52<br/>delta: -18<br/>improved_factors: ['feed']"]
    end
    
    subgraph "📤 /health Response"
        RES3["status: 'ok'<br/>model_loaded: true<br/>version: '1.0'"]
    end
    
    EP1 --> RES1
    EP2 --> RES2
    EP3 --> RES3
```

### Input Schema (Pydantic)

| Field | Type | Required | Constraints | Notes |
|---|---|---|---|---|
| `animal_id` | string | ✅ | Non-empty | Unique animal identifier |
| `breed` | string | ✅ | Enum | Animal breed |
| `age` | number | ✅ | > 0 | Age in years |
| `state` | enum | ✅ | `lactating` \| `dry` | Drives context-aware logic |
| `milk_yield` | number | ❌ | ≥ 0 | Optional; ignored if `dry` |
| `feed_intake` | enum | ✅ | `low` \| `medium` \| `high` | Categorical input |
| `activity_level` | enum | ✅ | `low` \| `medium` \| `high` | Categorical input |
| `temperature` | number | ✅ | 35–42°C | Body temperature |

### Error Handling

| HTTP Code | Condition | Trigger |
|---|---|---|
| `422` | Invalid input | Out-of-range values, wrong types |
| `400` | Missing data | Required fields absent |
| `500` | System error | Model failure, service crash |

---

## 8. 🚀 Deployment Architecture

```mermaid
graph TB
    subgraph "🌍 Production Deployment"
        subgraph "Frontend Hosting"
            VERCEL["☁ Vercel<br/>(Next.js SSR)"]
        end
        
        subgraph "Backend Hosting"
            RENDER["☁ Render / Railway<br/>(FastAPI + ML)"]
        end
        
        subgraph "Infrastructure"
            DOCKER["🐳 Docker<br/>(Containerization)"]
            NGINX["🔧 Nginx<br/>(Production Server)"]
        end
        
        subgraph "Optional Enhancements"
            REDIS["⚡ Redis<br/>(Caching)"]
            CELERY["🔄 Celery<br/>(Async Jobs)"]
        end
    end
    
    subgraph "🧑‍💻 Development"
        GIT["📦 Git + GitHub"]
        PYTEST["🧪 Pytest"]
        POSTMAN["📮 Postman<br/>(API Testing)"]
    end
    
    VERCEL <-->|"REST API"| RENDER
    RENDER --- DOCKER
    DOCKER --- NGINX
    RENDER -.-> REDIS
    RENDER -.-> CELERY
    GIT --> VERCEL
    GIT --> RENDER
```

---

## 9. ⚙ Complete Tech Stack Matrix

| Layer | Technology | Purpose | Status |
|---|---|---|---|
| **Frontend Framework** | Next.js (React SSR) | Dashboard, forms, SSR | 🟢 Core |
| **UI Styling** | Tailwind CSS | Rapid UI development | 🟢 Core |
| **Charts** | Recharts | Trend visualizations | 🟢 Core |
| **State Management** | React Hooks (useState, useEffect) | Local state | 🟢 Core |
| **Form Handling** | React Hook Form | Form validation & state | 🟢 Core |
| **Backend Framework** | FastAPI (Python) | REST API, async support | 🟢 Core |
| **Validation** | Pydantic | Input/output schemas | 🟢 Core |
| **API Documentation** | Swagger (auto-generated) | Auto API docs | 🟢 Core |
| **ML Library** | scikit-learn | Model training & prediction | 🟢 Core |
| **Data Processing** | pandas, numpy | Data manipulation | 🟢 Core |
| **Model Persistence** | joblib (.pkl files) | Save/load trained models | 🟢 Core |
| **Explainability** | SHAP | Feature importance | 🟢 Core |
| **Audio Processing** | Librosa | Voice stress analysis | 🟡 Optional |
| **Database (MVP)** | SQLite | Zero-setup file-based DB | 🟢 Core |
| **Database (Scale)** | PostgreSQL | Production-grade DB | 🔵 Future |
| **Containerization** | Docker | Reproducible environments | 🟢 Core |
| **Frontend Hosting** | Vercel | Edge deployment | 🟢 Core |
| **Backend Hosting** | Render / Railway | Python service hosting | 🟢 Core |
| **Caching** | Redis | Performance optimization | 🟡 Optional |
| **Async Jobs** | Celery | Background processing | 🟡 Optional |
| **Production Server** | Nginx | Reverse proxy | 🟡 Optional |
| **Version Control** | Git + GitHub | Source management | 🟢 Core |
| **Testing** | Pytest | Unit/integration tests | 🟢 Core |
| **API Testing** | Postman | Manual API testing | 🟢 Core |

---

## 10. 📊 Feature Engineering Pipeline Detail

```mermaid
flowchart LR
    subgraph "Raw Inputs"
        RM["🥛 milk_yield: 15L"]
        RF["🌾 feed_intake: low"]
        RA["🏃 activity: low"]
        RT["🌡 temperature: 39.8°C"]
    end
    
    subgraph "Derived Signals"
        DM["milk_drop_pct:<br/>(baseline - current) / baseline<br/>= (20-15)/20 = 25%"]
        DF["feed_score:<br/>low=0, medium=0.5, high=1.0<br/>= 0.0"]
        DA["activity_score:<br/>low=0, medium=0.5, high=1.0<br/>= 0.0"]
        DT["temp_risk:<br/>39.8 > 39.5 → FLAG<br/>= 1 (abnormal)"]
    end
    
    subgraph "Feature Vector"
        FV["[0.25, 0.0, 0.0, 1]"]
    end
    
    RM --> DM
    RF --> DF
    RA --> DA
    RT --> DT
    DM --> FV
    DF --> FV
    DA --> FV
    DT --> FV
    
    style FV fill:#6366F1,stroke:#333,color:#fff
```

---

## 11. 📈 Trend Tracking & Alerting System

```mermaid
flowchart TD
    DAILY["📅 Daily Data Entry"] --> STORE["💾 Store in SQLite History"]
    STORE --> ANALYZE["📊 Trend Analysis"]
    
    ANALYZE --> MILK_T["🥛 Milk Trend<br/>(Day-over-day change)"]
    ANALYZE --> ACT_T["🏃 Activity Trend<br/>(Day-over-day change)"]
    ANALYZE --> TEMP_T["🌡 Temp Trend<br/>(Moving average)"]
    
    MILK_T --> DETECT{"Declining<br/>Pattern?"}
    ACT_T --> DETECT
    TEMP_T --> DETECT
    
    DETECT -->|"Yes"| ALERT["⚠ Trend Alert<br/>Notify farmer of<br/>emerging pattern"]
    DETECT -->|"No"| NORMAL["✅ Normal<br/>Continue monitoring"]
    
    ALERT --> DASHBOARD["📊 Dashboard Update<br/>(Recharts visualization)"]
    NORMAL --> DASHBOARD
    
    style ALERT fill:#EF4444,stroke:#333,color:#fff
    style NORMAL fill:#10B981,stroke:#333,color:#fff
```

---

## 12. 🔐 Validation Flow

```mermaid
flowchart TD
    INPUT["📥 Incoming Data"] --> CHECK_RANGE{"Range Check"}
    
    CHECK_RANGE -->|"milk < 0"| REJECT_422["⛔ 422 Unprocessable"]
    CHECK_RANGE -->|"temp < 35 or > 42"| REJECT_422
    CHECK_RANGE -->|"Valid ranges ✓"| CHECK_MISSING{"Missing Value Check"}
    
    CHECK_MISSING -->|"Required fields missing"| REJECT_400["⛔ 400 Bad Request"]
    CHECK_MISSING -->|"All present ✓"| CHECK_TYPE{"Type Validation<br/>(Pydantic)"}
    
    CHECK_TYPE -->|"Wrong types"| REJECT_422
    CHECK_TYPE -->|"All valid ✓"| PASS["✅ Proceed to<br/>Feature Engineering"]
    
    style REJECT_422 fill:#EF4444,stroke:#333,color:#fff
    style REJECT_400 fill:#F59E0B,stroke:#333,color:#fff
    style PASS fill:#10B981,stroke:#333,color:#fff
```

---

## 13. 🧩 Component Interaction Map

```mermaid
graph TD
    subgraph "🖥 Frontend Components"
        AnimalSelector["AnimalSelector"]
        InputForm["InputForm<br/>(React Hook Form)"]
        RiskCard["RiskCard"]
        TrendChart["TrendChart<br/>(Recharts)"]
        SimPanel["SimulationPanel"]
        ExplainView["ExplainabilityView"]
    end
    
    subgraph "🪝 Hooks"
        useAPI["useAPI()"]
        useForm["useFormState()"]
    end
    
    subgraph "🌐 API Calls"
        POST_PREDICT["POST /predict"]
        POST_SIM["POST /simulate"]
    end
    
    AnimalSelector -->|"selected animal"| InputForm
    InputForm -->|"form data"| useForm
    useForm -->|"validated data"| useAPI
    useAPI -->|"request"| POST_PREDICT
    POST_PREDICT -->|"risk response"| RiskCard
    POST_PREDICT -->|"reasons"| ExplainView
    POST_PREDICT -->|"history"| TrendChart
    
    SimPanel -->|"modified inputs"| useAPI
    useAPI -->|"request"| POST_SIM
    POST_SIM -->|"delta response"| SimPanel
```

---

## 14. ⚡ Performance Requirements

| Metric | Target | Rationale |
|---|---|---|
| API Response Time | < 2 seconds | Real-time farmer usability |
| Simulation Response | < 1.5 seconds | Interactive what-if experience |
| Model Inference | Lightweight | Edge-compatible, no GPU needed |
| Frontend Load | SSR + Hydration | Fast initial paint via Next.js SSR |

---

## 15. 🔮 Future Roadmap

```mermaid
timeline
    title LHIS Evolution Roadmap
    section MVP (Current)
        Manual data input : Daily tracking
        SQLite storage : File-based DB
        Basic ML models : LR + RF
    section Phase 2
        IoT Sensor Integration : Automated data collection
        Real-time Monitoring : Continuous health stream
        PostgreSQL Migration : Production database
    section Phase 3
        Multi-Animal Analytics : Herd-level insights
        Mobile App Deployment : On-field access
        Advanced ML : Deep learning models
    section Phase 4
        Predictive Epidemiology : Herd outbreak prediction
        Marketplace Integration : Vet service connections
        Multi-Farm Federation : Regional analytics
```

---

## 16. ⚠ Known Limitations

> [!WARNING]
> **These are acknowledged constraints of the current MVP:**

| Limitation | Impact | Mitigation Path |
|---|---|---|
| **Manual data input** | User burden, data gaps | IoT sensors in Phase 2 |
| **No clinical validation** | Not a diagnostic tool | Partner with veterinary institutions |
| **Limited dataset** | Model accuracy ceiling | Crowdsource data from pilot farms |
| **No real-time monitoring** | Delayed detection | Streaming pipeline in Phase 2 |
| **Single-animal focus** | No herd-level insights | Multi-animal analytics in Phase 3 |

---

## 17. 🧠 Cognitive Summary — Why LHIS Matters

```mermaid
mindmap
    root((🧠 LHIS))
        🎯 Problem
            Reactive healthcare
            Fragmented data
            No personalization
            Financial losses
        💡 Innovation
            Context-Aware Engine
                Adapts to lifecycle stage
                Lactating vs Dry logic
            Multi-Signal Fusion
                Rule + ML + Voice
                Weighted combination
            Simulation Engine (USP)
                What-if scenarios
                Pre-action validation
            SHAP Explainability
                Transparent predictions
                Farmer-understandable reasons
        ⚙ Architecture
            Next.js Frontend
            FastAPI Backend
            scikit-learn ML
            SQLite Storage
        📈 Impact
            Reactive → Proactive
            Static → Interactive
            Guess → Data-driven
```

> [!IMPORTANT]
> **The three pillars that make LHIS unique:**
> 1. **Context-Awareness** — System adapts its risk calculation based on whether an animal is lactating or dry, ensuring different lifecycle stages get appropriate analysis
> 2. **Multi-Signal Fusion** — Combines rule-based logic, ML predictions, and optional voice analysis into a single risk score rather than treating signals in isolation
> 3. **Simulation Engine (USP)** — Farmers can modify inputs and see predicted risk changes *before* taking action, turning the system from an observer into a decision-support tool

---

*Analysis generated from 3 project documents comprising 21 pages of technical specification, covering system design, tech stack, and product requirements.*
