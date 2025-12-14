# Student Translator App

A Flask web application that translates student documents between English, French, Arabic, Swahili, and Kinyarwanda using OpenAI GPT-4.

## Features

- Upload PDF and DOCX files
- Automatic language detection
- Translation between 5 languages
- Download translated documents as PDF

## Deployment on Render

### Prerequisites
1. Create a Render account at https://render.com
2. Get an OpenAI API key from https://platform.openai.com

### Deployment Steps

1. **Connect your repository** to Render
2. **Create a new Web Service**
3. **Set environment variables** in Render dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
4. **Deploy** - Render will automatically use the configuration from `render.yaml`

### Environment Variables Required

- `OPENAI_API_KEY`: Your OpenAI API key (set this in Render dashboard)
- `PORT`: Automatically set by Render

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## File Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── render.yaml        # Render deployment configuration
├── runtime.txt        # Python version specification
├── Procfile          # Alternative deployment configuration
├── .env              # Environment variables (local only)
├── .gitignore        # Git ignore file
├── static/           # CSS and JavaScript files
├── templates/        # HTML templates
├── uploads/          # Temporary file uploads (created at runtime)
└── translations/     # Generated translations (created at runtime)
```

## Supported File Types

- PDF (.pdf)
- Microsoft Word (.docx)

## Supported Languages

- English
- French
- Arabic
- Swahili
- Kinyarwanda