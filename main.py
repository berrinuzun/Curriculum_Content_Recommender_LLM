import gradio as gr
from article_retrieval_agent import ArticleRetrievalAgent
from lecture_notes_generator_agent import LectureNotesGeneratorAgent
from storytelling_agent import StorytellingAgent
from editor_agent import EditorAgent
from pdf_generator_agent import PdfGeneratorAgent
import json


def process_request(topic):
    try:

        article_agent = ArticleRetrievalAgent("Article", "Article retrieval specialist")
        notes_agent = LectureNotesGeneratorAgent("Notes", "Notes generation specialist")
        story_agent = StorytellingAgent("Story", "Storytelling specialist")
        editor_agent = EditorAgent("Editor", "Academic editor")
        pdf_agent = PdfGeneratorAgent("PDF", "PDF generation specialist")


        with gr.Progress() as progress:
            progress(0, desc="Retrieving articles...")
            articles = article_agent.get_user_intent(topic)

            progress(0.25, desc="Generating notes...")
            notes = notes_agent.get_user_intent(articles)

            progress(0.5, desc="Creating story...")
            story = story_agent.get_user_intent(notes)

            progress(0.75, desc="Editing content...")
            edited_content = editor_agent.edit_content(story)

            progress(0.9, desc="Generating PDF...")
            pdf_output = pdf_agent.generate_pdf(json.loads(notes), json.loads(story))

        return {
            "content": edited_content["edited_content"],
            "pdf": json.loads(pdf_output)["document"]
        }

    except Exception as e:
        return gr.Error(f"An error occurred: {str(e)}")



with gr.Blocks(theme=gr.themes.Soft()) as iface:
    gr.Markdown("# AI Teaching Assistant")

    with gr.Row():
        topic_input = gr.Textbox(
            label="Enter Topic",
            placeholder="Enter the topic you want to teach..."
        )

    with gr.Row():
        submit_btn = gr.Button("Generate Content", variant="primary")

    with gr.Row():
        output_text = gr.Textbox(
            label="Generated Content",
            interactive=False
        )
        output_file = gr.File(
            label="Download PDF"
        )


    submit_btn.click(
        fn=process_request,
        inputs=[topic_input],
        outputs=[output_text, output_file]
    )

if __name__ == "__main__":
    iface.launch(share=True)
