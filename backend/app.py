from flask import Flask, render_template, request, jsonify
import openai
import os
import sys

# Set directory for frontend templates and create Flask instance
template_dir = os.path.abspath('../frontend')
app = Flask(__name__, template_folder=template_dir)

# Set the OpenAI API key, which should be set in your environment variables
openai.api_key = os.getenv('OPENAI_API_KEY') 

# Function to generate a response from the OpenAI GPT model
def generate_response(prompt): 
    try:
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            max_tokens=250,
            temperature=0.1
        )

        return response.choices[0].text.strip()
    except Exception as e:
        # If an error occurs, print it
        print(e, file=sys.stderr) 
        return "An error occurred while processing your request. Make sure you inserted the correct ChatGPT API key"

# Route for the main page
@app.route('/')
def index():
    return render_template('welcome.html')

# Route for the comparison tool page
@app.route('/index')
def comparison():
    return render_template('index.html') 

# Route for handling GPT queries
@app.route('/api/gpt-query', methods=['POST'])
def gpt_query():
    data = request.get_json() # Extracts the prompt

    # If prompt not provided will be an empty string
    prompt = data.get('prompt', '')  
    
    #Generates response of the prompt
    response_text = generate_response(prompt) 
    
    return jsonify(response=response_text)  

if __name__ == '__main__':
    app.run(debug=True, port=5001)
