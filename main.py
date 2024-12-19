import gradio as gr
from article_retrieval_agent import ArticleRetrievalAgent
from lecture_notes_generator_agent import LectureNotesGeneratorAgent
from storytelling_agent import StorytellingAgent
from editor_agent import EditorAgent
from pdf_generator_agent import PdfGeneratorAgent
from pdfminer.high_level import extract_text
import re
import json

def extract_pdf_text(pdf_path):
    text = extract_text(pdf_path)
    return text

def extract_syllabus_requirements(pdf_text):
    requirements = []
    pattern = r"(requirement|objective|goal|syllabus)\s*[:\-\s]*(.*)"
    matches = re.findall(pattern, pdf_text, re.IGNORECASE)
    for match in matches:
        requirements.append(match[1])
    return requirements

def format_json_output(json_output):
    # Convert the JSON dictionary into a formatted string with indentation
    return json.dumps(json_output, indent=4)

def process_request(user_input, chat_history, pdf_file=None):
    
    article_retrieval_agent = ArticleRetrievalAgent("Article Retrieval Agent", ArticleRetrievalAgent.prompt)
    lecture_notes_generator_agent = LectureNotesGeneratorAgent("Lecture Notes Generator Agent", LectureNotesGeneratorAgent.prompt)
    storytelling_agent = StorytellingAgent("Storytelling Agent", StorytellingAgent.prompt)
    editor_agent = EditorAgent("Editor Agent", EditorAgent.prompt)
    pdf_generator_agent = PdfGeneratorAgent()

    chat_history.append(("User", user_input))

    syllabus_requirements = []
    status = "Processing... Please wait."

    if pdf_file:
        pdf_text = extract_pdf_text(pdf_file.name)
        syllabus_requirements = extract_syllabus_requirements(pdf_text)

    article_content = article_retrieval_agent.retrieve_and_validate_articles(user_input)
    cleaned_article_content = article_retrieval_agent.remove_quotes(article_content)
    
    # Format the article content output into JSON and add to chat history
    article_json_output = {
        "status": "success",
        "article_content": cleaned_article_content,
        "tokensused": len(cleaned_article_content.split())
    }
    formatted_article_json = format_json_output(article_json_output)
    chat_history.append(("Bot", f"Article retrieval output:\n{formatted_article_json}"))
    
    status = "Articles retrieved successfully."

    lecture_notes = lecture_notes_generator_agent.get_user_intent(article_content)
    cleaned_lecture_notes = editor_agent.remove_quotes(lecture_notes)
    
    # Format the lecture notes output into JSON and add to chat history
    lecture_notes_json_output = {
        "status": "success",
        "lecture_notes": cleaned_lecture_notes,
        "tokensused": len(cleaned_lecture_notes.split())
    }
    formatted_lecture_notes_json = format_json_output(lecture_notes_json_output)
    chat_history.append(("Bot", f"Lecture notes output:\n{formatted_lecture_notes_json}"))
    
    status = "Lecture notes generated."

    if syllabus_requirements:
        for requirement in syllabus_requirements:
            if requirement.lower() not in cleaned_lecture_notes.lower():
                cleaned_lecture_notes = cleaned_lecture_notes.replace(requirement, "")
        chat_history.append(("Bot", f"Lecture notes after adjusting for syllabus requirements:\n{cleaned_lecture_notes}"))
        status = "Lecture notes adjusted for syllabus requirements."

    storytelling_output = storytelling_agent.get_user_intent(cleaned_lecture_notes)
    cleaned_storytelling_output = editor_agent.remove_quotes(storytelling_output)
    
    # Format the storytelling output into JSON and add to chat history
    storytelling_json_output = {
        "status": "success",
        "storytelling_content": cleaned_storytelling_output,
        "tokensused": len(cleaned_storytelling_output.split())
    }
    formatted_storytelling_json = format_json_output(storytelling_json_output)
    chat_history.append(("Bot", f"Storytelling content output:\n{formatted_storytelling_json}"))
    
    status = "Storytelling content created."

    # Process edited lecture notes
    edited_lecture_notes = editor_agent.edit_content(cleaned_lecture_notes)
    cleaned_edited_lecture_output = editor_agent.remove_quotes(edited_lecture_notes)
    
    # Format edited lecture notes output into JSON and add to chat history
    edited_lecture_notes_json_output = {
        "status": "success",
        "edited_lecture_notes": cleaned_edited_lecture_output,
        "tokensused": len(cleaned_lecture_notes.split())
    }
    formatted_edited_lecture_notes_json = format_json_output(edited_lecture_notes_json_output)
    chat_history.append(("Bot", f"Edited lecture notes output:\n{formatted_edited_lecture_notes_json}"))
    
    status = "Lecture notes edited."

    # Process edited storytelling content
    edited_storytelling_notes = editor_agent.edit_content(cleaned_storytelling_output)
    cleaned_edited_storytelling_output = editor_agent.remove_quotes(edited_storytelling_notes)
    
    # Format edited storytelling content output into JSON and add to chat history
    edited_storytelling_json_output = {
        "status": "success",
        "edited_storytelling_content": cleaned_edited_storytelling_output,
        "tokensused": len(cleaned_storytelling_output.split())
    }
    formatted_edited_storytelling_json = format_json_output(edited_storytelling_json_output)
    chat_history.append(("Bot", f"Edited storytelling content output:\n{formatted_edited_storytelling_json}"))
    
    status = "Storytelling content edited."

    pdf_path = pdf_generator_agent.generate_pdf(edited_lecture_notes, edited_storytelling_notes)
    chat_history.append(("Bot", "PDF generated successfully!"))
    status = "PDF generated successfully."

    # Create the output JSON
    json_output = {
        "status": "success",
        "editedcontent": cleaned_edited_storytelling_output,
        "tokensused": len(cleaned_lecture_notes.split()) + len(cleaned_storytelling_output.split())
    }

    # Format the JSON output for structured display
    formatted_json = format_json_output(json_output)
    chat_history.append(("Bot", f"Final content:\n{formatted_json}"))

    return chat_history, status, pdf_path

def gradio_interface():
    with gr.Blocks() as app:
        gr.Markdown("Curriculum Content Recommender for Professors")

        chatbot = gr.Chatbot()  

        user_input = gr.Textbox(label="Enter topic", placeholder="Ask me anything...")

        status = gr.Label("Status will appear here.")  

        pdf_file = gr.File(label="Upload syllabus PDF (optional)")

        download_link = gr.File(label="Download Generated PDF")

        generate_button = gr.Button("Generate")

        generate_button.click(
            process_request,
            inputs=[user_input, chatbot, pdf_file],
            outputs=[chatbot, status, download_link]  
        )

    return app

if __name__ == "__main__":
    app = gradio_interface()
    app.launch()
