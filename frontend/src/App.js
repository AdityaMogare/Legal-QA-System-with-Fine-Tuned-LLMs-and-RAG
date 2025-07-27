import React, { useState } from 'react';
import { Send, Loader2, Scale, BookOpen, MessageSquare, Zap } from 'lucide-react';
import axios from 'axios';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    const currentQuestion = question;
    setQuestion('');

    try {
      const response = await axios.post('/api/ask', {
        question: currentQuestion
      });

      const newChat = {
        question: currentQuestion,
        answer: response.data.answer,
        timestamp: new Date().toLocaleTimeString()
      };

      setChatHistory(prev => [...prev, newChat]);
      setAnswer(response.data.answer);
    } catch (error) {
      console.error('Error:', error);
      setAnswer('Sorry, I encountered an error while processing your question. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const exampleQuestions = [
    "What are Miranda rights?",
    "How does copyright law protect software?",
    "What constitutes workplace discrimination?",
    "What are the requirements for forming a contract?",
    "How does the Fourth Amendment protect privacy?"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-legal-50 to-legal-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-legal-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="bg-primary-600 p-2 rounded-lg">
                <Scale className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-legal-900">Legal QA System</h1>
                <p className="text-sm text-legal-600">Powered by AI & RAG</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-legal-600">
                <Zap className="h-4 w-4" />
                <span className="text-sm font-medium">Live</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Chat Area */}
          <div className="lg:col-span-2">
            <div className="card h-[600px] flex flex-col">
              <div className="flex items-center space-x-2 mb-4">
                <MessageSquare className="h-5 w-5 text-primary-600" />
                <h2 className="text-lg font-semibold text-legal-900">Ask Your Legal Question</h2>
              </div>
              
              {/* Chat History */}
              <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                {chatHistory.length === 0 ? (
                  <div className="text-center text-legal-500 py-8">
                    <BookOpen className="h-12 w-12 mx-auto mb-4 text-legal-300" />
                    <p>Start by asking a legal question below</p>
                  </div>
                ) : (
                  chatHistory.map((chat, index) => (
                    <div key={index} className="space-y-3">
                      <div className="bg-primary-50 p-3 rounded-lg">
                        <p className="text-legal-900 font-medium">Q: {chat.question}</p>
                        <p className="text-xs text-legal-500 mt-1">{chat.timestamp}</p>
                      </div>
                      <div className="bg-legal-50 p-3 rounded-lg">
                        <p className="text-legal-800">A: {chat.answer}</p>
                      </div>
                    </div>
                  ))
                )}
                
                {loading && (
                  <div className="flex items-center space-x-2 text-legal-600">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span>Processing your question...</span>
                  </div>
                )}
              </div>

              {/* Input Form */}
              <form onSubmit={handleSubmit} className="flex space-x-2">
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask a legal question..."
                  className="input-field flex-1"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={loading || !question.trim()}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Features */}
            <div className="card">
              <h3 className="text-lg font-semibold text-legal-900 mb-4">Features</h3>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <div className="bg-green-100 p-2 rounded-lg">
                    <Scale className="h-4 w-4 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-legal-900">Legal Expertise</p>
                    <p className="text-xs text-legal-600">Trained on 100K+ legal documents</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <BookOpen className="h-4 w-4 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-legal-900">RAG Technology</p>
                    <p className="text-xs text-legal-600">Retrieval-Augmented Generation</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="bg-purple-100 p-2 rounded-lg">
                    <Zap className="h-4 w-4 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-legal-900">Real-time Answers</p>
                    <p className="text-xs text-legal-600">Instant responses powered by AI</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Example Questions */}
            <div className="card">
              <h3 className="text-lg font-semibold text-legal-900 mb-4">Example Questions</h3>
              <div className="space-y-2">
                {exampleQuestions.map((example, index) => (
                  <button
                    key={index}
                    onClick={() => setQuestion(example)}
                    className="text-left text-sm text-legal-700 hover:text-primary-600 hover:bg-primary-50 p-2 rounded-lg transition-colors duration-200 w-full"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>

            {/* Disclaimer */}
            <div className="card bg-amber-50 border-amber-200">
              <h3 className="text-sm font-semibold text-amber-800 mb-2">Disclaimer</h3>
              <p className="text-xs text-amber-700">
                This AI system provides general legal information only and should not be considered as legal advice. 
                Always consult with a qualified attorney for specific legal matters.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 