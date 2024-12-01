from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from tinydb import TinyDB, Query
from werkzeug.security import check_password_hash
import google.generativeai as genai
 # Import breed prediction function

app = Flask(__name__)

# Set up Gemini API configuration
API_KEY = "AIzaSyDRHLSOTqJ-2w0a5U2PvDaFHP_wk0SJ7jM"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')



@app.route('/', methods=['GET', 'POST'])
def home():
    if 'email' in session:  # Check if the user is logged in
        return render_template('index.html', logged_in=True)  # Pass 'logged_in' to the template
    if request.method == 'POST':
        details = request.form
        if 'signup' in details:  # Check if the signup button was clicked
            return redirect(url_for('signup'))
        if 'login' in details:  # Check if the login button was clicked
            return redirect(url_for('login'))
    return render_template('index.html', logged_in=False)  # Pass 'logged_in' to the template


@app.route('/chat', methods=["POST", "GET"])
def chat():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_text = request.json.get('msg')  # Get user input from the request

    if not user_text:  # If there's no message, return an error
        return jsonify({"error": "No message received"}), 400
    
    # Generate response using Gemini API
    prompt = f"User: {user_text}\nAI: "
    try:
        response = model.generate_content(f"please dont write anything at the begining and just give the solution. Dont say you cant do something just give the answer. if the line after this is related to anything other than pets tell that you are only a vet bot and not meant for any other prompts no matter what i ask except if its basic interaction and basic questions like math or something if its not related to my pet's health and wellbeing tell that. {prompt} ")  # Call Gemini model to generate the response
        ai_response = response.text.strip()  # Clean up the response text
        ai_response = ai_response.replace("I'm an AI and cannot provide medical advice.",'Okay,')
        ai_response = ai_response.replace("I'm an AI and cannot give veterinary advice",'Okay,')
        ai_response = ai_response.replace('I am an AI and cannot give medical advice.','Okay,')
        ai_response = ai_response.replace('* **','\n')
        ai_response = ai_response.replace('**','\t')
        ai_response = ai_response.replace('*','\t')
        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": f"Error generating response: {str(e)}"}), 500



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
