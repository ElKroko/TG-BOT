import logging
from telegram import Update, Message, Chat # Añadido Message y Chat
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown # Sigue siendo útil para la cabecera del reenvío
from telegram import User
from fetchers.reddit import fetch_subreddit_posts
from utils.formatter import format_reddit_posts

from fetchers.hackernews import fetch_hn_posts
from utils.formatter import format_hn_posts

from config import ADMIN_IDS, TARGET_CHANNEL_ID
# Comentamos las importaciones de Twitter ya que esa funcionalidad está en pausa
# from fetchers.twitter import fetch_tweet_data
# from utils.formatter import format_tweet_message

logger = logging.getLogger(__name__)

async def testdaily_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ADMIN_IDS:
        return await update.message.reply_text("🚫 No tienes permiso.")
    await send_daily_news(context)
    await update.message.reply_text("✅ Noticias de prueba enviadas.")


async def my_roles_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    role = context.bot_data.get("user_roles", {}).get(update.effective_user.id)
    await update.message.reply_text(
        f"Tu rol actual: *{role or 'sin rol asignado'}*",
        parse_mode="Markdown"
    )


async def role_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Asigna un rol interno al usuario: /iamdev, /iamux, /iamcrypto."""
    cmd = update.message.text.lower().strip().lstrip("/")

    rol_map = {
        "iamdev":    "Desarrollador Frontend/Backend",
        "iamux":     "Diseñador UI/UX",
        "iamcrypto": "Entusiasta de Cripto y Trading"
    }
    if cmd not in rol_map:
        return

    role = rol_map[cmd]
    user = update.effective_user
    # Guarda en bot_data
    roles = context.bot_data.setdefault("user_roles", {})
    roles[user.id] = role

    await update.message.reply_text(
        f"✅ {user.full_name}, ahora estás registrado como *{role}*.",
        parse_mode="Markdown"
    )

async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía un DM de bienvenida cuando alguien entra al grupo."""
    for member in update.message.new_chat_members:
        try:
            # Envía mensaje privado
            await context.bot.send_message(
                chat_id=member.id,
                text=(
                    f"👋 ¡Bienvenido/a, {member.full_name}!\n\n"
                    "Este es el grupo oficial de Codevs. Te invito a:\n"
                    "• Leer las reglas en el canal fijado.\n"
                    "• Pasar por /help para ver comandos útiles.\n"
                    "• Presentarte con /iamdev, /iamux, /iamcrypto si quieres asignarte un rol."
                )
            )
        except Exception:
            # Si no se puede mandar PM (privacidad), saluda en el grupo
            await update.message.reply_text(
                f"👋 ¡Bienvenido/a, {member.full_name}! "
                "No pude mandarte un privado, pero aquí estamos para ayudarte."
            )


async def send_daily_news(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Callback que envía las noticias diarias al canal."""
    # 1) Reddit
    reddit_posts = fetch_subreddit_posts("python", 3)
    reddit_msg   = format_reddit_posts(reddit_posts, "python")

    # 2) Hacker News
    hn_posts  = fetch_hn_posts(5)
    hn_msg    = format_hn_posts(hn_posts, 5)

    # 3) Publicar ambos bloques
    await context.bot.send_message(
        chat_id=TARGET_CHANNEL_ID,
        text="🗞️ *Noticias diarias – CodevsBot* 🕘\n\n" + reddit_msg + "\n\n" + hn_msg,
        parse_mode="Markdown"
    )

async def hackernews_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja /hackernews para traer los posts top de HN."""
    user = update.effective_user
    if user.id not in ADMIN_IDS:
        await update.message.reply_text("🚫 No tienes permiso para usar este comando.")
        return

    args = context.args
    limit = int(args[0]) if args and args[0].isdigit() else 5

    posts = fetch_hn_posts(limit)
    message_text = format_hn_posts(posts, limit)

    await context.bot.send_message(
        chat_id=TARGET_CHANNEL_ID,
        text=message_text,
        parse_mode="Markdown"
    )
    await update.message.reply_text(f"✅ Publicados {len(posts)} posts de Hacker News.")



# --- INICIO: FUNCIONALIDAD DE TWITTER (COMENTADA POR AHORA) ---
# async def agregar_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Maneja el comando /agregar."""
#     user = update.effective_user
#     if user.id not in ADMIN_IDS:
#         await update.message.reply_text("🚫 No tienes permiso para usar este comando.")
#         logger.warning(f"Intento de acceso no autorizado al comando /agregar por el usuario {user.id} ({user.username}).")
#         return
#
#     if not context.args:
#         await update.message.reply_text("Por favor, proporciona una URL de Twitter después del comando.\nEjemplo: /agregar https://twitter.com/usuario/status/123")
#         return
#
#     tweet_url = context.args[0]
#
#     if not (tweet_url.startswith("https://twitter.com/") or tweet_url.startswith("https://x.com/")):
#         await update.message.reply_text("⚠️ Solo se soportan URLs de Twitter (twitter.com o x.com) por ahora.")
#         return
#
#     processing_message = await update.message.reply_text("🔄 Procesando tweet, por favor espera...")
#
#     # tweet_data = await fetch_tweet_data(tweet_url) # Problemas con snscrape/SSL
#     tweet_data = None # Simulación para que no falle si se descomenta
#
#     if not tweet_data:
#         await processing_message.edit_text("❌ No se pudo procesar el tweet (función temporalmente deshabilitada). Verifica la URL o inténtalo más tarde.")
#         # logger.error(f"Fallo al obtener datos del tweet para la URL: {tweet_url}") # Comentado
#         return
#
#     # formatted_message = format_tweet_message(tweet_data) # Comentado
#     formatted_message = "Contenido del tweet (función temporalmente deshabilitada)" # Simulación
#
#     try:
#         await context.bot.send_message(
#             chat_id=TARGET_CHANNEL_ID,
#             text=formatted_message,
#             parse_mode=ParseMode.MARKDOWN_V2,
#             disable_web_page_preview=False
#         )
#         await processing_message.edit_text("✅ ¡Tweet publicado en el canal! (simulado)")
#         # logger.info(f"Tweet de {tweet_data['author']} publicado en {TARGET_CHANNEL_ID} por {user.username}.") # Comentado
#     except Exception as e:
#         await processing_message.edit_text(f"❌ Error al publicar en el canal: {escape_markdown(str(e), version=2)}")
#         logger.error(f"Error al enviar mensaje al canal {TARGET_CHANNEL_ID}: {e}", exc_info=True)
# --- FIN: FUNCIONALIDAD DE TWITTER (COMENTADA POR AHORA) ---

async def start_command_handler(update, context):
    await update.message.reply_text(
        "👋 ¡Hola! Soy *CodevsBot*.\n\n"
        "• /help – ver comandos\n"
        "• /reddit – posts de Reddit\n"
        "• /hackernews – artículos de Hacker News\n"
        "• /myroles – tu rol\n"
        "• /testdaily – noticias ahora\n\n"
        "Y puedes reenviar mensajes para publicarlos en el canal (solo admins).",
        parse_mode=ParseMode.MARKDOWN
    )

async def help_command_handler(update, context):
    await update.message.reply_text(
        "*CodevsBot – Ayuda* 💡\n\n"
        "/start – bienvenida\n"
        "/help – esta ayuda\n"
        "/reddit <subreddit> [n]\n"
        "/hackernews [n]\n"
        "/myroles\n"
        "/testdaily\n"
        "Reenvío de mensajes (admins)",
        parse_mode=ParseMode.MARKDOWN
    )

# --- INICIO: NUEVA FUNCIONALIDAD DE REENVÍO DE MENSAJES DE TELEGRAM ---
def get_forward_origin_info(message: Message) -> tuple[str | None, int | None, str | None]:
    """
    Extrae información sobre el origen de un mensaje reenviado.
    Retorna (nombre_display, id_origen, tipo_origen ('user', 'channel', 'hidden_user_or_anonymous_group_admin', 'unknown'))
    """
    origin = message.forward_origin
    if not origin:
        return "Fuente Desconocida", None, "unknown"

    if origin.type == "user":
        user: User = origin.sender_user
        name = user.full_name
        if user.username:
            name += f" (@{user.username})"
        return name, user.id, "user"
    elif origin.type == "channel":
        chat: Chat = origin.chat
        message_id = origin.message_id # ID del mensaje original en el canal
        name = chat.title
        if chat.username:
            name = f"@{chat.username}"
        # Podríamos querer el link al mensaje específico si es un canal público
        # if chat.username and message_id:
        #     name += f"/{message_id}" # ej: @canal/123 (no es un link directo clickable en markdown simple)
        return name, chat.id, "channel"
    elif origin.type == "hidden_user":
        return origin.sender_user_name, None, "hidden_user_or_anonymous_group_admin"
    
    return "Fuente Desconocida", None, "unknown"


async def handle_forwarded_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja mensajes reenviados al bot."""
    message = update.effective_message
    
    if not message.forward_origin:
        # Esto no debería ocurrir si el filtro es filters.FORWARDED
        logger.debug("Mensaje recibido no es un reenvío (inesperado con filters.FORWARDED).")
        return

    user_who_forwarded = update.effective_user
    if user_who_forwarded.id not in ADMIN_IDS: # Restricción de admin
        await message.reply_text("🚫 No tienes permiso para usar esta función de reenvío.")
        logger.warning(f"Intento de reenvío no autorizado por {user_who_forwarded.id} ({user_who_forwarded.username}).")
        return

    origin_name, origin_id, origin_type = get_forward_origin_info(message)
    
    header_parts = ["➡️ Mensaje reenviado"]
    link_to_origin = None

    if origin_name:
        escaped_origin_name = escape_markdown(origin_name, version=2)
        if origin_type == "user" and origin_id:
            # tg://user?id=<user_id> es un deep link al perfil del usuario
            link_to_origin = f" de [{escaped_origin_name}](tg://user?id={origin_id})"
        elif origin_type == "channel":
            # Para canales públicos con @username
            if message.forward_origin and message.forward_origin.chat and message.forward_origin.chat.username:
                # message.forward_origin.chat.username NO incluye el @
                link_to_origin = f" del canal @{message.forward_origin.chat.username}"
                # Si quisiéramos link al mensaje específico (más complejo de asegurar que funcione en todos los clientes):
                # if message.forward_origin.message_id:
                #    link_to_origin += f"/{message.forward_origin.message_id}"
            # Para canales con título pero sin @username (privados)
            elif message.forward_origin and message.forward_origin.chat and message.forward_origin.chat.title:
                channel_title_escaped = escape_markdown(message.forward_origin.chat.title, version=2)
                link_to_origin = f" del canal \"{channel_title_escaped}\""
            else: # Fallback si no hay @username ni título claro (poco probable para canales)
                 link_to_origin = f" de {escaped_origin_name}"
        else: # hidden_user, unknown, etc.
            link_to_origin = f" de {escaped_origin_name}"
    
    if link_to_origin:
        header_parts.append(link_to_origin)
    header_parts.append(":")
    header_text = "".join(header_parts)


    try:
        # Enviar la cabecera primero
        await context.bot.send_message(
            chat_id=TARGET_CHANNEL_ID,
            text=header_text,
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True # Evitar preview para el link tg://
        )

        # Copiar el mensaje original que fue reenviado al bot
        await context.bot.copy_message(
            chat_id=TARGET_CHANNEL_ID,
            from_chat_id=message.chat_id,
            message_id=message.message_id,
        )
        
        await message.reply_text("✅ Mensaje reenviado al canal.")
        logger.info(f"Mensaje reenviado (origen: {origin_name or 'desconocido'}) al canal {TARGET_CHANNEL_ID} por {user_who_forwarded.username}.")

    except Exception as e:
        error_message_escaped = escape_markdown(str(e), version=2)
        logger.error(f"Error al reenviar mensaje al canal {TARGET_CHANNEL_ID}: {e}", exc_info=True)
        await message.reply_text(f"❌ Error al reenviar el mensaje: {error_message_escaped}")

async def reddit_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /reddit para obtener posts de un subreddit."""
    user = update.effective_user
    if user.id not in ADMIN_IDS:
        await update.message.reply_text("🚫 No tienes permiso para usar este comando.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("❗️ Uso: /reddit <subreddit> [cantidad]")
        return

    subreddit = args[0].lstrip("r/")
    limit = int(args[1]) if len(args) > 1 and args[1].isdigit() else 3

    posts = fetch_subreddit_posts(subreddit, limit)
    message_text = format_reddit_posts(posts, subreddit)
    await context.bot.send_message(
        chat_id=TARGET_CHANNEL_ID,
        text=message_text,
        parse_mode="Markdown"
    )
    await update.message.reply_text(f"✅ Publicados {len(posts)} posts de r/{subreddit}.")



# --- FIN: NUEVA FUNCIONALIDAD DE REENVÍO DE MENSAJES DE TELEGRAM ---