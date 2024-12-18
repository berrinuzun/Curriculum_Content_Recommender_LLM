from fpdf import FPDF
import json

class PdfGeneratorAgent():
    
    def __init__(self):
        super().__init__()

    def generate_pdf(self, lecture_notes, narrative):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        pdf.add_page()
        pdf.set_font('Arial', size=16)  

        lecture_notes_text = self.extract_attribute(lecture_notes, "edited_content") 
        lecture_notes_cleaned = self.clean_text(lecture_notes_text)
 
        narrative_text = self.extract_attribute(narrative, "edited_content")  
        narrative_cleaned = self.clean_text(narrative_text)

        pdf.cell(200, 10, txt="Lecture Notes:", ln=True, align="L")
        pdf.multi_cell(0, 10, txt=lecture_notes_cleaned)
  
        pdf.ln(10) 

        pdf.cell(200, 10, txt="Narrative Notes:", ln=True, align="L")
        pdf.multi_cell(0, 10, txt=narrative_cleaned)
    
        pdf_output = "generated_pdf_output.pdf"
        pdf.output(pdf_output)

        return pdf_output

    def clean_text(self, text):
        replacements = {
            '—': '-', 
            '–': '-',  
            '“': '"',  
            '”': '"',  
            '‘': "'",  
            '’': "'",  
            '•': '*',  
            '…': '...', 
            '*': '',
            '#': '', 
        }
        
        for key, value in replacements.items():
            text = text.replace(key, value)
        
        return ''.join(c for c in text if ord(c) < 256)  

    def extract_attribute(self, json_data, attribute_name):
        
        if isinstance(json_data, str):
            json_data = json.loads(json_data)  
        
        return json_data.get(attribute_name, "Attribute not found")
