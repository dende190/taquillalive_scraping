from dotenv import load_dotenv
import requests
import os

load_dotenv()

class Telegram:

  telegramBotId = None
  chatAEnviarMensajeId = None

  def __init__(self, chatAEnviarMensajeId=''):
    self.telegramBotId = os.getenv('TELEGRAM_BOT_ID')
    self.chatAEnviarMensajeId = (
      chatAEnviarMensajeId or
      os.getenv('TELEGRAM_CHAT_ID_POR_DEFECTO')
    )

  def enviarMensaje(self, mensaje):
    botEnlace = f'https://api.telegram.org/bot{self.telegramBotId}/sendMessage'
    botParametros = {
      'chat_id': self.chatAEnviarMensajeId,
      'text': mensaje,
    }

    try:
      response = requests.get(botEnlace, params=botParametros)
      response.raise_for_status()
      print('Mensaje enviado !')
    except requests.exceptions.RequestException as e:
      print(f'Ha ocurrido un error: {e}')
