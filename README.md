# Initial Setup 

1) Create a New API key on openrouter for mistralai/devstral-small:free
2) Copy that key and paste it in the app.py file (YOUR_API_KEY)


# To run this app 

pip install openai uvicorn fastapi

uvicorn app:app --reload --host 0.0.0.0 --port 8000

