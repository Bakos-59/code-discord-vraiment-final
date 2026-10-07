import discord
import re
import requests

client = discord.Client()

SALON_CIBLE_ID = 1554000268864135198  # Remplacez par votre ID de salon

COOKIES_CAPTCHAPAY = {
    "sid": os.getenv("CAPTCHA_SID"),  # Récupère la variable d'environnement
    "lang": "fr"
}

@client.event
async def on_ready():
    print(f'Connecté en tant que : {client.user}')

@client.event
async def on_message(message):
    if message.channel.id == SALON_CIBLE_ID:
        texte = message.content
        if message.embeds:
            for embed in message.embeds:
                if embed.description:
                    texte += "\n" + embed.description

        match = re.search(r"\b([A-Z0-9]{6})\b", texte)
        if match:
            code = match.group(1)
            print(f"🔥 Code détecté : {code}")
            
            # Envoi vers le site
            try:
                requests.post(
                    "https://captchapay.fr/api/account/redeem", 
                    json={"code": code}, 
                    cookies=COOKIES_CAPTCHAPAY, 
                    timeout=3
                )
                print(f"✅ Code {code} envoyé !")
            except Exception as e:
                print(f"❌ Erreur : {e}")

client.run(os.getenv("DISCORD_TOKEN"))