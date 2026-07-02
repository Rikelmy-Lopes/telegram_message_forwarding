
from telethon import TelegramClient, events
from bot import send_message
from config import API_HASH, API_ID, CANAIS_ALVO, PALAVRAS_CHAVE
from utils import send_notification

print(f"Palavras sendo monitoradas: {PALAVRAS_CHAVE}\n")
print(f"Canais sendo monitorados: {CANAIS_ALVO}\n")

client = TelegramClient('sessao_monitor', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CANAIS_ALVO))
async def monitorador(event):
    texto_mensagem: str = event.message.text

    if not texto_mensagem:
        return

    for palavra in PALAVRAS_CHAVE:
        if palavra in texto_mensagem.lower():
            print(f"Palavra encontrada no canal {event.chat.title}!")
            
            link_mensagem = f"https://t.me/{event.chat.username}/{event.message.id}" if event.chat.username else "Canal Privado"
            alerta = f"🚨 **Palavra-chave detectada! ({palavra})** \n\nCanal: {event.chat.title}\nTexto: {texto_mensagem}\nLink: {link_mensagem}"
            
            await send_message(alerta)
            send_notification(alerta, palavra)
            break

    


print("Monitor iniciado... Pressione Ctrl+C para parar.")

with client:
    client.run_until_disconnected()