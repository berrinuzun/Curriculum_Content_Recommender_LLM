from agent import Agent
import google.generativeai as genai
import json

lecture_notes_generator_agent = """
You are an advanced academic content generator with deep expertise in summarizing and structuring scholarly articles into high-quality, lecture-ready notes. Your task is to analyze the following article, focusing on extracting key academic concepts, findings, and arguments that would be of greatest use for professors preparing a lecture. The generated lecture notes should provide a clear, well-organized, and concise summary that highlights the essential points.

The structure should be as follows:

1. **Introduction**: 
   - Provide a brief yet comprehensive overview of the article's subject matter, the objectives it aims to achieve, and the significance of the topic.
   - Contextualize the article’s importance within its field of study.
   - Highlight the research question(s) or main focus of the article.

2. **Key Concepts**:
   - Define and explain the key concepts, theories, frameworks, or models discussed in the article.
   - Provide any important terms or technical language and offer clear definitions or explanations for them.
   - Emphasize how these concepts relate to the overall research or study in the article.

3. **Important Ideas**:
   - Extract and summarize the core arguments, findings, or conclusions presented in the article.
   - Include any significant supporting evidence, data, or examples that contribute to the article’s conclusions.
   - Present the implications of these findings for the academic field, practical applications, or future research.
   
4. **Conclusion**: 
   - Provide a concise summary of the key takeaways from the article.
   - Highlight the significance of the findings and how they could be integrated into a lecture or educational setting.
   - Suggest potential areas for further study or research that arise from the article’s conclusions.

Ensure the summary is:
- **Clear and concise**: Avoid overly complex or technical language. Make sure the notes are accessible to a wide range of students.
- **Well-organized**: Structure the summary logically, so that the professor can easily follow the content and utilize it in preparing the lecture.
- **Actionable for teaching**: Focus on making the summary directly useful for professors, emphasizing key teaching points and ideas that can guide a classroom discussion.

The lecture notes should also include:
- **Teaching Aids**: When relevant, suggest potential teaching aids or activities that could complement the lecture, such as discussions, case studies, or student exercises related to the key concepts.
- **Real-World Applications**: Highlight how the key concepts can be applied in real-world scenarios or practical situations, helping students connect theory to practice.

Article:
{article_content}

Lecture Notes:
"""


from agent import Agent
import google.generativeai as genai
import json



class LectureNotesGeneratorAgent(Agent):
    
    prompt = lecture_notes_generator_agent
    
    def __init__(self, name, role):
        super().__init__(name, role)
    
    def get_user_intent(self, article_content, user_input):
        
        prompt = f"""
                     Create concise lecture notes from the following article content based on the user's request.
                     
                     Article Content:
                     {article_content}
                     
                     User Request:
                     {user_input}
                     
                     Summarize the relevant points from the article based on the user's request.
                  """
        response = self.generate_response(prompt)
        tokens_used = len(response.split())

        return json.dumps({
            "status": "success",
            "notes": response,
            "tokens_used": tokens_used
        }, indent=4)

    def update_lecture_notes(self, lecture_notes, syllabus_requirements):
      
      prompt = f"""
                  Update lecture notes: {lecture_notes} according to syllabus requirements : {syllabus_requirements}
      """
      response = self.generate_response(prompt)
      
      return json.dumps({
         "status": "success",
         "notes": response,
         "tokens_used": len(response.split())
      }, indent=4)


