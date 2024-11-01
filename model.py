from transformers import pipeline
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
import os
import time

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

def imageGeneration_langChain(scenario, styles):
    
    image_prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Generate an image in the {styles_lang} style based on the scenario: '{scenario_lang}'"
            ),
            ("human", "{scenario_lang}")
        ]
    )

    prompt = image_prompt_template.format(scenario_lang=scenario, styles_lang=styles)

    print("Generated Prompt for DALL-E:")
    print(prompt)

    client = OpenAI()
    imageResponse = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format='url'
    )

    img_url = imageResponse.data[0].url
    return img_url

def saveImage(image_url, save_path):
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {save_path}")    
    else:
        print("Failed")

def runModels_langChain(url, styles):
    scenario = img2text(url)
    story = textGeneration_langChain(scenario)
    img_url = imageGeneration_langChain(scenario, styles)

    save_folder = 'static/imgs'
    os.makedirs(save_folder, exist_ok=True)
    file_name = f"generated_image_{int(time.time())}.png"
    save_path = os.path.join(save_folder, file_name)

    print(f"Image URL: {img_url}")
    # print(f"Saving image to: {save_path}")

    saveImage(img_url, save_path)
    relative_path = os.path.join('imgs', file_name)

    return([scenario,story,relative_path])