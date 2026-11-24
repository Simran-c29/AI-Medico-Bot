# AI Medico Bot

An educational Streamlit app for asking questions about a medical-report PDF. It uses Hugging Face embeddings, FAISS or ChromaDB for retrieval, and Google Gemini or a local Ollama model for answers.

## Run locally

1. Use Python 3.12 and create an environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. For Google Gemini, copy `.env.example` to `.env` and set `GOOGLE_API_KEY` to your own API key. Keep `.env` private.

   Alternatively, install [Ollama](https://ollama.com/), start its local service, and pull a model such as `llama3.2`. Select **Ollama** in the app.

3. Start the app:

   ```powershell
   streamlit run app.py
   ```

4. Upload a PDF, choose the model and vector database, then select **Build Database**.

The first build downloads the selected embedding model. Uploaded reports and generated vector databases are local and excluded from Git.

## Medical information

This app is for educational purposes only. It does not diagnose conditions or replace professional medical advice. Do not upload sensitive reports to services you do not trust; when using Gemini, report content is sent to Google's API.
