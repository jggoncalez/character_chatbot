from google.genai import types

# Futuro
web_search_declaration = types.Tool(
    google_search=types.GoogleSearch()
)