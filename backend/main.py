from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Legal QA System API",
    description="API for the Legal QA System powered by JurisPrae model",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    model_used: str
    confidence: Optional[float] = None

# Hugging Face API configuration
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/Enfysyz/JurisPrae"
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    logger.warning("HUGGINGFACE_API_KEY not found in environment variables. Please set it for production use.")

def query_huggingface_model(prompt: str) -> str:
    """
    Query the JurisPrae model on Hugging Face
    """
    if not HUGGINGFACE_API_KEY:
        # Fallback response for development
        return f"I'm sorry, but I need a Hugging Face API key to access the JurisPrae model. Please set the HUGGINGFACE_API_KEY environment variable. Your question was: {prompt}"
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Format the prompt for the legal model
    formatted_prompt = f"""You are a legal expert assistant. Please provide a clear, accurate, and helpful answer to the following legal question. 
    Remember to cite relevant legal principles and provide practical guidance when appropriate.
    
    Question: {prompt}
    
    Answer:"""
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
    }
    
    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Handle different response formats from Hugging Face
        if isinstance(result, list) and len(result) > 0:
            if "generated_text" in result[0]:
                return result[0]["generated_text"]
            elif "text" in result[0]:
                return result[0]["text"]
        
        # If the response format is different, try to extract the text
        if isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        
        # Fallback: return the raw response
        return str(result)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error querying Hugging Face API: {e}")
        raise HTTPException(status_code=500, detail=f"Error connecting to the model: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Legal QA System API is running",
        "model": "JurisPrae",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": "JurisPrae"}

@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a legal question and get an answer from the JurisPrae model
    """
    try:
        logger.info(f"Received question: {request.question}")
        
        # Get answer from the model
        answer = query_huggingface_model(request.question)
        
        logger.info(f"Generated answer for question: {request.question[:50]}...")
        
        return QuestionResponse(
            answer=answer,
            model_used="JurisPrae",
            confidence=0.85  # Placeholder confidence score
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/model-info")
async def get_model_info():
    """Get information about the model being used"""
    return {
        "model_name": "JurisPrae",
        "model_url": "https://huggingface.co/Enfysyz/JurisPrae",
        "description": "A legal expert model trained for legal question answering",
        "architecture": "LLaMA-based",
        "parameters": "8.03B"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 