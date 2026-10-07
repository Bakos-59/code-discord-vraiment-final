import os
import requests
import discord

client = discord.Client()

# 1. Remplacez par l'ID du salon où le bot doit LIRE / ÉCOUTER le code
TARGET_CHANNEL_ID = 1552274226977968179  

# 2. Remplacez par l'ID du salon où le bot doit ENVOYER les rapports
LOG_CHANNEL_ID = 1552274237585236004     

@client.event
async def on_ready():
    print(f"Connecté en tant que : {client.user}")
    print(f"Le self-bot écoute activement les messages dans le salon ID : {TARGET_CHANNEL_ID}")

@client.event
async def on_message(message):
    # Ignore les messages envoyés par le bot lui-même pour éviter les boucles
    if message.author == client.user:
        return

    # C'est ici qu'il lit le code : on vérifie si le message vient du salon cible
    if message.channel.id == TARGET_CHANNEL_ID:
        code_saisi = message.content.strip()
        print(f"Code détecté dans le salon cible : {code_saisi}")
        
        # Récupération des paramètres de connexion
        captcha_sid = os.getenv("CAPTCHA_SID")
        cookies = {
            "sid": captcha_sid,
            "lang": "fr"
        }
        
        log_channel = client.get_channel(LOG_CHANNEL_ID)
        
        try:
            # Envoi du code récupéré vers le site
            payload = {"code": code_saisi}
            response = requests.post("https://captchapay.fr/api/account/redeem", cookies=cookies, data=payload, timeout=5)
            
            if response.status_code == 200:
                statut_texte = f"✅ **Succès !** Le code `{code_saisi}` a été validé et entré avec succès."
            else:
                statut_texte = f"❌ **Échec !** Le code `{code_saisi}` a été rejeté (Code HTTP : {response.status_code})."
                
        except Exception as e:
            statut_texte = f"⚠️ **Erreur technique** lors de la soumission du code `{code_saisi}` : {e}"

        # Envoi du rapport dans le salon de logs différent
        if log_channel:
            await log_channel.send(
                f"**[Rapport CaptchaPay]**\n"
                f"• Code détecté dans <#{TARGET_CHANNEL_ID}>\n"
                f"• Auteur : {message.author.mention}\n"
                f"• Statut : {statut_texte}"
            )
            print("Rapport envoyé dans le salon de logs.")
        else:
            print("Erreur : Impossible de trouver le salon de logs (LOG_CHANNEL_ID).")

# Lancement du self-bot
token = os.getenv("DISCORD_TOKEN")
if token:
    client.run(token)
else:
    print("Erreur : DISCORD_TOKEN manquant.")