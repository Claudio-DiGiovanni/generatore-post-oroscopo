import os
import tkinter as tk
import openai
import random
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
import datetime
import uuid
import io
import openAIKey

def show_image(img_path):
    img = Image.open(img_path)
    img.show()


# Imposta la chiave API di OpenAI
openai.api_key = openAIKey.openai_api_key


# Crea una lista dei segni zodiacali
zodiac_signs = ["Ariete", "Toro", "Gemelli", "Cancro", "Leone", "Vergine", "Bilancia", "Scorpione", "Sagittario", "Capricorno", "Acquario", "Pesci"]

date = datetime.datetime.now().strftime("%Y-%m-%d")

def generate_and_save():

# Seleziona un segno zodiacale in modo casuale
    sign = random.choice(zodiac_signs)

# Scarica l'immagine dal web
    response = openai.Image.create(
        prompt=f"uno sfondo a tinta unica con colori scuri e che presenti riferimenti al segno zodiacale {sign}",
        n=1,
        size="1024x1024"
    )
    img_url = response['data'][0]['url']
    response1 = requests.get(img_url)
    img = Image.open(io.BytesIO(response1.content))

    # Genera la trascrizione dell'oroscopo
    prompt = (f"Genera una previsione lunga e accattivante per il segno zodiacale {sign} in italiano calcolando che la data corrente è {date}")
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    oroscopo = completions.choices[0].text

    d = ImageDraw.Draw(img)
    # Scegli un font di dimensioni più grandi
    font = ImageFont.truetype("Candaral.ttf", 50)
    # Scegli un colore contrastante

    lines = textwrap.wrap(oroscopo, width=30)
    y_text = 10
    for line in lines:
        width, height = d.textsize(line, font)
        d.text(((img.width - width) / 2, y_text), line, font=font, fill=(255, 255, 255))
        y_text += height

    # Crea un nome univoco per il file immagine
    img_name = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{str(uuid.uuid4().int)[:8]}-oroscopo.jpg"
    # Crea il percorso completo per l'immagine
    img_folder = "img"
    img_path = os.path.join(img_folder, img_name)
    # Salva l'immagine
    img.save(img_path)
    show_image(img_path)

    # Genera la caption accattivante
    prompt = (f"Genera una caption per instagram accattivante per l'oroscopo {sign} in italiano aggiungendo oltre alla caption anche ashtag a tema")
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop= None,        
        temperature=0.5,
    )
    caption = completions.choices[0].text

    # Specifica il percorso della cartella caption
    caption_folder = "caption"
    # Crea un nome univoco per il file caption
    caption_name = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{str(uuid.uuid4().int)[:8]}-caption.txt"
    # Crea il percorso completo per il file caption
    caption_path = os.path.join(caption_folder, caption_name)
    # Salva la caption
    with open(caption_path, "w") as f:
        f.write(caption)
root = tk.Tk()
generate_and_save_button = tk.Button(root, text="Genera e salva", command=generate_and_save)
generate_and_save_button.pack()
root.mainloop()
