import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# # OpenAI Key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'facts.csv')
CHROMA_PATH = os.path.join(BASE_DIR, 'chroma_db')
