from fpdf import FPDF

class PdfGeneratorAgent():
    
    def __init__(self):
        super().__init__()

    def generate_pdf(self, lecture_notes, narrative):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        pdf.add_page()
        pdf.set_font('Arial', size=16)  

        lecture_notes = self.clean_text(str(lecture_notes))
        narrative = self.clean_text(str(narrative))

        pdf.cell(200, 10, txt="Lecture Notes:", ln=True, align="L")
        pdf.multi_cell(0, 10, txt=lecture_notes)
  
        pdf.ln(10) 

        pdf.cell(200, 10, txt="Narrative Notes:", ln=True, align="L")
        pdf.multi_cell(0, 10, txt=narrative)
    
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
        }
        
        for key, value in replacements.items():
            text = text.replace(key, value)
        
        return ''.join(c for c in text if ord(c) < 256)  

