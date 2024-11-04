from transformers import pipeline
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import requests
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the FAISS index
index_dir = os.path.join(os.path.dirname(__file__), 'data', 'faiss_index')
embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
faiss_index = FAISS.load_local(index_dir, embedding_model, allow_dangerous_deserialization=True)

def retrieve_style_info(style):
    
    logging.info(f"Retrieving style information for: {style}")

    retriever = faiss_index.as_retriever()
    rag_chain = RetrievalQA.from_chain_type(
        llm = ChatOpenAI(model="gpt-4o-mini"),
        retriever = retriever,
        chain_type = "stuff"
    )
    result = rag_chain({"query": f"Tell me about the {style} painting style."})
    logging.info(f"Retrieved style information: {result['result']}")
    return result['result']

def img2text(url):
    img_to_text_pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
    text = img_to_text_pipe(url)[0]["generated_text"]
    return text

def textGeneration_langChain(msg):
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        max_tokens= 200,
        timeout=None,
        max_retries=2,
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert short story teller. Using a simple narrative you generate story in less than 100 words based on the given scenario."
            ),
            ("human","{scenario_lang}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    out_message = chain.invoke({"scenario_lang" : msg})
    return out_message

def imageGeneration_langChain(scenario, styles, style_info):

    logging.info(f"Generating image for scenario: '{scenario}' with style: '{styles}'")
    logging.info(f"Style information used in prompt: {style_info}")
    
    image_prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Generate an image in the {styles_lang} style, described as: '{style_info}'. The scenario is: '{scenario_lang}'"
            ),
            ("human", "{scenario_lang}")
        ]
    )

    prompt = image_prompt_template.format(scenario_lang=scenario, styles_lang=styles, style_info=style_info)
    logging.info(f"Generated Prompt for DALL-E: {prompt}")

    client = OpenAI()
    imageResponse = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format='url'
    )

    img_url = imageResponse.data[0].url
    logging.info(f"Generated image URL: {img_url}")
    return img_url

def saveImage(image_url, save_path):
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        logging.info(f"Image saved to {save_path}")    
    else:
        logging.error("Failed to save image")

def runModels_langChain(url, styles):
    scenario = img2text(url)
    story = textGeneration_langChain(scenario)
    style_info = retrieve_style_info(styles)
    img_url = imageGeneration_langChain(scenario, styles, style_info)

    save_folder = 'static/imgs'
    os.makedirs(save_folder, exist_ok=True)
    file_name = f"generated_image_{int(time.time())}.png"
    save_path = os.path.join(save_folder, file_name)

    logging.info(f"Image URL: {img_url}")

    saveImage(img_url, save_path)
    relative_path = os.path.join('imgs', file_name)

    return([scenario,story,relative_path])