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
 
        # Remove unnecessary special characters while keeping structure
        text = text.replace('*', '')
        
        # Replace Markdown headers (e.g., ## Title) with clean new lines
        text = re.sub(r'#+\s?', '\n', text)  # Remove # and ensure a new line
        
        # Remove inline code (text between backticks)
        text = re.sub(r'`[^`]*`', '', text)
        
        # Remove Markdown images and links
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Remove images
        text = re.sub(r'\[.*?\]\(.*?\)', '', text)   # Remove links
        
        # Replace \n or escaped newlines with real newlines
        text = text.replace('\\n', '\n')
        
        # Normalize multiple newlines into a single one
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Ensure double spacing for readability
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
   
