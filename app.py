from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer
import json
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util
import os
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

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

@app.route('/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file_ext = os.path.splitext(file.filename)[1].lower()

    new_data = []

    if file_ext == '.csv':
        df = pd.read_csv(file)
    elif file_ext == '.xlsx':
        df = pd.read_excel(file)
    elif file_ext == '.json':
        new_data = json.load(file)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    if file_ext in ['.csv', '.xlsx']:
        for _, row in df.iterrows():
            if 'question' in row and 'answer' in row:
                new_data.append({
                    "question": row['question'],
                    "answer": row['answer']
                })
    knowledge_base.extend(new_data)

    with open('knowledge_base.json', 'w') as f:
        json.dump(knowledge_base, f)

    return jsonify({"message": "Data successfully uploaded and integrated."})

if __name__ == '__main__':
    app.run(debug=True)
