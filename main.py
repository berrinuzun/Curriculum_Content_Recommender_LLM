import gradio as gr
from article_retrieval_agent import ArticleRetrievalAgent
from lecture_notes_generator_agent import LectureNotesGeneratorAgent
from storytelling_agent import StorytellingAgent
from editor_agent import EditorAgent
from pdf_generator_agent import PdfGeneratorAgent

def process_request(user_input, chat_history):
    article_retrieval_agent = ArticleRetrievalAgent("Article Retrieval Agent", ArticleRetrievalAgent.prompt)
    lecture_notes_generator_agent = LectureNotesGeneratorAgent("Lecture Notes Generator Agent", LectureNotesGeneratorAgent.prompt)
    storytelling_agent = StorytellingAgent("Storytelling Agent", StorytellingAgent.prompt)
    editor_agent = EditorAgent("Editor Agent", EditorAgent.prompt)
    pdf_generator_agent = PdfGeneratorAgent()

    article_content = article_retrieval_agent.retrieve_and_validate_articles(user_input)

    lecture_notes = lecture_notes_generator_agent.get_user_intent(article_content)

    storytelling_output = storytelling_agent.get_user_intent(lecture_notes)

    edited_lecture_notes = editor_agent.edit_content(lecture_notes)
    
    edited_storytelling_notes = editor_agent.edit_content(storytelling_output)

    pdf_path = pdf_generator_agent.generate_pdf(edited_lecture_notes, edited_storytelling_notes)

    status = "PDF generated successfully!"
    
    # Adding chat history to include the user input and agent response
    chat_history.append(("User", user_input))
    chat_history.append(("Bot", status))

    return chat_history, pdf_path

def gradio_interface():
    with gr.Blocks() as app:
        gr.Markdown("## Multi-Agent Content Generator Chatbot")
        
        # Chat interface for conversation
        chatbot = gr.Chatbot()
        
        # Input for user query
        user_input = gr.Textbox(label="Enter your query")
        
        # Status label
        status = gr.Label("Status will appear here.")
        
        # PDF download link
        download_link = gr.File(label="Download Generated PDF")
        
        # Button for generating responses
        generate_button = gr.Button("Generate")
        
        # Connecting the button click with processing
        generate_button.click(
            process_request,
            inputs=[user_input, chatbot],
            outputs=[chatbot, download_link]
        )

    return app

if __name__ == "__main__":
    app = gradio_interface()
    app.launch()
