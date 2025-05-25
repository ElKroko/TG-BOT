import logging
from telegram import BotCommand
from telegram.constants import ParseMode
from telegram.ext import Application, ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, TARGET_CHANNEL_ID
from datetime import time, timedelta
from zoneinfo import ZoneInfo
from handlers import (
    start_command_handler,
    handle_forwarded_message,
    reddit_command_handler,
    hackernews_command_handler,   # <-- nuevo import
    help_command_handler,
    send_daily_news,
    welcome_new_members,
    role_command_handler,
    my_roles_handler,
    testdaily_handler
)

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
        BotCommand("start", "🚀 Bienvenida"),
        BotCommand("help", "💡 Ayuda"),
        BotCommand("reddit", "🌐 Posts de Reddit"),
        BotCommand("hackernews", "🚀 Artículos HN"),
        BotCommand("myroles", "👤 Ver tu rol"),
        BotCommand("testdaily", "🗞️ Noticias de prueba")
    ]
    try:
        await application.bot.set_my_commands(bot_commands)
        logger.info("Comandos del bot configurados en el menú.")
    except Exception as e:
        logger.error(f"Error al configurar los comandos del bot: {e}", exc_info=True)

    
    bot_description = (
         "Soy CodevsBot, tu asistente de Codevs. ✨\n\n"
            "• Reenvía mensajes para compartirlos.\n"
            "• /reddit para posts de Reddit.\n"
            "• /hackernews para HN.\n"
            "• /myroles para tu rol.\n"
            "• /testdaily para prueba de noticias."
    )
    try:
        await application.bot.set_my_description(description=bot_description)
        logger.info("Descripción del bot configurada.")
    except Exception as e:
        logger.error(f"Error al configurar la descripción del bot: {e}", exc_info=True)
    
    await application.bot.send_message(
        chat_id=TARGET_CHANNEL_ID,
        text="🤖 *CodevsBot está en línea y listo para compartir novedades!*",
        parse_mode=ParseMode.MARKDOWN
    )
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

    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # —— AÑADIR AQUI LOS HANDLERS —— 
    application.add_handler(CommandHandler("start", start_command_handler))
    application.add_handler(CommandHandler("help", help_command_handler))

    application.add_handler(CommandHandler("reddit", reddit_command_handler))   # ← ¡registra Reddit!
    application.add_handler(CommandHandler("hackernews", hackernews_command_handler))
    application.add_handler(CommandHandler("myroles", my_roles_handler))
    application.add_handler(CommandHandler("testdaily", testdaily_handler))

    # Bienvenida, roles y reenvío
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members))
    application.add_handler(CommandHandler("iamdev", role_command_handler))
    application.add_handler(CommandHandler("iamux",  role_command_handler))
    application.add_handler(CommandHandler("iamcrypto", role_command_handler))
    application.add_handler(MessageHandler(filters.FORWARDED & (~filters.COMMAND), handle_forwarded_message))
    
    # Jobs de prueba y diario
    # Se ejecuta todos los días a las 09:00 (hora de Santiago)
    application.job_queue.run_daily(
        send_daily_news,
        time=time(hour=9, minute=0, tzinfo=ZoneInfo("America/Santiago"))
    )
    
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()