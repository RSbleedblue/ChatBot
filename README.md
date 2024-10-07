## AI Chatbot with Hugging Face Transformers and Flask

This project is an AI-based chatbot built using Flask, Hugging Face `DialoGPT`, and a custom knowledge base in JSON format. It intelligently responds to user queries using semantic search, fuzzy matching for handling spelling mistakes, and generates responses with `DialoGPT` when a knowledge base match is not found.

### Features

- **Knowledge Base**: Responds to predefined questions from a JSON knowledge base.
- **Semantic Matching**: Uses sentence-transformer models to handle different question formats (e.g., active/passive voice).
- **Fuzzy Matching**: Handles minor spelling mistakes using fuzzy matching techniques.
- **AI Generation**: For unmatched questions, it generates text responses using Hugging Face's `DialoGPT` model.

### Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.7 or later
- `pip` (Python package installer)

### Installation

Follow these steps to set up and run the project:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/chatbot.git
   cd chatbot
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**
   Run the following command to install all required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the Knowledge Base File**
   Create a `knowledge_base.json` file in the project root directory with predefined questions and answers:
   ```json
   [
       {
           "question": "What are your opening hours?",
           "answer": "We are open from 9 AM to 5 PM, Monday to Friday."
       },
       {
           "question": "What services do you offer?",
           "answer": "We offer a variety of services including repairs, maintenance, and consultations."
       }
   ]
   ```

5. **Run the Application**
   Start the Flask app:
   ```bash
   python app.py
   ```

6. **Test the API**
   You can use `curl` or Postman to test the `/chat` endpoint. Here's a sample `curl` request:
   ```bash
   curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"message": "What are your services?"}'
   ```

### Dependencies

The following Python libraries are used in this project:

- `Flask`: Web framework for creating the REST API.
- `transformers`: Hugging Face library to integrate pre-trained models like `DialoGPT`.
- `fuzzywuzzy`: Library for fuzzy string matching to handle spelling mistakes.
- `sentence-transformers`: Provides pre-trained models for sentence embeddings and semantic search.
- `nltk` or `spacy` (optional): For further natural language processing like lemmatization, stopword removal, etc.

### requirements.txt

Here’s a `requirements.txt` file that lists all necessary dependencies:

```
Flask==2.3.3
transformers==4.34.0
fuzzywuzzy==0.18.0
sentence-transformers==2.2.2
torch==2.0.1
nltk==3.8.1  # Optional for extra NLP processing
```
