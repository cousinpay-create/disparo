from telethon import TelegramClient, types
import asyncio

api_id = '29101921'
api_hash = '763380a347c4db6aa5ea04bc6728d104'
client = TelegramClient('session_name', api_id, api_hash)
channel_id = 1003047007281

# ➤ IDs bloqueados
blocked_ids = [
    1002488975694,  # coloque aqui o ID do grupo que NÃO deve receber
]

async def send_message_to_my_groups():
    dialogs = await client.get_dialogs()

    last_post = await client.get_messages(channel_id, limit=1)
    if not last_post:
        print(f"Não foi possível encontrar mensagens no canal {channel_id}")
        return

    for dialog in dialogs:
        try:
            # pula se estiver bloqueado
            if dialog.id in blocked_ids:
                print(f"🔒 Ignorando (bloqueado): {dialog.title}")
                continue

            if dialog.is_group or dialog.is_channel:
                if dialog.is_channel:
                    peer = types.PeerChannel(dialog.id)
                else:
                    peer = types.PeerChat(dialog.id)

                await client.forward_messages(peer, last_post[0].id, from_peer=channel_id)
                print(f"Mensagem encaminhada para: {dialog.title}")

        except Exception:
            pass

async def periodic_task():
    while True:
        await send_message_to_my_groups()
        print("Esperando 1 hora até o próximo envio...")
        await asyncio.sleep(3600)

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(periodic_task())
