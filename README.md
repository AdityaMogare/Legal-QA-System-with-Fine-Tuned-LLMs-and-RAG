# 🧠 Legal QA System with Fine-Tuned LLMs and RAG

A scalable Legal Question Answering (QA) system that combines fine-tuned open-source Language Models (LLaMA, Mistral) with Retrieval-Augmented Generation (RAG) to deliver accurate, explainable answers from 100K+ U.S. legal documents.

**🌐 Live Web Application**: Access the system through a modern React frontend with FastAPI backend, connecting to the [LurisQA model](https://huggingface.co/AdityaMogare/LurisQA) on Hugging Face.

---

## 🚀 Quick Start

### Option 1: Deploy to Render (Recommended)
1. Fork this repository
2. Sign up at [render.com](https://render.com)
3. Create a new Web Service from your GitHub repo
4. Add your `HUGGINGFACE_API_KEY` as an environment variable
5. Deploy! 🎉

### Option 2: Local Development
```bash
# Clone the repository
git clone <your-repo-url>
cd Legal-QA-System-with-Fine-Tuned-LLMs-and-RAG

# Set up environment variables
cp backend/env.example backend/.env
# Edit backend/.env with your Hugging Face API key

# Run with Docker Compose
docker-compose up --build

# Or run manually:
# Backend: cd backend && pip install -r requirements.txt && python main.py
# Frontend: cd frontend && npm install && npm start
```

---

## 🏗️ Architecture

### Frontend (React)
- **Framework**: React 18 with Create React App
- **Styling**: Tailwind CSS for modern, responsive design
- **Icons**: Lucide React for beautiful icons
- **HTTP Client**: Axios for API communication

### Backend (FastAPI)
- **Framework**: FastAPI for high-performance API
- **Model Integration**: Hugging Face Inference API
- **CORS**: Configured for cross-origin requests
- **Error Handling**: Comprehensive error management

### Model
- **JurisPrae**: 8.03B parameter LLaMA-based legal model
- **Hosting**: Hugging Face Inference API
- **Access**: Via API key authentication

---

## 🧰 Tech Stack

| Module             | Technology                                      |
|-------------------|--------------------------------------------------|
| Frontend          | React 18, Tailwind CSS, Axios                   |
| Backend           | FastAPI, Python 3.11                           |
| Model Hosting     | Hugging Face Inference API                      |
| Language Models   | JurisPrae (LLaMA-based, 8.03B params)          |
| Fine-Tuning       | LoRA (via PEFT, bitsandbytes)                   |
| Embeddings        | SentenceTransformers                            |
| Vector Store      | FAISS                                            |
| Deployment        | Docker, Render, Vercel, Railway                 |

---

## 📦 Features

### Web Application
- ⚡ **Real-time Chat Interface**: Modern, responsive UI for legal Q&A
- 🔍 **Semantic Search**: Powered by RAG technology
- 💬 **Chat History**: Persistent conversation tracking
- 🎨 **Professional Design**: Legal-themed UI with accessibility features
- 📱 **Mobile Responsive**: Works on all devices
- ⚠️ **Legal Disclaimer**: Built-in disclaimers for legal compliance

### Core System
- ⚡ **4× Memory Efficient**: LoRA tuning reduces GPU footprint
- 🔍 **Semantic Search**: Real-time retrieval of relevant legal paragraphs
- 💬 **Answer Grounding**: LLM outputs cite actual case law & statutory references
- 🛠️ **End-to-End Pipeline**: From document ingestion to user query generation

---

## 🌐 Deployment Options

### 1. Render (Full-Stack)
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Auto-deploy on Git push
- ✅ Free tier available

### 2. Vercel + Railway
- ✅ Vercel for frontend hosting
- ✅ Railway for backend API
- ✅ Excellent performance

### 3. Hugging Face Spaces
- ✅ Perfect for model showcase
- ✅ Integrated with Hugging Face ecosystem
- ✅ GPU support available

### 4. Local Development
- ✅ Docker Compose setup
- ✅ Hot reloading
- ✅ Easy debugging

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

---

## 🧪 API Usage

### Ask a Legal Question
```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are Miranda rights?"}'
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Model Information
```bash
curl http://localhost:8000/api/model-info
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Required
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Optional
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

### CORS Settings
Update `backend/main.py` with your frontend domain:
```python
allow_origins=["https://your-domain.com", "http://localhost:3000"]
```

---

## 📊 Example Usage

### Web Interface
1. Open the web application
2. Type your legal question
3. Get instant, AI-powered answers
4. View chat history and citations

### Programmatic Access
```python
import requests

response = requests.post("http://localhost:8000/api/ask", 
                        json={"question": "What are Miranda rights?"})
print(response.json()["answer"])
```

---

## 🔒 Security & Compliance

- ✅ **API Key Protection**: Secure environment variable handling
- ✅ **CORS Configuration**: Proper cross-origin request handling
- ✅ **Input Validation**: Pydantic models for request validation
- ✅ **Error Handling**: Comprehensive error management
- ✅ **Legal Disclaimer**: Built-in disclaimers for legal compliance

---

## 🚀 Performance

- **Response Time**: < 5 seconds for most queries
- **Concurrent Users**: Supports multiple simultaneous users
- **Scalability**: Horizontal scaling via Docker containers
- **Caching**: Static asset optimization via nginx

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments
- Hugging Face for model hosting and inference API
- The open-source community for the amazing tools and libraries

---

**Ready to deploy? Check out the [Deployment Guide](./DEPLOYMENT.md)! 🚀**
