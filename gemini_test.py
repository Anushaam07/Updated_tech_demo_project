# import os
# import google.generativeai as genai

# api_key = os.getenv("GEMINI_API_KEY")
# model_name = os.getenv("MODEL_ID", "models/gemini-2.0-flash")

# if not api_key:
#     print("GEMINI_API_KEY is not set!")
#     exit()

# genai.configure(api_key=api_key)

# try:
#     model = genai.GenerativeModel(model_name)
#     response = model.generate_content("Health check: respond with OK")
#     print("Gemini Response:", response.text)
#     print("Gemini API Key is working fine!")
# except Exception as e:
#     print("Gemini API error:", e)


import google.generativeai as genai

genai.configure(api_key="AIzaSyBwfjKs0qlfq-ivK209Gy7KKsfXXr209Jo")

model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("Hello, world!")
print(response.text)
