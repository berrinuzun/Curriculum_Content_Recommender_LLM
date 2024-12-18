from fpdf import FPDF
import json

class PdfGeneratorAgent():
    
    def __init__(self):
        super().__init__()
        
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