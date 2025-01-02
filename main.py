import gradio as gr
from article_retrieval_agent import ArticleRetrievalAgent
from lecture_notes_generator_agent import LectureNotesGeneratorAgent
from storytelling_agent import StorytellingAgent
from editor_agent import EditorAgent
from pdf_generator_agent import PdfGeneratorAgent
from curriculum_content_recommender_agent import CurriculumContentRecommenderAgent
from agent import Agent
from pdfminer.high_level import extract_text
import sqlite3
import json
from auth import register_user, login_user

article_retrieval_agent = ArticleRetrievalAgent("Article Retrieval Agent", ArticleRetrievalAgent.prompt)
lecture_notes_generator_agent = LectureNotesGeneratorAgent("Lecture Notes Generator Agent", LectureNotesGeneratorAgent.prompt)
storytelling_agent = StorytellingAgent("Storytelling Agent", StorytellingAgent.prompt)
editor_agent = EditorAgent("Editor Agent", EditorAgent.prompt)
pdf_generator_agent = PdfGeneratorAgent()
curriculum_content_recommender_agent = CurriculumContentRecommenderAgent("Curriculum Content Recommender", CurriculumContentRecommenderAgent.prompt)
agent = Agent("Agent", "Agent")
formatted_article_json = None
lecture_notes = None
narrative_notes = None
recommendations = None

def create_db():
    conn = sqlite3.connect('chats.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            user_input TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    conn.commit()
    conn.close()

create_db()  # Call this to set up the database when the application starts

# Save chat to the database
def save_chat_to_db(username, user_input, bot_response):
    conn = sqlite3.connect('chats.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO chats (username, user_input, bot_response) VALUES (?, ?, ?)''', (username, user_input, bot_response))
    conn.commit()
    conn.close()

# Get past chats from the database
def get_past_chats(username):
    conn = sqlite3.connect('chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT user_input, bot_response, timestamp FROM chats WHERE username = ? ORDER BY timestamp DESC''', (username,))
    chats = cursor.fetchall()
    conn.close()

    formatted_chats = []
    for chat in chats:
        formatted_chats.append(f"User: {chat[0]}\nBot: {chat[1]}\nTimestamp: {chat[2]}\n{'-'*20}")
    
    return "\n".join(formatted_chats)


def extract_pdf_text(pdf_path):
    text = extract_text(pdf_path)
    return text

def extract_syllabus_requirements(pdf_text):
    prompt = f"Extract syllabus requirements from following text : {pdf_text}"
    requirements = agent.generate_response(prompt)
    return requirements

def format_json_output(json_output):
    return json.dumps(json_output, indent=4)

def decide_agent(user_input):
    prompt = f"""
                Decide which of the following agents should handle the job based on the user input:
                - Article Retrieval Agent
                - Lecture Notes Generator
                - Storytelling Agent
                - Editor Agent
                - PDF Generator Agent
                - Curriculum Content Recommender Agent
                - Other Agent

                User Input: {user_input}

                Guidelines:
                - If the user asks for articles, references, or research material, assign it to the Article Retrieval Agent.
                - If the user asks to generate or summarize lecture notes, assign it to the Lecture Notes Generator.
                - If the user asks to create a story, narrative, or creative content, assign it to the Storytelling Agent.
                - If the user asks for editing, proofreading, or refining text, assign it to the Editor Agent.
                - If the user asks to generate or work with PDFs (such as extracting text or creating a PDF), assign it to the PDF Generator Agent.
                - If the user asks for curriculum-related recommendations (topics, materials, or activities for learning), assign it to the Curriculum Content Recommender Agent.
                - If the request does not match any of the above categories, assign it to the Other Agent.

                Please respond with the name of the agent that should handle the request.
                """
    response = agent.generate_response(prompt)
    return response

def extract_topic_from_query(user_input):
    prompt = f"Extract the main topic from the following user query: '{user_input}'"
    response = agent.generate_response(prompt)
    return response

def article_retrieval(topic):
    article_content = article_retrieval_agent.retrieve_and_validate_articles(topic.strip())
    cleaned_article_content = article_retrieval_agent.remove_quotes(article_content)

    article_json_output = {
        "status": "success",
        "article_content": cleaned_article_content,
        "tokens_used": len(cleaned_article_content.split())
    }
    formatted_article_json = format_json_output(article_json_output)
    
    return formatted_article_json

def generate_lecture_notes(articles, user_input, syllabus_requirements):
    
    lecture_notes = lecture_notes_generator_agent.get_user_intent(articles, user_input)
    updated_lecture_notes = lecture_notes_generator_agent.update_lecture_notes(lecture_notes, syllabus_requirements)
    cleaned_lecture_notes = lecture_notes_generator_agent.remove_quotes(updated_lecture_notes)

    lecture_notes_json_output = {
        "status": "success",
        "notes": cleaned_lecture_notes,
        "tokens_used": len(cleaned_lecture_notes.split())
    }
    formatted_lecture_notes = format_json_output(lecture_notes_json_output)

    return formatted_lecture_notes

def generate_narrative_notes(lecture_notes):
    
    narrative_notes = storytelling_agent.get_user_intent(lecture_notes)
    cleaned_narrative_notes = storytelling_agent.remove_quotes(narrative_notes)
    
    narrative_notes_output = {
        "status": "success",
        "notes": cleaned_narrative_notes,
        "tokens_used": len(cleaned_narrative_notes.split())
    }
    formatted_narrative_notes = format_json_output(narrative_notes_output)
    
    return formatted_narrative_notes

def edit_notes(notes):
    
    edited_notes = editor_agent.edit_content(notes)
    cleaned_edited_notes = editor_agent.remove_quotes(edited_notes)
    
    edited_notes_output = {
        "status": "success",
        "edited_notes": cleaned_edited_notes,
        "tokens_used": len(cleaned_edited_notes.split())
    }
    formatted_edited_notes = format_json_output(edited_notes_output)
    
    return formatted_edited_notes

def recommend(query):
    
    recommendations = curriculum_content_recommender_agent.get_recommendations(query)
    cleaned_recommendations = curriculum_content_recommender_agent.remove_quotes(recommendations)
    
    recommendations_output = {
        "status": "success",
        "notes": cleaned_recommendations,
        "tokens_used": len(cleaned_recommendations.split())
    }
    formatted_recommendations = format_json_output(recommendations_output)
    
    return formatted_recommendations

def process_user_query(user_input, chat_history, pdf_file=None):
    
    global formatted_article_json
    global lecture_notes
    global narrative_notes
    global recommendations
    
    pdf_path = None

    status = "Processing..."  
    
    chat_history.append(("User", user_input))

    syllabus_requirements = []
    if pdf_file:
        pdf_text = extract_pdf_text(pdf_file.name)
        syllabus_requirements = extract_syllabus_requirements(pdf_text)

    agent_response = decide_agent(user_input)

    if "article retrieval agent" in agent_response.lower():
        topic = extract_topic_from_query(user_input)
        formatted_article_json = article_retrieval(topic.strip())
        chat_history.append(("Bot", f"Article retrieval:\n{formatted_article_json}"))
        status = "Articles retrieved successfully."

    elif "lecture notes generator" in agent_response.lower():
        if formatted_article_json is None:
            lecture_notes = generate_lecture_notes(None, user_input, syllabus_requirements)
            chat_history.append(("Bot", f"Lecture Notes:\n{lecture_notes}"))
            status = "Lecture notes generated successfully."
        else:
            lecture_notes = generate_lecture_notes(formatted_article_json, user_input, syllabus_requirements)
            chat_history.append(("Bot", f"Lecture Notes:\n{lecture_notes}"))
            status = "Lecture notes generated successfully."
            
    elif "storytelling agent" in agent_response.lower():
        narrative_notes = generate_narrative_notes(lecture_notes)
        chat_history.append(("Bot", f"Narrative Notes:\n{narrative_notes}"))
        status = "Narrative notes generated successfully."
        
    elif "editor agent" in agent_response.lower():
        if "lecture" in user_input.lower():
            edited_notes = edit_notes(lecture_notes)
            chat_history.append(("Bot", f"Edited Lecture Notes:\n{edited_notes}"))
            status = "Lecture notes edited successfully."
            lecture_notes = edited_notes
        elif "narrative" in user_input.lower():
            edited_notes = edit_notes(narrative_notes)
            chat_history.append(("Bot", f"Edited Narrative Notes:\n{edited_notes}"))
            status = "Narrative notes edited successfully."
            narrative_notes = edited_notes
            
    elif "curriculum content recommender agent" in agent_response.lower():
        recommendations = recommend(user_input)
        chat_history.append(("Bot", f"Recommendations:\n{recommendations}"))
        status = "Recommendations generated successfully"
            
    elif "pdf generator agent" in agent_response.lower():
        try:
            if "lecture" in user_input.lower() and ("storytelling" in user_input.lower() or "narrative" in user_input.lower()):
                if lecture_notes and narrative_notes:  # Ensure both notes are not empty
                    pdf_path = pdf_generator_agent.generate_pdf(lecture_notes, narrative_notes,None)
                    chat_history.append(("Bot", "PDF generated successfully!"))
                    status = "PDF generated successfully."
                else:
                    chat_history.append(("Bot", "Lecture notes or storytelling notes are missing."))
                    status = "Missing notes to generate the PDF."
            elif "lecture" in user_input.lower():
                if lecture_notes:  # Ensure lecture notes are not empty
                    pdf_path = pdf_generator_agent.generate_pdf(lecture_notes, None, None)
                    chat_history.append(("Bot", "PDF generated successfully!"))
                    status = "PDF generated successfully."
                else:
                    chat_history.append(("Bot", "Lecture notes are missing."))
                    status = "Missing lecture notes to generate the PDF."
            elif "storytelling" in user_input.lower() or "narrative" in user_input.lower():
                if narrative_notes:  # Ensure storytelling notes are not empty
                    pdf_path = pdf_generator_agent.generate_pdf(narrative_notes, None, None)
                    chat_history.append(("Bot", "PDF generated successfully!"))
                    status = "PDF generated successfully."
                else:
                    chat_history.append(("Bot", "Storytelling notes are missing."))
                    status = "Missing storytelling notes to generate the PDF."
            elif "recommendations" in user_input.lower():
                pdf_path = pdf_generator_agent.generate_pdf(None, None, recommendations)
                chat_history.append(("Bot", "PDF generated successfully!"))
                status = "PDF generated successfully."
            else:
                chat_history.append(("Bot", "Unrecognized notes type for PDF generation."))
                status = "Unrecognized notes type."
        except Exception as e:
            chat_history.append(("Bot", f"Error generating PDF: {str(e)}"))
            status = f"Error generating PDF: {str(e)}"
            
    elif "other agent" in agent_response.lower():
        response = agent.generate_response(user_input)
        chat_history.append(("Bot", f"{response}"))
        status = "Generated"


    return chat_history, status, pdf_path


sessions = {}

def gradio_interface():
    with gr.Blocks() as app:

        with gr.Row():
            gr.Markdown("Curriculum Content Recommender for Professors")  
            logout_button = gr.Button("Logout", elem_id="logout-button", size="sm", visible=False)  

        with gr.Tab("Login"):
            login_username = gr.Textbox(label="Username", placeholder="Enter your username")
            login_password = gr.Textbox(label="Password", type="password", placeholder="Enter your password")
            login_status = gr.Label()
            login_button = gr.Button("Login")

        with gr.Tab("Register"):
            register_username = gr.Textbox(label="Username", placeholder="Enter your username")
            register_password = gr.Textbox(label="Password", type="password", placeholder="Enter your password")
            register_status = gr.Label()
            register_button = gr.Button("Register")
            
        chatbot_tab = gr.Tab("Chatbot", visible=False)

        with chatbot_tab:
            chatbot = gr.Chatbot()
            user_input = gr.Textbox(label="Enter query", placeholder="Ask me anything...")
            pdf_file = gr.File(label="Upload syllabus PDF (optional)")
            status = gr.Label("Status will appear here.")
            download_link = gr.File(label="Download Generated PDF")  # For file download link
            generate_button = gr.Button("Generate")
            
        with gr.Row():
            view_past_chats_button = gr.Button("View Past Chats")
            past_chats_output = gr.Textbox(label="Your Past Chats", interactive=False)
            
        

        def login_action(username, password):
            if login_user(username, password):
                sessions[username] = True
                return f"Login successful! Welcome, {username}.", gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)  # Show chatbot and logout button
            return "Invalid username or password.", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

        def register_action(username, password):
            return register_user(username, password)

        def logout_action(username):
            if username in sessions:
                del sessions[username]
            return gr.update(visible=False), gr.update("Logged out successfully. Please log in again."), gr.update(visible=False), gr.update(visible=True)

        def process_with_auth(user_input, chat_history, pdf_file, username):
            if username in sessions and sessions[username]:
                chat_history, status, pdf_name = process_user_query(user_input, chat_history, pdf_file)
                
                # Save the conversation to the database
                if chat_history:
                    user_input_text = chat_history[-1][1]  # User input
                    bot_response_text = chat_history[-1][0]  # Last bot response
                    save_chat_to_db(username, user_input_text, bot_response_text)

                return chat_history, status, gr.update(value=pdf_name, visible=True)  # Update download link with PDF path
            return [], "Unauthorized: Please log in first.", gr.update(visible=False)

        login_button.click(
            login_action,
            inputs=[login_username, login_password],
            outputs=[login_status, chatbot_tab, logout_button, login_button]  
        )

        register_button.click(
            register_action,
            inputs=[register_username, register_password],
            outputs=register_status
        )

        logout_button.click(
            logout_action,
            inputs=[login_username],
            outputs=[chatbot_tab, login_status, logout_button, login_button] 
        )

        generate_button.click(
            process_with_auth,
            inputs=[user_input, chatbot, pdf_file, login_username],
            outputs=[chatbot, status, download_link]  
        )
        
        view_past_chats_button.click(
            lambda username: get_past_chats(username),
            inputs=[login_username],
            outputs=[past_chats_output]
        )

    return app


if __name__ == "__main__":
    app = gradio_interface()
    app.launch()
