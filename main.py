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
    
    # Initialize agents
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
    chat_history.append(("Bot", f"I found relevant articles based on your input:\n{cleaned_article_content}"))
    status = "Articles retrieved successfully."

    lecture_notes = lecture_notes_generator_agent.get_user_intent(article_content)
    cleaned_lecture_notes = editor_agent.remove_quotes(lecture_notes)
    chat_history.append(("Bot", f"Lecture notes have been generated:\n{cleaned_lecture_notes}"))
    status = "Lecture notes generated."

    if syllabus_requirements:
        for requirement in syllabus_requirements:
            if requirement.lower() not in cleaned_lecture_notes.lower():
                cleaned_lecture_notes = cleaned_lecture_notes.replace(requirement, "")
        chat_history.append(("Bot", f"Lecture notes after adjusting for syllabus requirements:\n{cleaned_lecture_notes}"))
        status = "Lecture notes adjusted for syllabus requirements."

    storytelling_output = storytelling_agent.get_user_intent(cleaned_lecture_notes)
    cleaned_storytelling_output = editor_agent.remove_quotes(storytelling_output)
    chat_history.append(("Bot", f"The storytelling content has been created:\n{cleaned_storytelling_output}"))
    status = "Storytelling content created."

    edited_lecture_notes = editor_agent.edit_content(cleaned_lecture_notes)
    chat_history.append(("Bot", f"Lecture notes have been edited:\n{edited_lecture_notes}"))
    status = "Lecture notes edited."

    edited_storytelling_notes = editor_agent.edit_content(cleaned_storytelling_output)
    chat_history.append(("Bot", f"Storytelling content has been edited:\n{edited_storytelling_notes}"))
    status = "Storytelling content edited."

    pdf_path = pdf_generator_agent.generate_pdf(edited_lecture_notes, edited_storytelling_notes)
    chat_history.append(("Bot", "PDF generated successfully!"))
    status = "PDF generated successfully."

    return chat_history, status, pdf_path

def gradio_interface():
    with gr.Blocks() as app:
        gr.Markdown("## Multi-Agent Content Generator Chatbot")

        chatbot = gr.Chatbot()  

        user_input = gr.Textbox(label="Enter your query", placeholder="Ask me anything...")

        status = gr.Label("Status will appear here.")  # Label to show status

        pdf_file = gr.File(label="Upload syllabus PDF (optional)")

        download_link = gr.File(label="Download Generated PDF")

        generate_button = gr.Button("Generate")

        generate_button.click(
            process_request,
            inputs=[user_input, chatbot, pdf_file],
            outputs=[chatbot, status, download_link]  # Output the status as well
        )

    return app

if __name__ == "__main__":
    app = gradio_interface()
    app.launch()
