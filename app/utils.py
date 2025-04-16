import PyPDF2
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Charger variables depuis .env
load_dotenv()

# Connexion Azure OpenAI via SDK officiel
client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Lecture PDF
def lire_pdf(path):
    texte = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            texte += page.extract_text()
    return texte

# Poser une question à GPT
def poser_question(question, contexte):
    reponse = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "Tu es un assistant expert en jardinage."},
            {"role": "user", "content": f"Voici un extrait de document :\n{contexte}\n\nQuestion : {question}"}
        ],
        max_tokens=700,
        temperature=0.5,
        top_p=1.0
    )
    return reponse.choices[0].message.content
