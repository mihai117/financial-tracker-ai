import os
import firebase_admin
from firebase_admin import credentials

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # this way we can retrieve the base directory of the project

cred_path = os.path.join(BASE_DIR, 'config', 'firebase', 'financial-tracker-ai-firebase-adminsdk-fbsvc-095fc94a81.json') # constructing the path to the key location
cred = credentials.Certificate(cred_path)

firebase_admin.initialize_app(cred)