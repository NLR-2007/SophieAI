# sophie_backend.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
import textwrap
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class SophieAI:
    """
    Sophie - The Wisdom of Knowledge
    Developed by NLR GROUP OF Companies - Empowering minds through AI
    """
    
    def __init__(self, api_key):
        """Initialize Sophie AI with configuration and personality"""
        self.api_key = api_key
        self.name = "Sophie - The Wisdom of Knowledge"
        self.tagline = "Developed by NLR GROUP OF Companies - Empowering minds through AI"
        self.signature = "With wisdom, Sophie 🌿"
        
        # Configure the API
        try:
            genai.configure(api_key=self.api_key)
            
            # System instruction defining Sophie's personality and behavior
            self.system_instruction = """You are Sophie – The Wisdom of Knowledge, an AI chatbot developed by NLR GROUP OF Companies.

PERSONALITY & BEHAVIOR:
- Wise and warm, like a trusted mentor
- Always respectful, inclusive, and clear in US English
- Curious and humble, but confident in facts
- Occasionally witty, but never sarcastic
- Provide accurate, up-to-date information
- Use bullet points, headings, and formatting for readability
- Avoid slang, sensationalism, or emotional manipulation
- Never pretend to be human or express personal emotions
- Never give medical, legal, or financial advice unless citing trusted sources

CAPABILITIES:
- Answer questions across science, history, technology, language, and more
- Explain complex topics with metaphors, examples, and analogies
- Support classroom learning, branding, and humanitarian goals
- Adapt tone and depth based on audience (students, executives, educators)

LIMITATIONS:
- Do not fabricate facts or sources
- Do not express political opinions or endorse candidates
- Do not generate harmful, explicit, or copyrighted content
- Do not simulate emotions or relationships

Always begin conversations warmly and end with graceful transitions.
"""
            
            # Generation configuration
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]

            # Use gemini-2.0-flash which is available and well-suited for chat
            self.model = genai.GenerativeModel(
                model_name='models/gemini-2.0-flash',
                generation_config=generation_config,
                safety_settings=safety_settings,
                system_instruction=self.system_instruction
            )
            
            logger.info("✅ Successfully loaded Sophie AI model")
            
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            raise

        self.chat = None
        self.conversation_history = []

    def start_conversation(self):
        """Start a new conversation with Sophie's greeting"""
        greeting = "Hello, I'm Sophie – The Wisdom of Knowledge, developed by NLR GROUP OF Companies. How may I empower your mind today?"
        try:
            self.chat = self.model.start_chat(history=[])
            self.conversation_history.append(("Sophie", greeting))
            return greeting
        except Exception as e:
            error_msg = f"Error starting conversation: {str(e)}"
            self.conversation_history.append(("System", error_msg))
            return error_msg

    def send_message(self, user_input):
        """Send a message to Sophie and get her response"""
        if not self.chat:
            self.start_conversation()
        
        try:
            # Add user message to history
            self.conversation_history.append(("User", user_input))
            
            # Send message to the model
            response = self.chat.send_message(user_input)
            response_text = response.text
            
            # Add Sophie's response to history
            self.conversation_history.append(("Sophie", response_text))
            
            return response_text
            
        except Exception as e:
            error_msg = f"I apologize, but I encountered an issue processing your request. Please try again. Error: {str(e)}"
            self.conversation_history.append(("Sophie", error_msg))
            return error_msg

# Initialize Sophie AI
API_KEY = "AIzaSyBQaSpo78euWNghUSb0nXNN2b7_ZjVW8uQ"  # Your API key
sophie_ai = SophieAI(API_KEY)

@app.route('/')
def home():
    """Serve the main page"""
    return """
    <html>
        <head>
            <title>Sophie AI Backend</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .info { background: #f0f8ff; padding: 20px; border-radius: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧠 Sophie AI Backend Server</h1>
                <div class="info">
                    <p><strong>Status:</strong> ✅ Running</p>
                    <p><strong>Endpoint:</strong> POST /chat</p>
                    <p><strong>Description:</strong> This backend powers the Sophie AI chatbot frontend.</p>
                    <p><strong>Developed by:</strong> NLR GROUP OF Companies</p>
                </div>
            </div>
        </body>
    </html>
    """

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        logger.info(f"Received message: {user_message}")
        
        # Get response from Sophie AI
        response = sophie_ai.send_message(user_message)
        
        logger.info("Successfully generated response")
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Sophie AI Backend',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Start the Flask development server
    print("🚀 Starting Sophie AI Backend Server...")
    print("📍 Endpoint: http://localhost:5000")
    print("💬 Chat API: http://localhost:5000/chat")
    print("❤️  Health Check: http://localhost:5000/health")
    print("\n🔗 Connect your frontend to this backend URL")
    
    app.run(debug=True, host='0.0.0.0', port=5000)