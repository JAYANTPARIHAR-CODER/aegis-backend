AEGIS Backend

Run locally:

1. (optional) Create and activate a virtualenv:

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2. Install dependencies:

   pip install -r requirements.txt

3. Start the server:

   uvicorn main:app --reload --host 127.0.0.1 --port 8000

Or run the helper script:

./start_backend.ps1

The API root responds at `http://127.0.0.1:8000/`.
