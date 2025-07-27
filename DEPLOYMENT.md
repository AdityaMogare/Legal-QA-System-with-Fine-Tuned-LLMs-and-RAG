# 🚀 Deployment Guide

This guide covers deploying your Legal QA System to various platforms.

## 📋 Prerequisites

1. **Hugging Face API Key**: Get your API key from [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. **Git Repository**: Your code should be in a Git repository
3. **Model Access**: Ensure your JurisPrae model is accessible via the Hugging Face API

## 🔧 Environment Setup

Create a `.env` file in the `backend/` directory:

```bash
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

## 🌐 Platform Deployment Options

### 1. Render (Recommended for Full-Stack)

Render is perfect for hosting both frontend and backend together.

#### Setup Steps:

1. **Sign up** at [render.com](https://render.com)
2. **Connect your GitHub repository**
3. **Create a new Web Service**
4. **Configure the service**:
   - **Name**: `legal-qa-system`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Root Directory**: Leave empty (root of repo)
   - **Build Command**: Leave empty (uses Dockerfile)
   - **Start Command**: Leave empty (uses Dockerfile CMD)

#### Environment Variables:
Add these in Render dashboard:
```
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

#### Benefits:
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Auto-deploy on Git push
- ✅ Free tier available
- ✅ Easy scaling

### 2. Vercel (Frontend) + Railway (Backend)

#### Frontend on Vercel:

1. **Sign up** at [vercel.com](https://vercel.com)
2. **Import your repository**
3. **Configure build settings**:
   - **Framework Preset**: `Create React App`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

#### Backend on Railway:

1. **Sign up** at [railway.app](https://railway.app)
2. **Deploy from GitHub**
3. **Select the backend directory**
4. **Add environment variables**:
   ```
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   ```

#### Update Frontend API URL:
In `frontend/src/App.js`, update the axios base URL to your Railway backend URL.

### 3. Hugging Face Spaces

Perfect for showcasing your model with a web interface.

#### Setup Steps:

1. **Go to** [Hugging Face Spaces](https://huggingface.co/spaces)
2. **Create a new Space**
3. **Choose**: `Docker` template
4. **Upload your code** or connect GitHub repository

#### Space Configuration:
- **SDK**: `Docker`
- **Hardware**: `CPU` (free) or `GPU` (paid)
- **Visibility**: `Public` or `Private`

### 4. Local Development

#### Using Docker Compose:

```bash
# Clone the repository
git clone <your-repo-url>
cd Legal-QA-System-with-Fine-Tuned-LLMs-and-RAG

# Set up environment variables
cp backend/env.example backend/.env
# Edit backend/.env with your API key

# Build and run
docker-compose up --build
```

#### Manual Setup:

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## 🔒 Security Considerations

### Environment Variables:
- ✅ Never commit API keys to Git
- ✅ Use platform-specific secret management
- ✅ Rotate keys regularly

### CORS Configuration:
Update `backend/main.py` with your frontend domain:
```python
allow_origins=["https://your-domain.com", "http://localhost:3000"]
```

### Rate Limiting:
Consider adding rate limiting for production:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

## 📊 Monitoring & Analytics

### Health Checks:
- Endpoint: `/health`
- Returns model status and basic info

### Logging:
- Backend logs are available in platform dashboards
- Consider adding structured logging for production

### Performance:
- Monitor API response times
- Track model inference latency
- Set up alerts for errors

## 🚀 Production Checklist

- [ ] Environment variables configured
- [ ] CORS settings updated for production domain
- [ ] HTTPS enabled
- [ ] Health checks implemented
- [ ] Error handling in place
- [ ] Rate limiting configured
- [ ] Monitoring set up
- [ ] Backup strategy in place

## 🔧 Troubleshooting

### Common Issues:

1. **CORS Errors**: Update `allow_origins` in backend
2. **API Key Issues**: Verify Hugging Face API key is valid
3. **Model Loading**: Check if JurisPrae model is accessible
4. **Build Failures**: Ensure all dependencies are in requirements.txt

### Debug Commands:

```bash
# Check backend health
curl http://localhost:8000/health

# Test API endpoint
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are Miranda rights?"}'

# Check Docker logs
docker-compose logs legal-qa-app
```

## 📞 Support

For deployment issues:
1. Check platform-specific documentation
2. Review logs in platform dashboard
3. Verify environment variables
4. Test locally first

---

**Happy Deploying! 🎉** 