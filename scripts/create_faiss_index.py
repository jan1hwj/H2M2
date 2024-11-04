import wikipediaapi
from datasets import Dataset
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

# Initialize Wikipedia API
user_agent = "This is a course project to practice how to incorporate external API. For educational purpose only."
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent=user_agent
)

# List of painting styles to retrieve
art_styles = [
    "Watercolor",
    "Cubism", 
    "Pop Art", 
    "Realism (arts)",
    "Cartoon",
    "Art Deco"
]

# Retrieve and store descriptions for each style
data = []
for style in art_styles:
    page = wiki.page(style)
    if page.exists():
        summary = page.summary
        data.append({"style": style, "description": summary})
    else:
        print(f"Page for {style} not found on Wikipedia.")

# Convert to dataset format
data_dict = {
    "style": [entry["style"] for entry in data],
    "description": [entry["description"] for entry in data]
}
dataset = Dataset.from_dict(data_dict)

# Generate embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
data_dict["embedding"] = [embedding_model.encode(description, convert_to_tensor=False) for description in data_dict["description"]]

# Create FAISS index
text_embedding_pairs = list(zip(data_dict["description"], data_dict["embedding"]))
metadata = [{"style": style} for style in data_dict["style"]]

faiss_index = FAISS.from_embeddings(
    text_embedding_pairs,
    HuggingFaceEmbeddings(),
    metadatas=metadata
)

# Ensure data directory exists
index_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_index')
os.makedirs(index_dir, exist_ok=True)

# Save the FAISS index to the data directory
faiss_index.save_local(index_dir)
print(f"FAISS index created and saved to {index_dir}")
