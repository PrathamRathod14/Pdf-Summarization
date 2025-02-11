import os
import tempfile
import asyncio
from io import BytesIO
from fpdf import FPDF
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from nicegui import ui
from docx import Document

# -------------------- API Setup --------------------
CHATGROQ_API_KEY = "{YOUR_API_KEY}"  # Replace with your ChatGroq API key
model = ChatGroq(api_key=CHATGROQ_API_KEY, model_name="llama-3.3-70b-versatile")

# -------------------- Functions --------------------

async def summarize_text(text):
    """Summarizes the given text using ChatGroq API."""
    try:
        prompt = f"Write a concise summary of the following (Max 1 sentence):\n\n{text}"
        response = await asyncio.to_thread(model.invoke, [HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "An error occurred while summarizing the text."

async def handle_upload(file):
    """Handles the uploaded PDF file and provides feedback to the user."""
    try:
        output_text.set_text("Processing your file... Please wait.")
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, file.name)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(file.content.read())

        # Process PDF and get summary
        summary = await process_pdf(file_path)
        os.remove(file_path)

        # Display summary and generate download buttons
        output_text.set_text(summary)
        show_download_buttons(summary)

    except Exception as e:
        print(f"Error handling upload: {e}")
        output_text.set_text("Error occurred during file upload. Please try again.")

async def process_pdf(file_path):
    """Loads, splits, and summarizes the PDF content asynchronously."""
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()

        if not pages:
            return "Error: No text found in the uploaded PDF."

        # Split PDF content into chunks for summarization
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(pages)

        if not chunks:
            return "Error: PDF could not be split into chunks."

        # Summarize each chunk asynchronously
        summaries = await asyncio.gather(*(summarize_text(chunk.page_content) for chunk in chunks))
        unique_summaries = list(set(filter(None, summaries)))
        return "\n".join(unique_summaries)
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return "An error occurred while processing the PDF."

def generate_word(summary):
    """Generate a Word document from the summary."""
    doc = Document()
    doc.add_paragraph(summary)
    byte_io = BytesIO()
    doc.save(byte_io)
    byte_io.seek(0)
    return byte_io

def generate_pdf(summary):
    """Generate a valid PDF document from the summary."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(190, 10, summary)
    pdf_data = pdf.output(dest='S').encode('latin1')  # Use 'S' to output as string
    byte_io = BytesIO(pdf_data)
    byte_io.seek(0)
    return byte_io

def show_download_buttons(summary):
    """Creates buttons to download the summary in Word and PDF formats."""
    def download_word():
        word_file = generate_word(summary)
        ui.download(word_file.read(), "summary.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    def download_pdf():
        pdf_file = generate_pdf(summary)
        ui.download(pdf_file.read(), "summary.pdf", "application/pdf")

    with ui.row().classes("justify-center mt-4"):
        ui.button("Download as Word", on_click=download_word).classes("mr-2 bg-blue-500 hover:bg-blue-700 text-white")
        ui.button("Download as PDF", on_click=download_pdf).classes("ml-2 bg-green-500 hover:bg-green-700 text-white")

def pdf_dialog_interface():
    """Creates a dialog interface for uploading PDFs and displaying the summary."""
    pdf_dialog = ui.dialog()
    with pdf_dialog, ui.card().classes('rounded-2xl shadow-lg p-8 bg-gray-100'):
        ui.label("Upload a PDF to Summarize").classes(
            "font-size: 24px; font-weight: bold; color: #2D3748; text-align: center;"
        )

        with ui.column().classes("justify-center items-center"):
            ui.upload(on_upload=handle_upload, multiple=False).props('primary').classes("mt-4")

        global output_text
        with ui.card().classes("mt-6 w-full p-4 bg-white rounded-xl shadow"):
            output_text = ui.label("Summary will appear here.").style(
                "font-size: 16px; color: #555; white-space: pre-wrap; overflow-y: auto; max-height: 300px;"
            )

    return pdf_dialog

# -------------------- Main --------------------

# Initialize and display the PDF dialog interface
pdf_dialog_interface()

# Button to open dialog manually for debugging
ui.button("Open PDF Summarizer", on_click=lambda: pdf_dialog_interface().open()).classes("m-4 bg-yellow-500 hover:bg-yellow-700 text-white")

# Run the NiceGUI interface
ui.run()
