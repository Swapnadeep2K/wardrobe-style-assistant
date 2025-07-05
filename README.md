# 👗 Wardrobe Style Assistant

A lightweight full-stack AI application that generates captions for clothing images and extracts fashion attributes like color, type, pattern, and fit using a rule-based system.

---

## 📦 Tech Stack

- **Backend**: FastAPI, Hugging Face Transformers (`vit-gpt2`), PyTorch, Pillow
- **Frontend**: React (coming soon)
- **Deployment**: Render (free tier), Docker

---

## 🧠 What It Does

Given a clothing image, it:
1. Uses the `vit-gpt2-image-captioning` model to generate a caption.
2. Extracts fashion-related attributes (e.g., sleeve length, color, type, etc.) using rule-based matching.
3. Returns JSON with both caption and detected attributes.

---

## 📁 Project Structure

```
wardrobe-style-assistant/
├── backend/         # FastAPI app with AI model
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── render.yaml
│   └── .dockerignore
├── frontend/        # React app (will be added later)
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### 🔧 Backend (FastAPI)

#### ▶️ Run Locally (Recommended for Dev)

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI

#### 🐳 Run via Docker

```bash
cd backend
docker build -t wardrobe-backend .
docker run -p 10000:10000 wardrobe-backend
```

Visit: [http://localhost:10000/docs](http://localhost:10000/docs)

---

### 🧪 API Endpoint

`POST /predict/`

**Body**: `multipart/form-data` with `file` as the image  
**Response**:

```json
{
  "caption": "a woman wearing a floral dress",
  "attributes": {
    "type": "dress",
    "pattern": "floral",
    "gender": "female",
    "style": "casual",
    ...
  }
}
```

---

### 🧠 Model Used

- `nlpconnect/vit-gpt2-image-captioning` from Hugging Face
- Inference happens at runtime
- Fashion attributes are extracted using rules in `app.py`

---

## 🌍 Deployment

This app can be deployed easily to Render:

#### render.yaml

```yaml
services:
  - type: web
    name: wardrobe-style-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app:app --host 0.0.0.0 --port 10000
    plan: free
```

---

## 🛣️ Roadmap

- ✅ FastAPI backend with model inference
- ✅ Rule-based fashion attribute extraction
- 🔲 React frontend UI for uploading images
- 🔲 Docker Compose to run frontend + backend together
- 🔲 Outfit recommendation engine

---

## 🧑‍💻 Author

**Swapnadeep Sarkar**  
FastAPI | Hugging Face | React | AEP Consultant

---

## 🪪 License

MIT License