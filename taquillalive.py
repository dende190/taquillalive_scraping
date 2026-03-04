from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Browser, Page
import asyncio
import random
import time
import requests

ENLACE = ()
PAGINA_TIEMPO_ESPERA_EN_MILISEGUNDOS = 60000
SELECTORES_POR_NOMBRE = {
  'platea1CampoTextoBoletas': 'input[data-section_id=S_PLT1]',
  'platea2CampoTextoBoletas': 'input[data-section_id=S_PLT2]',
}
ENCABEZADO_USUARIO_AGENTE = (
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
)

playwright = None
async def abrirNavegador() -> Browser:
  global playwright
  playwright = await async_playwright().start()
  navegador = await playwright.chromium.launch(headless=True)
  print('Navegador abierto')
  return navegador

async def cerrarNavegador(navegador: Browser):
  await navegador.close();
  await playwright.stop()
  print('Navegador cerrado')

def enviarTelegramMensaje():
  chat_id = ''
  message = ('Boletas platea disponibles ' + ENLACE)

  telegramEnlace = ()
  telegramParametros = {
    'chat_id': chat_id,
    'text': message
  }

  try:
    response = requests.get(telegramEnlace, params=telegramParametros)
    response.raise_for_status()
    print("Message sent successfully!")
  except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

async def verificarBoletasDisponibilidad(navegador: Browser) -> dir:
  navegadorContexto = await (
    navegador.new_context(user_agent=ENCABEZADO_USUARIO_AGENTE)
  )
  navegadorPestana = await navegadorContexto.new_page()
  await (
    navegadorPestana.goto(ENLACE, timeout=PAGINA_TIEMPO_ESPERA_EN_MILISEGUNDOS)
  )
  await navegadorPestana.wait_for_load_state('networkidle')
  navegadorPestanaContenido = await navegadorPestana.content()
  htmlParseado = BeautifulSoup(navegadorPestanaContenido, 'html.parser')
  print(f'Enlace abierto: {ENLACE}')

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

  return False

async def inicializarBusqueda():
  navegador = None;
  try:
    navegador = await abrirNavegador()
    return await verificarBoletasDisponibilidad(navegador=navegador)
  finally:
    if navegador:
      await cerrarNavegador(navegador=navegador)

async def main():
  while (True):
    time.sleep(random.uniform(1, 6))
    hayBoletas = await inicializarBusqueda()
    if hayBoletas:
      enviarTelegramMensaje()
      break;

if __name__ == '__main__':
  asyncio.run(main())
