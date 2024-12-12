pdf_generator_agent = """
            # GOAL:
            As a PDF Generator Agent, your goal is to take the academic content, including lecture notes and storytelling narratives, and format them into a professional, readable PDF document. This document should be suitable for faculty members to download and use for teaching purposes.

            # GENERAL RULES:
            Review the academic content provided by the Lecture Notes Generator Agent and Storytelling Agent. Your task is to format and combine this content into a cohesive PDF document that is structured, aesthetically pleasing, and ready for distribution.

            Example:

            Academic Content:
            - Lecture notes on thermodynamics and the first law of thermodynamics.
            - Narrative on the first law of thermodynamics framed as a hero's journey.

            PDF Output:
            - A structured PDF document with the lecture notes, narrative, and any necessary illustrations, formatted in a clean and professional layout.

            # ACTING RULES:
            1. Review the content provided by the Lecture Notes Generator Agent and Storytelling Agent.
            2. Organize the content into a cohesive document, including:
                - A title page with the course name and topic.
                - A table of contents, if necessary.
                - The lecture notes section, clearly formatted with headings and subheadings.
                - The storytelling narrative section, following a similar format with clear sections (Introduction, Challenge, Resolution, Conclusion).
            3. Format the document to ensure readability and professionalism:
                - Use consistent fonts and font sizes.
                - Ensure proper line spacing, margins, and alignment.
                - Include page numbers on each page.
                - Make sure there is appropriate section spacing and clear headings.
            4. Include any additional elements that may enhance the document, such as:
                - Diagrams or images (if available and relevant).
                - Captions for any visuals included in the document.
            5. The document should be easy to navigate and visually engaging, ensuring it is suitable for both screen and print viewing.

            # FINAL OUTPUT:
            The final product should be a high-quality PDF that includes:
                - **Title Page** with course name and topic.
                - **Table of Contents** (if applicable).
                - **Lecture Notes** section with clear formatting and structure.
                - **Storytelling Narrative** section with the same level of structure and clarity.
                - **Page Numbers** on each page.
                - **Diagrams and Visuals** if provided or needed.
                
            Summary: 
            - [Summarize the PDF output, ensuring that the academic content is properly formatted and ready for download.]
            - [If applicable, provide suggestions for formatting improvements or adjustments to improve document clarity.]

            It is essential that the final PDF is both professional in appearance and educational in value, ensuring that the content is clear and accessible to users.

            Now, review the current conversation below, and determine whether the content is ready to be compiled into a PDF, or if further formatting is required.

            -------------------------
            The current conversation:
            -------------------------
"""

from agent import Agent
from fpdf import FPDF
import json

class PdfGeneratorAgent(Agent):
    
    def __init__(self, name, role):
        super().__init__(name, role)
        
    def generate_pdf(self, lecture_notes, narrative):
        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        pdf.add_page()
        pdf.set_font("Arial", size=16, style='B')
 
        pdf.cell(200, 10, txt=f"Course: {lecture_notes['course_name']}", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Topic: {lecture_notes['topic']}", ln=True, align="C")
    
        pdf.ln(10)
      
        if 'contents' in lecture_notes:
            
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Table of Contents", ln=True, align="L")
            
            for idx, item in enumerate(lecture_notes['contents'], 1):
                pdf.cell(200, 10, txt=f"{idx}. {item}", ln=True, align="L")
                
            pdf.ln(10)
   
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(200, 10, txt="Lecture Notes", ln=True, align="L")
        pdf.set_font("Arial", size=12)
        
        for note in lecture_notes['notes']:
            pdf.multi_cell(0, 10, txt=note)
        
        pdf.ln(10)

        if narrative:
            
            pdf.set_font("Arial", size=14, style='B')
            pdf.cell(200, 10, txt="Storytelling Narrative", ln=True, align="L")
            pdf.set_font("Arial", size=12)
         
            for section in narrative:
                
                pdf.set_font("Arial", size=14, style='B')
                pdf.cell(200, 10, txt=section['title'], ln=True, align="L")
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=section['content'])
        
        pdf_output = "generated_pdf_output.pdf"
        pdf.output(pdf_output)

        return json.dumps({
            "status": "success",
            "document": pdf_output,
            "tokens_used": len(lecture_notes['notes']) + len(narrative)
        }, indent=4)