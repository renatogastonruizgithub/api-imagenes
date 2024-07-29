import firebase_admin
from firebase_admin import credentials, storage
import uuid
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET')
FIREBASE_TYPE = os.getenv('FIREBASE_TYPE')
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
FIREBASE_PRIVATE_KEY_ID = os.getenv('FIREBASE_PRIVATE_KEY_ID')
FIREBASE_PRIVATE_KEY = os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n')
FIREBASE_CLIENT_EMAIL = os.getenv('FIREBASE_CLIENT_EMAIL')
FIREBASE_CLIENT_ID = os.getenv('FIREBASE_CLIENT_ID')
FIREBASE_AUTH_URI = os.getenv('FIREBASE_AUTH_URI')
FIREBASE_TOKEN_URI = os.getenv('FIREBASE_TOKEN_URI')
FIREBASE_AUTH_PROVIDER_X509_CERT_URL = os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL')
FIREBASE_CLIENT_X509_CERT_URL = os.getenv('FIREBASE_CLIENT_X509_CERT_URL')
FIREBASE_UNIVERSE_DOMAIN=os.getenv('FIREBASE_UNIVERSE_DOMAIN')

cred = credentials.Certificate({
  "type": FIREBASE_TYPE,
    "project_id": FIREBASE_PROJECT_ID,
    "private_key_id": FIREBASE_PRIVATE_KEY_ID,
    "private_key": FIREBASE_PRIVATE_KEY,
    "client_email": FIREBASE_CLIENT_EMAIL,
    "client_id": FIREBASE_CLIENT_ID,
    "auth_uri": FIREBASE_AUTH_URI,
    "token_uri": FIREBASE_TOKEN_URI,
    "auth_provider_x509_cert_url": FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url": FIREBASE_CLIENT_X509_CERT_URL,
  "universe_domain":FIREBASE_UNIVERSE_DOMAIN
})

firebase_admin.initialize_app(cred, {
    'storageBucket':FIREBASE_STORAGE_BUCKET
})

def upload_image_from_firebase(image):
    try:
        bucket = storage.bucket()            
        blob = bucket.blob(f'portafolio/{uuid.uuid4()}-{image.name}')
        blob.upload_from_file(image.file, content_type=image.content_type)
        blob.make_public()
        firebase_url = blob.public_url
        return firebase_url
    except Exception as e:
        print("Error en firebase subir archivo:", e)
        return False     


def delete_image_from_firebase(url): 
    try: 
        # Extraer el nombre del archivo de la URL
        filename = url.split('/')[-1].split('portafolio/')[0]        
        # Obtener una referencia al bucket de almacenamiento de Firebase
        bucket = storage.bucket()
        # Obtener una referencia al archivo en Firebase Storage
        blob = bucket.blob("portafolio/"+filename)              
        blob.delete()       
        return True  

    except Exception as e:
        print("Error en firebase al eliminar el archivo:", e)
        return False 