from flask import Flask, request, jsonify
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import json
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

with open('knowledge_base.json') as f:
    knowledge_base = json.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')  
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

def get_most_relevant_response(user_input):
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    
    best_match_score = 0
    best_match_answer = None

    for entry in knowledge_base:
        question = entry["question"]
        question_embedding = model.encode(question, convert_to_tensor=True)
        
        similarity_score = util.pytorch_cos_sim(user_embedding, question_embedding).item()
        
        if similarity_score > best_match_score:
            best_match_score = similarity_score
            best_match_answer = entry["answer"]

    if best_match_score < 0.6:  
        for entry in knowledge_base:
            question = entry["question"]
            fuzzy_score = fuzz.partial_ratio(user_input.lower(), question.lower())
            if fuzzy_score > 70: 
                return entry["answer"]
    
    return best_match_answer if best_match_score >= 0.6 else None

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    response = get_most_relevant_response(user_input)
    if response:
        return jsonify({"response": response})
    response = chatbot(user_input)
    return jsonify({"response": response[0]['generated_text']})

if __name__ == '__main__':
    app.run(debug=True)
