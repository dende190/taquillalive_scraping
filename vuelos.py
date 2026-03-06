from navegador import Navegador
from telegram import Telegram
from playwright.async_api import Browser
import asyncio
import re

SELECTORES_POR_NOMBRE = {
  'vueloMasEconomicoPrecio': '[role=tablist] [data-hveid] [data-gs]',
  'platea2CampoTextoBoletas': 'input[data-section_id=S_PLT2]',
}

async def verificarVueloEconomico(navegador: Browser, enlace: str):
  vueloMasEconomicoPrecioAntiguo = 0;
  telegram = Telegram()
  while True:
    print('Buscando vuelos')

    htmlParseado = await navegador.obtenerPaginaContenido()

    vueloMasEconomicoPrecioTexto = (
      htmlParseado
      .select(SELECTORES_POR_NOMBRE['vueloMasEconomicoPrecio'])
      [0]
      .text
    )

    if not vueloMasEconomicoPrecioTexto:
      print('No encontro el valor del precio')
      continue

    vueloMasEconomicoPrecio = (
      int(re.split(r'\s', vueloMasEconomicoPrecioTexto)[1].replace(',', ''))
    )

    if not vueloMasEconomicoPrecioAntiguo:
      vueloMasEconomicoPrecioAntiguo = vueloMasEconomicoPrecio
      print(f'Valor inical {vueloMasEconomicoPrecio}')
      continue

    if (vueloMasEconomicoPrecio >= vueloMasEconomicoPrecioAntiguo):
      continue

    print('Vuelo encontrado')
    telegram.enviarMensaje(f'Vuelo mas economico encontrado, estaba en {vueloMasEconomicoPrecioAntiguo} y ahora esta en {vueloMasEconomicoPrecio}: {enlace}')
    vueloMasEconomicoPrecioAntiguo = vueloMasEconomicoPrecio

async def main():
  enlace = (
    input('\nIngresa el enlace de google flights: ').strip()
  )
  chatAEnviarMensajeId = (
    input('\nIngresa el chat Id de telegram: ').strip()
  )
  navegador = Navegador(enlace=enlace)
  print(f'Enlace abierto: {enlace}')
  await verificarVueloEconomico(navegador=navegador, enlace=enlace)

if __name__ == '__main__':
  asyncio.run(main())
