from azure.storage.blob import ContainerClient
from io import BytesIO
import PyPDF2
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Charger les variables .env
load_dotenv()

# Azure OpenAI
client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def poser_question(question, contexte):
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "Tu es un expert du jardinage."},
            {"role": "user", "content": f"Voici des extraits de documents :\n{contexte}\n\nQuestion : {question}"}
        ],
        max_tokens=700,
        temperature=0.5,
        top_p=1.0
    )
    return response.choices[0].message.content

def lire_tous_les_pdfs_du_dossier():
    sas_folder_url = os.getenv("AZURE_STORAGE_SAS_FOLDER")
    if not sas_folder_url:
        raise ValueError("La variable AZURE_STORAGE_SAS_FOLDER n’est pas définie.")

    # Extraire les infos
    parts = sas_folder_url.split('/')
    account_url = f"{parts[0]}//{parts[2]}"
    container_name = parts[3]
    folder_path = '/'.join(parts[4:]).split('?')[0]
    sas_token = sas_folder_url.split('?')[1]

    container = ContainerClient(
        account_url=account_url,
        container_name=container_name,
        credential=f"?{sas_token}"
    )

    textes = []
    for blob in container.list_blobs(name_starts_with=folder_path):
        if blob.name.lower().endswith(".pdf"):
            try:
                blob_client = container.get_blob_client(blob.name)
                stream = BytesIO()
                blob_data = blob_client.download_blob()
                blob_data.readinto(stream)
                stream.seek(0)

                reader = PyPDF2.PdfReader(stream)
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            textes.append(page_text)
                    except Exception as e:
                        print(f"Erreur lecture page {page_num} du fichier {blob.name} : {e}")

            except Exception as e:
                print(f"Erreur lecture fichier {blob.name} : {e}")
                continue

    return "\n".join(textes)
