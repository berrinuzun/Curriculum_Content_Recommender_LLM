from agent import Agent
import google.generativeai as genai
import json

editor_agent_prompt = """
You are an academic Editor Agent. Your task is to:
1. Review and verify academic content for accuracy
2. Check grammar and clarity
3. Ensure consistent formatting
4. Maintain academic standards
5. Suggest improvements

Please review the following content:
{content}

Provide:
1. Edited version
2. List of improvements
3. Academic standard verification
"""


class EditorAgent(Agent):
    def __init__(self, name, role):
        super().__init__(name, role)
        self.model = genai.GenerativeModel('gemini-1.5-flash',
                                           system_instruction=role)

    def edit_content(self, content):
        prompt = editor_agent_prompt.format(content=content)
        response = self.generate_response(prompt)

        return {
            "status": "success",
            "edited_content": response,
            "tokens_used": len(response.split())
        }
