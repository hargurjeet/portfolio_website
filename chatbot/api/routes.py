from flask import Blueprint, request, jsonify
from chatbot.core.rag_chain import get_answer

api = Blueprint('api', __name__)

@api.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    # qa_chain should be initialized once and reused
    answer = get_answer(qa_chain, question)
    
    return jsonify({'answer': answer})
