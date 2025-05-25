import logging
# import asyncio # asyncio es importado por telegram.ext así que no es estrictamente necesario importarlo aquí directamente
from telegram import BotCommand
from telegram.ext import Application, ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers import start_command_handler, handle_forwarded_message, reddit_command_handler


# Configuración básica de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def post_init(application: Application) -> None: # <--- ESTA ES LA LÍNEA CORREGIDA
    """
    Tareas a realizar después de que la aplicación se ha inicializado
    y antes de que comience el polling/webhook.
    Aquí configuramos los comandos del bot y la descripción.
    """
    bot_commands = [
        BotCommand("start", "🚀 Iniciar el bot y ver mensaje de bienvenida"),
        BotCommand("reddit", "🌐 Publicar posts de Reddit: /reddit <subreddit> [cantidad]")
    ]
    try:
        await application.bot.set_my_commands(bot_commands)
        logger.info("Comandos del bot configurados en el menú.")
    except Exception as e:
        logger.error(f"Error al configurar los comandos del bot: {e}", exc_info=True)


    bot_description = (
        "Soy CodevsBot, tu asistente para compartir contenido destacado. ✨\n\n"
        "Reenvíame mensajes de Telegram y (si eres admin) los publicaré en el canal del grupo Codevs."
    )
    try:
        await application.bot.set_my_description(description=bot_description)
        logger.info("Descripción del bot configurada.")
    except Exception as e:
        logger.error(f"Error al configurar la descripción del bot: {e}", exc_info=True)
    
    # bot_short_description = "Asistente para Codevs."
    # try:
    #     await application.bot.set_my_short_description(short_description=bot_short_description)
    #     logger.info("Descripción corta (About) del bot configurada.")
    # except Exception as e:
    #     logger.error(f"Error al configurar la descripción corta del bot: {e}", exc_info=True)


def main() -> None:
    """Inicia el bot de Telegram."""
    if not BOT_TOKEN:
        logger.error("El BOT_TOKEN no está configurado. Revisa tu archivo .env o variables de entorno.")
        return

    logger.info("Iniciando el bot...")

    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    application.add_handler(CommandHandler("start", start_command_handler))
    application.add_handler(CommandHandler("reddit", reddit_command_handler))   # ← ¡registra Reddit!
    application.add_handler(MessageHandler(filters.FORWARDED & (~filters.COMMAND), handle_forwarded_message))

    logger.info("Bot iniciado y escuchando updates...")
    application.run_polling()

if __name__ == "__main__":
    main()