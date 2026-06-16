import google.generativeai as genai

import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash-native-audio-latest"
)

response = model.generate_content(
    "Say only: Gemini Working"
)

print(response.text)