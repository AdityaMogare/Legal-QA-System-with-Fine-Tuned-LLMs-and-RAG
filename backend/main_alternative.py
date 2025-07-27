from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
import os
from dotenv import load_dotenv
import logging
import random

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Legal QA System API",
    description="API for the Legal QA System with fallback responses",
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

# Fallback legal responses for testing
LEGAL_RESPONSES = {
    "miranda": {
        "answer": "Miranda rights are constitutional protections that must be read to criminal suspects before police questioning. They include: 1) The right to remain silent, 2) The right to an attorney, 3) The right to have an attorney appointed if you cannot afford one, and 4) The warning that anything you say can be used against you in court. These rights stem from the 5th and 6th Amendments to the U.S. Constitution and were established in the landmark case Miranda v. Arizona (1966).",
        "confidence": 0.95
    },
    "copyright": {
        "answer": "Copyright law protects software as literary works under the Copyright Act of 1976. Software copyright protection covers: 1) Source code and object code, 2) User interfaces and screen displays, 3) Documentation and manuals. Protection is automatic upon creation and lasts for the author's life plus 70 years. However, copyright only protects the expression of ideas, not the ideas themselves. Fair use exceptions may apply for research, education, or reverse engineering.",
        "confidence": 0.92
    },
    "discrimination": {
        "answer": "Workplace discrimination occurs when an employer treats an employee or job applicant unfavorably because of protected characteristics. Protected classes include: race, color, religion, sex, national origin, age (40+), disability, and genetic information. Common forms include: hiring discrimination, pay disparities, promotion denials, harassment, and wrongful termination. The Equal Employment Opportunity Commission (EEOC) enforces federal anti-discrimination laws. Remedies may include back pay, reinstatement, and punitive damages.",
        "confidence": 0.89
    },
    "contract": {
        "answer": "A valid contract requires four essential elements: 1) Offer - a clear proposal to enter into an agreement, 2) Acceptance - unqualified agreement to the offer's terms, 3) Consideration - something of value exchanged between parties, and 4) Mutual intent - both parties intend to be bound. Additional requirements include: capacity to contract, legality of purpose, and proper form (written for certain types). Contracts can be express (written or oral) or implied from conduct.",
        "confidence": 0.91
    },
    "fourth_amendment": {
        "answer": "The Fourth Amendment protects against unreasonable searches and seizures by government officials. It requires: 1) Probable cause for searches and arrests, 2) Warrants issued by neutral magistrates, 3) Particularity in describing what can be searched or seized. Exceptions include: consent searches, plain view doctrine, exigent circumstances, and automobile searches. The exclusionary rule prevents illegally obtained evidence from being used in court. This protection applies to homes, persons, papers, and effects.",
        "confidence": 0.94
    }
}

def get_fallback_response(question: str) -> str:
    """
    Generate a fallback response based on the question content
    """
    question_lower = question.lower()
    
    # Check for specific legal topics
    if any(word in question_lower for word in ["miranda", "rights", "arrest"]):
        return LEGAL_RESPONSES["miranda"]["answer"]
    elif any(word in question_lower for word in ["copyright", "software", "intellectual property"]):
        return LEGAL_RESPONSES["copyright"]["answer"]
    elif any(word in question_lower for word in ["discrimination", "workplace", "employment"]):
        return LEGAL_RESPONSES["discrimination"]["answer"]
    elif any(word in question_lower for word in ["contract", "agreement", "offer", "acceptance"]):
        return LEGAL_RESPONSES["contract"]["answer"]
    elif any(word in question_lower for word in ["fourth amendment", "search", "seizure", "privacy"]):
        return LEGAL_RESPONSES["fourth_amendment"]["answer"]
    else:
        # Generic legal response
        return f"I understand you're asking about: '{question}'. This appears to be a legal question. While I can provide general legal information, please note that this is not legal advice. For specific legal matters, I recommend consulting with a qualified attorney who can provide personalized guidance based on your particular circumstances and jurisdiction."

def query_huggingface_model(prompt: str) -> str:
    """
    Try to query Hugging Face model, fallback to local responses if needed
    """
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    
    if not HUGGINGFACE_API_KEY:
        logger.warning("No Hugging Face API key found, using fallback responses")
        return get_fallback_response(prompt)
    
    # Try different legal models that support inference
    models_to_try = [
        "microsoft/DialoGPT-medium",  # General conversational model
        "gpt2",  # Fallback model
    ]
    
    for model in models_to_try:
        try:
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
                "Content-Type": "application/json"
            }
            
            formatted_prompt = f"Legal question: {prompt}\nAnswer:"
            
            payload = {
                "inputs": formatted_prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{model}",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    if "generated_text" in result[0]:
                        return result[0]["generated_text"]
                elif isinstance(result, dict) and "generated_text" in result:
                    return result["generated_text"]
                    
        except Exception as e:
            logger.warning(f"Failed to query model {model}: {e}")
            continue
    
    # If all models fail, use fallback
    logger.info("All Hugging Face models failed, using fallback response")
    return get_fallback_response(prompt)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Legal QA System API is running",
        "model": "Fallback Legal Assistant",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": "Fallback Legal Assistant"}

@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a legal question and get an answer
    """
    try:
        logger.info(f"Received question: {request.question}")
        
        # Get answer from model or fallback
        answer = query_huggingface_model(request.question)
        
        logger.info(f"Generated answer for question: {request.question[:50]}...")
        
        return QuestionResponse(
            answer=answer,
            model_used="Fallback Legal Assistant",
            confidence=0.85
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/model-info")
async def get_model_info():
    """Get information about the model being used"""
    return {
        "model_name": "Fallback Legal Assistant",
        "model_url": "https://huggingface.co/models",
        "description": "A legal assistant with fallback responses for common legal questions",
        "architecture": "Hybrid (API + Fallback)",
        "parameters": "Variable"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 