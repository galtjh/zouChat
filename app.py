from flask import Flask, request, render_template
import csv
import os
from fuzzywuzzy import process

app = Flask(__name__)

# Load data
def load_data(filename):
    qa_pairs = {}
    if not os.path.exists(filename):
        print(f"[Error] CSV file '{filename}' not found!")
        return qa_pairs
    
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            try:
                question = row['utterance_zou'].strip()
                answer = row['response_zou'].strip()
                if question and answer:  # Only add if both exist
                    qa_pairs[question] = answer
            except KeyError as e:
                print(f"[Warning] Row {i} missing expected column: {e}. Row contents: {row}")
            except AttributeError:
                print(f"[Warning] Row {i} has invalid format or missing fields. Row contents: {row}")
    
    print(f"[Info] Loaded {len(qa_pairs)} Q&A pairs from CSV")
    return qa_pairs

qa_data = load_data('zou_intents_entities.csv')

def format_response(response):
    """Format response to display lists properly"""
    if ':' in response and ',' in response:
        parts = response.split(':', 1)
        if len(parts) == 2:
            header = parts[0].strip()
            items_text = parts[1].strip()
            items = [item.strip() for item in items_text.split(',')]
            
            # Format as numbered list
            formatted = f"{header}:\n"
            for i, item in enumerate(items, 1):
                formatted += f"{i}. {item}\n"
            return formatted
    return response

def get_best_match(user_input, threshold=80):    ### Low threshold gives wrong answers, high threshold trigger stock apoloygy ###
    if not qa_data:
        return "zouChat: CSV file thu hman theih lou e! Please check your data file."
    
    best_match, score = process.extractOne(user_input, qa_data.keys())
    if score >= threshold:
        raw_response = qa_data[best_match]
        return format_response(raw_response)
    return "Tami ka training data ah a um nai sih a, tu-le-tu in ka hing dawng thei nai sih hi. Maban a don thei pai ding ka ki lamen hi. Hing ngaisiam in. 👏\n\nA nuai a Sample Prompt te nang dong thei ding hi. Tualeh India a state capital te leh khovel pumpi a national capital tengteng ka thei hi. Ka theina tan, nang enkhe ut ei?"

@app.route("/", methods=["GET", "POST"])
def chat():
    user_input = ""
    bot_response = ""
    if request.method == "POST":
        user_input = request.form["message"]
        bot_response = get_best_match(user_input)
    return render_template("chat.html", user_input=user_input, bot_response=bot_response)

if __name__ == "__main__":
    print(f"[Info] Starting Zou Language Chatbot...")
    print(f"[Info] Data loaded: {len(qa_data)} entries")
    app.run(debug=True)




"""

from flask import Flask, request, render_template
import csv
from fuzzywuzzy import process

app = Flask(__name__)

# Load data
def load_data(filename):
    qa_pairs = {}
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            qa_pairs[row['utterance_zou'].strip()] = row['response_zou'].strip()
    return qa_pairs

qa_data = load_data('zou_intents_entities.csv')

def get_best_match(user_input, threshold=70):
    best_match, score = process.extractOne(user_input, qa_data.keys())
    if score >= threshold:
        return qa_data[best_match]
    return "zouChat: Na thugen thei siam sing e!"

@app.route("/", methods=["GET", "POST"])
def chat():
    user_input = ""
    bot_response = ""
    if request.method == "POST":
        user_input = request.form["message"]
        bot_response = get_best_match(user_input)
    return render_template("chat.html", user_input=user_input, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
    
    
    """
