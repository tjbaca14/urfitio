from sentence_transformers import SentenceTransformer
import os
# Define the model you want to download (for example, "paraphrase-MiniLM-L6-v2")
model_name = "sentence-transformers/all-mpnet-base-v2"

# Load the model
model = SentenceTransformer(model_name, use_auth_token=os.environ.get("HF_TOKEN"))

# Optionally, save the model locally
model.save("./model")