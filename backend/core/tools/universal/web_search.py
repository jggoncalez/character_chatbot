from google.genai import types

# A declaration que você registra no TOOL_DECLARATIONS
web_search_declaration = types.Tool(
    google_search=types.GoogleSearch()
)