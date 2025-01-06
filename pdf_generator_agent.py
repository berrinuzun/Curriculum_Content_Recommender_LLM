from fpdf import FPDF
import json

class PdfGeneratorAgent():

    def __init__(self):
        super().__init__()

    def generate_pdf(self, lecture_notes=None, narrative=None, recommendations=None):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.add_page()
        pdf.set_font('Arial', size=16)

        # Lecture Notes
        if lecture_notes:
            lecture_notes_text = self.extract_attribute(lecture_notes, "notes")
            lecture_notes_cleaned = self.clean_text(lecture_notes_text)
            pdf.cell(200, 10, txt="Lecture Notes:", ln=True, align="L")
            pdf.multi_cell(0, 10, txt=lecture_notes_cleaned)
            pdf.ln(10)

        # Narrative Notes
        if narrative:
            narrative_text = self.extract_attribute(narrative, "notes")
            narrative_cleaned = self.clean_text(narrative_text)
            pdf.cell(200, 10, txt="Narrative Notes:", ln=True, align="L")
            pdf.multi_cell(0, 10, txt=narrative_cleaned)
            pdf.ln(10)

        # Recommendations
        if recommendations:
            recommendations_text = self.extract_attribute(recommendations, "recommendations")
            recommendations_cleaned = self.clean_text(recommendations_text)
            pdf.cell(200, 10, txt="Recommendations:", ln=True, align="L")
            pdf.multi_cell(0, 10, txt=recommendations_cleaned)
            pdf.ln(10)

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

        text = ''.join(c for c in text if ord(c) < 256)
        text = text.replace('\n', '\n')  # Ensures that \n in string is treated as a newline

        return text

    def extract_attribute(self, json_data, attribute_name):
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        return json_data.get(attribute_name, "Attribute not found")
