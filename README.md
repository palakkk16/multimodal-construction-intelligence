# Multimodal Construction Intelligence Platform

A Streamlit capstone starter app with four modules:
1. Site Safety & PPE Audit
2. Crack Diagnostics & Structural Integrity
3. Planning & Indicative Real Estate Valuation
4. Daily Site Assistant & Weather-Aware Advisory

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Gemini API key

Paste your Google Gemini API key into the password field in the sidebar. The app uses it for optional image analysis and chatbot responses. If no key is supplied, the app runs in demonstration mode with explicitly labelled sample outputs.

For deployment, you can use Streamlit Community Cloud secrets instead of entering the key in the UI. If you do this, update `app.py` to read `st.secrets["GEMINI_API_KEY"]`; do not commit secrets to Git.

## Deploy to Streamlit Community Cloud

1. Push `app.py`, `requirements.txt`, and `README.md` to a GitHub repository.
2. Create a new app at https://share.streamlit.io/.
3. Select the repository and `app.py` as the main file.
4. Deploy. No external database is required.

## Important limitations

- Demo mode does not analyze uploaded images. It returns sample data, clearly labelled as demo output.
- AI image outputs can be wrong. A photo cannot reliably verify all PPE, establish code compliance, measure crack width without a scale, or certify structural safety.
- Planning costs, market valuation, steel, and cement quantities are illustrative assumptions, not a bill of quantities, structural design, or professional valuation.
- Verify all safety-critical decisions with the site's qualified safety officer and structural engineer.
- Gemini model availability can change; if the configured model is unavailable, select a currently supported vision-capable model in `app.py`.
