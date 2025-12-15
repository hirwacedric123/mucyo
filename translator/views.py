"""
Student Translator MVP - Django Views
A web app that translates student documents from English to Kinyarwanda, French, Swahili, or Arabic using OpenAI GPT-4o.
"""

import os
from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.utils.text import get_valid_filename
from openai import OpenAI
import PyPDF2
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Supported languages
LANGUAGES = {
    'english': 'English',
    'french': 'French',
    'arabic': 'Arabic',
    'swahili': 'Swahili',
    'kinyarwanda': 'Kinyarwanda'
}

# Initialize OpenAI client
# Get API key from settings (which loads from .env)
OPENAI_API_KEY = getattr(settings, 'OPENAI_API_KEY', '') or os.environ.get('OPENAI_API_KEY', '')
print(f"DEBUG: OpenAI API Key found: {'Yes' if OPENAI_API_KEY else 'No'}")
print(f"DEBUG: API Key length: {len(OPENAI_API_KEY) if OPENAI_API_KEY else 0}")

client = None
if OPENAI_API_KEY:
    try:
        # Initialize OpenAI client with API key
        # Updated to work with OpenAI library v2.x
        client = OpenAI(api_key=OPENAI_API_KEY)
        print("DEBUG: OpenAI client initialized successfully")
    except Exception as e:
        print(f"Warning: OpenAI client initialization failed: {e}")
        import traceback
        print(traceback.format_exc())
        client = None
else:
    print("Warning: OPENAI_API_KEY is not set. Please add it to your .env file.")


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    """Extract text content from a PDF file."""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_docx(file_path):
    """Extract text content from a DOCX file."""
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")


def detect_language(text):
    """Detect the language of the given text using OpenAI."""
    if not client:
        raise Exception("OpenAI client not initialized")
        
    prompt = f"""Detect the language of the following text. Respond with only one word from these options: English, French, Arabic, Swahili, Kinyarwanda.

Text: {text[:500]}..."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a language detection expert. Respond with only the language name."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=10
        )
        
        detected_language = response.choices[0].message.content.strip().lower()
        return detected_language
    except Exception as e:
        raise Exception(f"Error detecting language: {str(e)}")


def translate_text(text, source_language, target_language):
    """Translate text using OpenAI model."""
    if not client:
        raise Exception("OpenAI client not initialized")
        
    if not text or not text.strip():
        raise Exception("No text to translate")
    
    # Create the translation prompt
    prompt = f"""You are a professional translator for educational documents.

Translate the following text from {source_language} to {target_language}.
- Keep the meaning exact and accurate with high precision.
- Use clear and natural language suitable for students.
- Maintain any academic or technical terms as precisely as possible.
- Preserve formatting and structure.
- Do not add explanations, only output the translated text.

Text to translate:
{text}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional translator specializing in educational documents with high accuracy."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=4000
        )
        
        translated_text = response.choices[0].message.content.strip()
        return translated_text
    except Exception as e:
        raise Exception(f"Error during translation: {str(e)}")


def create_pdf_file(text, output_path):
    """Create a PDF file with the translated text."""
    try:
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add the translated text
        paragraphs = text.split('\n')
        for para_text in paragraphs:
            if para_text.strip():
                p = Paragraph(para_text, styles['Normal'])
                story.append(p)
                story.append(Spacer(1, 0.2*inch))
        
        doc.build(story)
    except Exception as e:
        raise Exception(f"Error creating PDF file: {str(e)}")


@require_http_methods(["GET"])
def index(request):
    """Render the main upload form page."""
    try:
        return render(request, 'translator/index.html', {'languages': LANGUAGES})
    except Exception as e:
        # Log the error for debugging
        import traceback
        print(f"Error rendering index template: {e}")
        print(traceback.format_exc())
        # Re-raise to see the actual error in DEBUG mode
        raise


@require_http_methods(["POST"])
def translate(request):
    """Handle file upload, translation, and return the translated document."""
    
    # Debug: Log form data
    print(f"DEBUG: POST data: {request.POST}")
    print(f"DEBUG: FILES data: {request.FILES}")
    
    # Check if file was uploaded
    if 'file' not in request.FILES:
        messages.error(request, 'No file selected. Please upload a document.')
        return redirect('translator:index')
    
    file = request.FILES['file']
    source_language = request.POST.get('source_language', '').lower()
    target_language = request.POST.get('target_language', '').lower()
    
    # Validate file
    if file.name == '':
        messages.error(request, 'No file selected. Please choose a file to upload.')
        return redirect('translator:index')
    
    if not allowed_file(file.name):
        messages.error(request, 'Invalid file type. Please upload a PDF or DOCX file.')
        return redirect('translator:index')
    
    # Validate language selections
    if source_language not in LANGUAGES:
        messages.error(request, 'Invalid source language selected.')
        return redirect('translator:index')
        
    if target_language not in LANGUAGES:
        messages.error(request, 'Invalid target language selected.')
        return redirect('translator:index')
        
    if source_language == target_language:
        messages.error(request, 'Source and target languages cannot be the same.')
        return redirect('translator:index')
    
    # Create uploads directory if it doesn't exist
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(settings.TRANSLATIONS_FOLDER, exist_ok=True)
    
    file_path = None
    try:
        # Save uploaded file - sanitize filename for security
        original_filename = file.name
        safe_filename = get_valid_filename(original_filename)
        file_path = os.path.join(settings.UPLOAD_FOLDER, safe_filename)
        
        # Ensure the path is within UPLOAD_FOLDER (prevent directory traversal)
        file_path = os.path.abspath(file_path)
        upload_folder = os.path.abspath(settings.UPLOAD_FOLDER)
        if not file_path.startswith(upload_folder):
            raise Exception("Invalid file path detected.")
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Extract text based on file type
        file_ext = safe_filename.rsplit('.', 1)[1].lower()
        if file_ext == 'pdf':
            extracted_text = extract_text_from_pdf(file_path)
        elif file_ext == 'docx':
            extracted_text = extract_text_from_docx(file_path)
        else:
            raise Exception("Unsupported file type")
        
        # Check if text was extracted
        if not extracted_text or not extracted_text.strip():
            raise Exception("No text could be extracted from the document. The file may be empty or corrupted.")
        
        # Check if OpenAI client is initialized
        if not client:
            raise Exception("OpenAI API key is not configured. Please set OPENAI_API_KEY in your .env file or environment variables.")
        
        # Detect document language and validate
        detected_language = detect_language(extracted_text)
        source_lang_name = LANGUAGES[source_language]
        
        if detected_language != source_language and not detected_language.startswith(source_language[:3]):
            raise Exception(f"Document language mismatch. Expected {source_lang_name}, but detected {detected_language.title()}. Please select the correct source language.")
        
        # Translate the text
        source_lang_name = LANGUAGES[source_language]
        target_lang_name = LANGUAGES[target_language]
        translated_text = translate_text(extracted_text, source_lang_name, target_lang_name)
        
        # Create output filename - sanitize base name to ensure safe filename
        base_name = os.path.splitext(safe_filename)[0]
        # Remove any potentially unsafe characters from base name
        safe_base_name = get_valid_filename(base_name)
        output_filename = f"{safe_base_name}_translated.pdf"
        output_path = os.path.join(settings.TRANSLATIONS_FOLDER, output_filename)
        
        # Ensure output path is within TRANSLATIONS_FOLDER
        output_path = os.path.abspath(output_path)
        translations_folder = os.path.abspath(settings.TRANSLATIONS_FOLDER)
        if not output_path.startswith(translations_folder):
            raise Exception("Invalid output file path detected.")
        
        # Create the translated PDF file
        create_pdf_file(translated_text, output_path)
        
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Redirect to success page with download link
        return redirect('translator:success', filename=output_filename)
        
    except Exception as e:
        # Clean up on error
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        # Log the full error for debugging
        import traceback
        error_trace = traceback.format_exc()
        print(f"Translation error: {str(e)}")
        print(f"Full traceback:\n{error_trace}")
        
        messages.error(request, f'Error processing document: {str(e)}')
        return redirect('translator:index')


@require_http_methods(["GET"])
def success(request, filename):
    """Render the success page with download link."""
    if not filename:
        messages.error(request, 'No file to download.')
        return redirect('translator:index')
    
    # Sanitize filename for security
    safe_filename = get_valid_filename(filename)
    
    # Verify the file actually exists
    file_path = os.path.join(settings.TRANSLATIONS_FOLDER, safe_filename)
    file_path = os.path.abspath(file_path)
    translations_folder = os.path.abspath(settings.TRANSLATIONS_FOLDER)
    
    if not file_path.startswith(translations_folder):
        messages.error(request, 'Invalid file path.')
        return redirect('translator:index')
    
    if not os.path.exists(file_path):
        messages.error(request, 'File not found.')
        return redirect('translator:index')
    
    return render(request, 'translator/success.html', {'filename': safe_filename})


@require_http_methods(["GET"])
def download(request, filename):
    """Download the translated document."""
    try:
        # Sanitize filename to prevent directory traversal
        safe_filename = get_valid_filename(filename)
        file_path = os.path.join(settings.TRANSLATIONS_FOLDER, safe_filename)
        
        # Additional security check - ensure the resolved path is within TRANSLATIONS_FOLDER
        file_path = os.path.abspath(file_path)
        translations_folder = os.path.abspath(settings.TRANSLATIONS_FOLDER)
        
        if not file_path.startswith(translations_folder):
            messages.error(request, 'Invalid file path.')
            return redirect('translator:index')
        
        if not os.path.exists(file_path):
            messages.error(request, 'File not found.')
            return redirect('translator:index')
        
        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=safe_filename
        )
    except Exception as e:
        messages.error(request, f'Error downloading file: {str(e)}')
        return redirect('translator:index')

