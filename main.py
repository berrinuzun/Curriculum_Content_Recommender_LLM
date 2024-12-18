import gradio as gr
from article_retrieval_agent import ArticleRetrievalAgent
from lecture_notes_generator_agent import LectureNotesGeneratorAgent
from storytelling_agent import StorytellingAgent
from editor_agent import EditorAgent
from pdf_generator_agent import PdfGeneratorAgent

def process_request(user_input, chat_history):
    # Ajanları başlatıyoruz
    article_retrieval_agent = ArticleRetrievalAgent("Article Retrieval Agent", ArticleRetrievalAgent.prompt)
    lecture_notes_generator_agent = LectureNotesGeneratorAgent("Lecture Notes Generator Agent", LectureNotesGeneratorAgent.prompt)
    storytelling_agent = StorytellingAgent("Storytelling Agent", StorytellingAgent.prompt)
    editor_agent = EditorAgent("Editor Agent", EditorAgent.prompt)
    pdf_generator_agent = PdfGeneratorAgent()

    # Kullanıcının isteğine göre işlemleri başlatıyoruz
    chat_history.append(("User", user_input))  # Kullanıcı girdisi ekleniyor

    # Makale alma ve doğrulama
    article_content = article_retrieval_agent.retrieve_and_validate_articles(user_input)
    chat_history.append(("Bot", f"I found relevant articles based on your input:\n{article_content}"))  # Makale içeriği ekleniyor

    # Ders notları oluşturuluyor
    lecture_notes = lecture_notes_generator_agent.get_user_intent(article_content)
    chat_history.append(("Bot", f"Lecture notes have been generated:\n{lecture_notes}"))  # Ders notları ekleniyor

    # Storytelling (Hikaye anlatımı) oluşturuluyor
    storytelling_output = storytelling_agent.get_user_intent(lecture_notes)
    chat_history.append(("Bot", f"The storytelling content has been created:\n{storytelling_output}"))  # Hikaye anlatımı ekleniyor

    # İçerik düzenleniyor
    edited_lecture_notes = editor_agent.edit_content(lecture_notes)
    chat_history.append(("Bot", f"Lecture notes have been edited:\n{edited_lecture_notes}"))  # Düzenlenmiş ders notları ekleniyor
    
    edited_storytelling_notes = editor_agent.edit_content(storytelling_output)
    chat_history.append(("Bot", f"Storytelling content has been edited:\n{edited_storytelling_notes}"))  # Düzenlenmiş hikaye anlatımı ekleniyor

    # PDF oluşturuluyor
    pdf_path = pdf_generator_agent.generate_pdf(edited_lecture_notes, edited_storytelling_notes)
    chat_history.append(("Bot", "PDF generated successfully!"))  # PDF oluşturuluyor

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
