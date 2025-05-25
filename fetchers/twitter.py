import snscrape.modules.twitter as sntwitter
import logging
import re

logger = logging.getLogger(__name__)

def extract_tweet_id(tweet_url: str) -> str | None:
    """Extrae el ID del tweet de una URL de Twitter/X."""
    # Patrón para URLs como https://twitter.com/user/status/12345
    # o https://x.com/user/status/12345
    # o https://twitter.com/user/status/12345?s=20
    match = re.search(r"(?:twitter\.com|x\.com)/[^/]+/status/(\d+)", tweet_url)
    if match:
        return match.group(1)
    return None

async def fetch_tweet_data(tweet_url: str) -> dict | None:
    """
    Extrae información de un tweet usando snscrape.
    Devuelve un diccionario con 'author', 'text' y 'url' o None si falla.
    """
    tweet_id = extract_tweet_id(tweet_url)
    if not tweet_id:
        logger.warning(f"No se pudo extraer el ID del tweet de la URL: {tweet_url}")
        return None

    try:
        scraper = sntwitter.TwitterTweetScraper(tweetId=tweet_id, mode=sntwitter.TwitterTweetScraperMode.SINGLE)
        tweet_data = None
        # snscrape.get_items() es un generador, pero para un solo tweet debería dar un item
        for i, tweet in enumerate(scraper.get_items()):
            if i == 0: # Solo nos interesa el primer (y único) tweet
                tweet_data = {
                    "author": tweet.user.username,
                    "text": tweet.renderedContent, # O tweet.rawContent si prefieres texto sin procesar
                    "url": tweet.url
                }
            break # Solo necesitamos el primer item
        
        if not tweet_data:
            logger.warning(f"No se encontró el tweet con ID: {tweet_id} desde URL: {tweet_url}")
            return None
            
        return tweet_data
    except Exception as e:
        logger.error(f"Error al scrapear el tweet {tweet_url} (ID: {tweet_id}): {e}", exc_info=True)
        return None

if __name__ == '__main__':
    # Ejemplo de uso (requiere un entorno async para probar 'await')
    import asyncio
    async def main_test():
        # Reemplaza con una URL de tweet válida para probar
        test_url = "https://twitter.com/elonmusk/status/1700000000000000000" # URL hipotética
        # Para probar una real, reemplaza la URL de arriba con una que exista
        # por ejemplo, test_url = "https://twitter.com/TwitterDev/status/1585724950049169408"
        
        # Asegúrate de que la URL que uses para probar exista, sino snscrape no devolverá nada.
        # Para encontrar una URL de tweet:
        # 1. Ve a Twitter/X
        # 2. Encuentra un tweet cualquiera
        # 3. Haz clic en el tweet para abrirlo en su propia página
        # 4. Copia la URL de la barra de direcciones del navegador
        # Ejemplo: test_url = "https://twitter.com/PythonWeekly/status/1772719082982473838" (reemplaza si no funciona)
        
        # Para que esta prueba funcione, asegúrate de que la URL es válida y el tweet público.
        # Cambia esta URL por una que sepas que existe.
        example_url = "https://twitter.com/jack/status/20" # El primer tweet de Jack Dorsey
        if example_url == "https://twitter.com/jack/status/20": # Placeholder check
            print("Por favor, reemplaza la URL de ejemplo en fetchers/twitter.py con una URL de tweet real y pública para probar.")
            return

        data = await fetch_tweet_data(example_url)
        if data:
            print("Datos del tweet extraídos:")
            print(f"  Autor: @{data['author']}")
            print(f"  Texto: {data['text'][:100]}...") # Muestra solo los primeros 100 caracteres
            print(f"  URL: {data['url']}")
        else:
            print(f"No se pudieron extraer datos para la URL: {example_url}")

    asyncio.run(main_test())