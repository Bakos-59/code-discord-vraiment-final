import discord
import re
import requests
import os

client = discord.Client()

SALON_CIBLE_ID = 1552274226977968179  # Salon où le bot lit le code
LOG_CHANNEL_ID = 1552274237585236004  # Remplacez par l'ID de votre salon de logs pour les rapports

COOKIES_CAPTCHAPAY = {
    "sid": os.getenv("CAPTCHA_SID"),
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
            
            log_channel = client.get_channel(LOG_CHANNEL_ID)
            statut_texte = ""
            
            # Envoi vers le site et analyse de la réponse
            try:
                response = requests.post(
                    "https://captchapay.fr/api/account/redeem", 
                    json={"code": code}, 
                    cookies=COOKIES_CAPTCHAPAY, 
                    timeout=3
                )
                
                print(f"✅ Code {code} envoyé ! (Statut HTTP : {response.status_code})")
                
                # Vous pouvez ajuster cette condition selon ce que le site renvoie en cas de succès
                if response.status_code == 200:
                    statut_texte = f"✅ **Code mis avec succès** : `{code}`"
                else:
                    statut_texte = f"⚠️ **Code non validé** par le site (Code HTTP : {response.status_code}) pour `{code}`"
                    
            except Exception as e:
                print(f"❌ Erreur : {e}")
                statut_texte = f"❌ **Erreur technique** lors de l'envoi du code `{code}` : {e}"

            # Envoi du rapport dans le salon de logs unique
            if log_channel:
                try:
                    await log_channel.send(
                        f"**[Rapport CaptchaPay]**\n"
                        f"• Statut : {statut_texte}\n"
                        f"• Auteur du message : {message.author.mention}"
                    )
                    print("Rapport envoyé dans le salon de logs.")
                except Exception as log_err:
                    print(f"Erreur lors de l'envoi du rapport dans le salon de logs : {log_err}")
            else:
                print("Attention : LOG_CHANNEL_ID introuvable ou mal configuré.")

client.run(os.getenv("DISCORD_TOKEN"))