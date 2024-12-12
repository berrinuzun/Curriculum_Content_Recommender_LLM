import google.generativeai as genai
import os

try:
    genai.configure(api_key=os.environ["API_KEY"])
except KeyError:
    raise Exception("API key not found. Please set the API_KEY environment variable.")

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=role)

    def generate_response(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
    
    def remove_quotes(self, text):
        return text.replace('*', '').replace('', '').replace('#', '')