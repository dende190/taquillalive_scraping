from navegador import Navegador
from telegram import Telegram
from playwright.async_api import Browser
import asyncio

SELECTORES_POR_NOMBRE = {
  'platea1CampoTextoBoletas': 'input[data-section_id=S_PLT1]',
  'platea2CampoTextoBoletas': 'input[data-section_id=S_PLT2]',
}

async def verificarBoletasDisponibilidad(navegador: Browser) -> bool:
  print('Buscando boletas')

  htmlParseado = await navegador.obtenerPaginaContenido()

  dPlatea1CampoTextoBoletas = (
    htmlParseado.select(SELECTORES_POR_NOMBRE['platea1CampoTextoBoletas'])
  )
  if dPlatea1CampoTextoBoletas:
    boletasDisponibles = int(dPlatea1CampoTextoBoletas[0]['data-available'])
    if boletasDisponibles:
      return True

  dPlatea2CampoTextoBoletas = (
    htmlParseado.select(SELECTORES_POR_NOMBRE['platea2CampoTextoBoletas'])
  )
  if dPlatea2CampoTextoBoletas:
    boletasDisponibles = int(dPlatea2CampoTextoBoletas[0]['data-available'])
    if boletasDisponibles:
      return True

  await verificarBoletasDisponibilidad(navegador=navegador)

async def main():
  enlace = (
    input('\nIngresa el enlace de la compra de boletas: ').strip()
  )
  chatAEnviarMensajeId = (
    input('\nIngresa el chat Id de telegram: ').strip()
  )
  navegador = Navegador(enlace=enlace)
  print(f'Enlace abierto: {enlace}')
  await verificarBoletasDisponibilidad(navegador=navegador)

  telegram = Telegram()
  telegram.enviarMensaje(f'Boletas platea encontradas: {enlace}')

if __name__ == '__main__':
  asyncio.run(main())
