from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Browser, Page
import random
import time

class Navegador:
  PAGINA_TIEMPO_ESPERA_EN_MILISEGUNDOS = 60000
  ENCABEZADO_USUARIO_AGENTE = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
  )

  enlace = ''
  playwright = None
  paginaContenido = None
  chromium = None
  chromiumContexto = None
  pagina = None

  def __init__(self, enlace):
    self.enlace = enlace

  async def abrir(self):
    self.playwright = await async_playwright().start()
    chromium = await self.playwright.chromium.launch(headless=True)
    self.chromiumContexto = await (
      chromium.new_context(user_agent=self.ENCABEZADO_USUARIO_AGENTE)
    )
    self.chromium = chromium
    print('Navegador abierto')

  async def obtenerPaginaContenido(self):
    if not self.chromiumContexto:
      await self.abrir()

    if self.pagina:
      return await self.recargar()

    pagina = await self.chromiumContexto.new_page()
    self.pagina = pagina
    await (
      pagina
      .goto(self.enlace, timeout=self.PAGINA_TIEMPO_ESPERA_EN_MILISEGUNDOS)
    )
    await pagina.wait_for_load_state('networkidle')
    paginaContenido = await pagina.content()
    return BeautifulSoup(paginaContenido, 'html.parser')

  async def cerrar(self):
    await self.chromium.close();
    await self.playwright.stop()
    print('Navegador cerrado')

  async def recargar(self):
    print('recargando pagina')

    time.sleep(random.uniform(1, 6))
    pagina = self.pagina
    await pagina.reload(wait_until='networkidle')
    paginaContenido = await pagina.content()
    return BeautifulSoup(paginaContenido, 'html.parser')
