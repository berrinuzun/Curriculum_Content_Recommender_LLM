import google.generativeai as genai
import os
import re

try:
    genai.configure(api_key=os.environ["API_KEY"])
except KeyError:
    raise Exception("API key not found. Please set the API_KEY environment variable.")

generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=role, generation_config=generation_config)

    def generate_response(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
    
    def remove_quotes(self, text):
 
        text = text.replace('*', '').replace('#', '').replace('_', '')  
        text = re.sub(r"[\"'].+?[\"']", '', text)
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        text = re.sub(r'\[.*?\]\(.*?\)', '', text)   

        text = text.replace('\\n', '\n')
        text = re.sub(r'\s+', ' ', text).strip()

        return text
   
