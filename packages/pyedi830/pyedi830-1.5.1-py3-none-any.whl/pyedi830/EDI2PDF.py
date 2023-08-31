from weasyprint import HTML
import sys
from .debug import Debug
from .EDI2HTML import EDI2HTML
from io import StringIO, BytesIO

class EDI2PDF(EDI2HTML):
    def __init__(self, template_file_path='830_Forecast.html', use_debug=False):
        super().__init__(template_file_path=template_file_path, use_debug=use_debug)

    def to_pdf(self, edi_file_path, pdf_file_path, temp_html_file_path):
        self.to_html(edi_file_path, temp_html_file_path)
        self.html_to_pdf(temp_html_file_path, pdf_file_path)

    def html_to_pdf(self, html_file_path, pdf_file_path):
        Debug.log_message(f"Rendering html to pdf...")

        # Increase to 2000 to solve the big file rendering problem.
        sys.setrecursionlimit(2000)
        
        html_handler = None
        if isinstance(html_file_path, StringIO):
            html_handler = HTML(string=html_file_path.getvalue())
        else:
            html_handler = HTML(html_file_path)
        
        html_handler.write_pdf(pdf_file_path)

        if isinstance(pdf_file_path, BytesIO):
            Debug.log_message(f"Done to render pdf into BytesIO")
        else:
            Debug.log_message(f"Done to render pdf into {pdf_file_path}")        
        
        return pdf_file_path