
# PDF Summarization 

The application allows users to upload PDF files, process their contents, generate a concise summary using the ChatGroq API, and download the summary in Word or PDF format. It uses NiceGUI for the web interface and integrates various Python libraries for handling the PDFs and generating the documents.

## Features
- Upload a PDF and summarize its contents.
- Use the ChatGroq API to generate a concise summary.
- Display the summary in a user-friendly interface.
- Download the summary in either Word (`.docx`) or PDF format.

## Technologies Used
- **Python**: The main programming language.
- **NiceGUI**: A web UI library for creating the interface.
- **ChatGroq API**: A powerful AI model for generating text summaries.
- **PyPDF2**: For reading and processing PDF files.
- **fpdf**: For generating PDF files.
- **docx**: For generating Word files.
- **asyncio**: For asynchronous processing of large PDF files.
- **langchain**: For text splitting and document loading.

---

## Installation

To run this application locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/PrathamRathod14/Pdf-Summarization.git
    cd Pdf-Summarization
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:

    Install the following libraries using `pip`:

    ```bash
    pip install nicegui fpdf PyPDF2 langchain langchain_groq docx asyncio
    ```

4. **Set up your ChatGroq API key**:
    - Obtain a ChatGroq API key by signing up at [ChatGroq](https://www.chatgroq.com).
    - Replace the placeholder in the script with your API key:
    ```python
    CHATGROQ_API_KEY = "your-api-key-here"
    ```

5. **Run the application**:
    ```bash
    python app.py
    ```

6. **Access the application**:
    - Open your browser and go to `http://localhost:8080` to use the application.

---

## Usage

- Click the "Open PDF Summarizer" button to upload a PDF file.
- The file will be processed and summarized using the ChatGroq API.
- Once the summary is generated, you can download the result in either Word (`.docx`) or PDF format by clicking the respective download buttons.

## API Details
- The application uses **ChatGroq's AI model** to generate summaries of the uploaded PDF files.
- A prompt is sent to the model for each chunk of text, requesting a concise summary.


### Steps for contributing:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Commit the changes: `git commit -am 'Add new feature'`.
5. Push to the branch: `git push origin feature-name`.
6. Submit a pull request with a description of the changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
