import os
import requests
import discord

client = discord.Client()

# Configuration des salons (Remplacez par vos vrais IDs numériques)
TARGET_CHANNEL_ID = 1552274239883714561  # Le salon où vous entrez / postez le code
LOG_CHANNEL_ID = 1552274237585236004     # Le salon unique où TOUS les rapports sont envoyés

@client.event
async def on_ready():
    print(f"Connecté en tant que : {client.user}")
    print("Le self-bot écoute les messages pour traiter et rapporter les codes.")

@client.event
async def on_message(message):
    # Ignore les propres messages du bot pour éviter les boucles
    if message.author == client.user:
        return

    # Le bot lit le code uniquement dans le salon cible (TARGET_CHANNEL_ID)
    if message.channel.id == TARGET_CHANNEL_ID:
        code_saisi = message.content.strip()
        print(f"Code détecté : {code_saisi}")
        
        # Récupération des paramètres de session depuis les variables d'environnement
        captcha_sid = os.getenv("CAPTCHA_SID")
        cookies = {
            "sid": captcha_sid,
            "lang": "fr"
        }
        
        log_channel = client.get_channel(LOG_CHANNEL_ID)
        statut_texte = ""
        
        try:
            # Envoi du code récupéré vers le site via une requête HTTP
            payload = {"code": code_saisi}
            response = requests.post("https://captchapay.fr/api/account/redeem", cookies=cookies, data=payload, timeout=5)
            
            # Cas 1 : La requête a réussi (200 OK)
            if response.status_code == 200:
                # Vous pouvez affiner cette condition selon le texte renvoyé par le site si nécessaire
                # Par exemple, si le site renvoie un JSON avec un statut de validation :
                # data = response.json()
                # if data.get("success"): ...
                
                statut_texte = f"✅ **Code mis avec succès** (Code: `{code_saisi}`)"
            else:
                # Cas 2 : Le site a répondu, mais avec une erreur / code rejeté
                statut_texte = f"⚠️ **Code non validé** par le site (Code HTTP : {response.status_code} pour `{code_saisi}`)"
                
        except Exception as e:
            # Cas 3 : Impossible d'envoyer le code (erreur réseau, site hors ligne, etc.)
            statut_texte = f"❌ **Échec de l'envoi du code** `{code_saisi}`.\n• Erreur technique : {e}"

        # Dans TOUS les cas, on envoie le rapport dans le salon de logs
        if log_channel:
            await log_channel.send(
                f"**[Rapport CaptchaPay]**\n"
                f"• Statut : {statut_texte}\n"
                f"• Posté par : {message.author.mention}"
            )
            print("Rapport envoyé dans le salon de logs.")
        else:
            print("Erreur : Salon de logs (LOG_CHANNEL_ID) introuvable.")

# Lancement du self-bot
token = os.getenv("DISCORD_TOKEN")
if token:
    client.run(token)
else:
    print("Erreur : La variable DISCORD_TOKEN est introuvable.")