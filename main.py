import gradio as gr
from article_retrieval_agent import ArticleRetrievalAgent
from lecture_notes_generator_agent import LectureNotesGeneratorAgent
from storytelling_agent import StorytellingAgent
from editor_agent import EditorAgent
from pdf_generator_agent import PdfGeneratorAgent
from pdfminer.high_level import extract_text
import re

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

def process_request(user_input, chat_history, pdf_file=None):
   
    article_retrieval_agent = ArticleRetrievalAgent("Article Retrieval Agent", ArticleRetrievalAgent.prompt)
    lecture_notes_generator_agent = LectureNotesGeneratorAgent("Lecture Notes Generator Agent", LectureNotesGeneratorAgent.prompt)
    storytelling_agent = StorytellingAgent("Storytelling Agent", StorytellingAgent.prompt)
    editor_agent = EditorAgent("Editor Agent", EditorAgent.prompt)
    pdf_generator_agent = PdfGeneratorAgent()

    chat_history.append(("User", user_input))  

    syllabus_requirements = []
    if pdf_file:
        pdf_text = extract_pdf_text(pdf_file.name) 
        syllabus_requirements = extract_syllabus_requirements(pdf_text)  

    article_content = article_retrieval_agent.retrieve_and_validate_articles(user_input)
    chat_history.append(("Bot", f"I found relevant articles based on your input:\n{article_content}"))

    lecture_notes = lecture_notes_generator_agent.get_user_intent(article_content)
    chat_history.append(("Bot", f"Lecture notes have been generated:\n{lecture_notes}"))

    if syllabus_requirements:
        for requirement in syllabus_requirements:
            if requirement.lower() not in lecture_notes.lower():
                lecture_notes = lecture_notes.replace(requirement, "")
        chat_history.append(("Bot", f"Lecture notes after adjusting for syllabus requirements:\n{lecture_notes}"))

    storytelling_output = storytelling_agent.get_user_intent(lecture_notes)
    chat_history.append(("Bot", f"The storytelling content has been created:\n{storytelling_output}"))

    edited_lecture_notes = editor_agent.edit_content(lecture_notes) 
    chat_history.append(("Bot", f"Lecture notes have been edited:\n{edited_lecture_notes}"))

    edited_storytelling_notes = editor_agent.edit_content(storytelling_output) 
    chat_history.append(("Bot", f"Storytelling content has been edited:\n{edited_storytelling_notes}"))

    pdf_path = pdf_generator_agent.generate_pdf(edited_lecture_notes, edited_storytelling_notes)
    chat_history.append(("Bot", "PDF generated successfully!"))

    return chat_history, pdf_path


def gradio_interface():
    with gr.Blocks() as app:
        gr.Markdown("## Multi-Agent Content Generator Chatbot")

        chatbot = gr.Chatbot()

        user_input = gr.Textbox(label="Enter your query")

        status = gr.Label("Status will appear here.")

        pdf_file = gr.File(label="Upload syllabus PDF (optional)")

        download_link = gr.File(label="Download Generated PDF")

        generate_button = gr.Button("Generate")

        generate_button.click(
            process_request,
            inputs=[user_input, chatbot, pdf_file],
            outputs=[chatbot, download_link]
        )

    return app

if __name__ == "__main__":
    app = gradio_interface()
    app.launch()
