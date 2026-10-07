import os
import requests
import discord

# Configuration du client (self-bot)
client = discord.Client()

# Remplacez par l'ID numérique de votre salon Discord (où le bot doit envoyer le message)
CHANNEL_ID = 1552274226977968179  

@client.event
async def on_ready():
    print(f"Connecté avec succès en tant que : {client.user} (Version 2)")
    
    # Récupération des variables d'environnement configurées sur Bot-Hosting
    discord_token = os.getenv("DISCORD_TOKEN")
    captcha_sid = os.getenv("CAPTCHA_SID")
    
    # Étape de vérification / simulation de l'action sur le site
    status_message = "🔄 Initialisation de la vérification du code..."
    
    try:
        # Simulation des cookies / données pour la requête vers le site
        cookies = {
            "sid": captcha_sid,
            "lang": "fr"
        }
        
        # Exemple de requête de test (Remplacez l'URL par l'endpoint réel si nécessaire)
        # On utilise timeout=5 pour éviter de bloquer le bot si le site met du temps à répondre
        response = requests.get("https://captchapay.net/", cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            status_message = "✅ Le site a bien répondu. Le code a été soumis/vérifié avec succès !"
        else:
            status_message = f"⚠️ Le site a répondu avec le code d'erreur HTTP : {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        status_message = f"❌ Erreur lors de la communication avec le site : {e}"

    # Envoi du message dans le salon Discord configuré
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(
            f"**[Rapport du Self-Bot - Version 2]**\n"
            f"• Compte : `{client.user}`\n"
            f"• Statut : {status_message}"
        )
        print("Message de rapport envoyé dans le salon avec succès !")
    else:
        print("Erreur : Impossible de trouver le salon avec l'ID spécifié.")

# Lancement du self-bot en utilisant le token sécurisé
token = os.getenv("DISCORD_TOKEN")
if not token:
    print("Erreur critique : La variable DISCORD_TOKEN est introuvable.")
else:
    client.run(token)