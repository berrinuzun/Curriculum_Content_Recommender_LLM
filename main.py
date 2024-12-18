import gradio as gr
from article_retrieval_agent import ArticleRetrievalAgent
from lecture_notes_generator_agent import LectureNotesGeneratorAgent
from storytelling_agent import StorytellingAgent
from editor_agent import EditorAgent
from pdf_generator_agent import PdfGeneratorAgent

def process_request(user_input):
    article_retrieval_agent = ArticleRetrievalAgent("Article Retrieval Agent", ArticleRetrievalAgent.prompt)
    lecture_notes_generator_agent = LectureNotesGeneratorAgent("Lecture Notes Generator Agent", LectureNotesGeneratorAgent.prompt)
    storytelling_agent = StorytellingAgent("Storytelling Agent", StorytellingAgent.prompt)
    editor_agent = EditorAgent("Editor Agent", EditorAgent.prompt)
    pdf_generator_agent = PdfGeneratorAgent()

    article_content = article_retrieval_agent.retrieve_and_validate_articles(user_input)
    
    print(article_content)

    lecture_notes = lecture_notes_generator_agent.get_user_intent(article_content)
    
    print(lecture_notes)

    storytelling_output = storytelling_agent.get_user_intent(lecture_notes)
    
    print(storytelling_output)

    edited_lecture_notes = editor_agent.edit_content(lecture_notes)
    
    print(edited_lecture_notes)
    
    edited_storytelling_notes = editor_agent.edit_content(storytelling_output)
    
    print(edited_storytelling_notes)
    
    # Combine both sections with appropriate formatting
    content = f"Lecture Notes:\n\n{edited_lecture_notes}\n\n{'-'*50}\n\nNarrative Notes:\n\n{edited_storytelling_notes}"

    # PDF Generation
    pdf_path = pdf_generator_agent.generate_pdf(edited_lecture_notes, edited_storytelling_notes)

    # Return status and the generated PDF link
    status = "PDF generated successfully!"
    return status, pdf_path


def gradio_interface():
    with gr.Blocks() as app:
        gr.Markdown("## Multi-Agent Content Generator")
        user_input = gr.Textbox(label="Enter your prompt")
        generate_button = gr.Button("Generate")
        status = gr.Label("Status will appear here.")
        download_link = gr.File(label="Download Generated PDF")  # Doğrudan dosya yolunu gösterecek

        generate_button.click(
            process_request,
            inputs=[user_input],
            outputs=[status, download_link]
        )
    return app

if __name__ == "__main__":
    app = gradio_interface()
    app.launch()
