from telethon import TelegramClient, events
import time

# Your API ID and Hash
api_id = '24356162'  # Replace with your api_id
api_hash = '62ec18e1057a76c520f10662c66ef71b'  # Replace with your api_hash
bot_token = '7145293109:AAFpWPXnPbRk_svPa8dSkdn5gvDtiNXOpf8'  # Replace with your bot token
affiliate_bot_username = 'QuotexPartnerBot'  # Affiliate bot username

# Initialize the Telegram Client
client = TelegramClient('session_name', api_id, api_hash).start(bot_token=bot_token)

async def forward_to_affiliate(trader_id):
    # Send the trader ID to the affiliate bot and get the response
    await client.send_message(affiliate_bot_username, trader_id)

    # Wait for response from the affiliate bot
    async for message in client.iter_messages(affiliate_bot_username, limit=1):
        response = message.text
        return response

async def send_vip_link(chat_id):
    # VIP invite link generation logic here (with expiration)
    invite_link = await client.export_chat_invite_link(chat_id, expire_in=3600)  # Link expires in 1 hour
    await client.send_message(chat_id, f"Here's your VIP link: {invite_link}")

async def handle_trader_id(event):
    trader_id = event.text  # Assume user sends trader ID in the chat
    response = await forward_to_affiliate(trader_id)

    if "User found" in response and "Deposit" in response:
        # Extract deposit amount from response
        deposit_amount = float(response.split('Deposits Sum: $')[1].split()[0])
        if deposit_amount >= 30:
            # Send VIP link if deposit is sufficient
            await send_vip_link(event.chat.id)
        else:
            await client.send_message(event.chat.id, "Your deposit is less than the required amount to join the VIP group.")
    else:
        await client.send_message(event.chat.id, "No user found or invalid trader ID.")

@client.on(events.NewMessage())
async def my_event_handler(event):
    if event.is_private:  # Respond only to private messages
        await handle_trader_id(event)

client.run_until_disconnected()
