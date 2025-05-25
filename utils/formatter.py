from telegram.helpers import escape_markdown

def format_tweet_message(tweet_data: dict) -> str:
    """
    Formatea los datos del tweet para ser enviados a Telegram.
    Usa MarkdownV2.
    """
    if not tweet_data or not all(k in tweet_data for k in ["author", "text", "url"]):
        return "Error: Datos del tweet incompletos o no disponibles."

    author = escape_markdown(tweet_data['author'], version=2)
    text = escape_markdown(tweet_data['text'], version=2)
    url = escape_markdown(tweet_data['url'], version=2) # Aunque la URL no suele necesitar escape si es para link

    # El formato de link en MarkdownV2 es [texto visible](URL)
    # Las URLs en sí mismas no necesitan ser escapadas si se usan dentro de `()` de un link.
    # Sin embargo, el texto visible sí necesita escape.
    
    formatted_message = (
        f"🧠 Tweet destacado por @{author}\n\n"
        f"\"{text}\"\n\n"
        f"🔗 Ver tweet: [{escape_markdown(tweet_data['url'], version=2)}]({tweet_data['url']})" # La URL en () no se escapa
    )
    return formatted_message

def format_reddit_posts(posts, subreddit_name):
    if not posts:
        return f"⚠️ No encontré posts en r/{subreddit_name}."
    lines = [f"📰 *Top posts de r/{subreddit_name}*:\n"]
    for p in posts:
        lines.append(
            f"• *{p['title']}*  \n"
            f"  por u/{p['author']} · 👍 {p['score']}  \n"
            f"  🔗 {p['url']}\n"
        )
    return "\n".join(lines)


if __name__ == '__main__':
    # Ejemplo de uso
    sample_data = {
        "author": "ai_news",
        "text": "OpenAI lanza una nueva arquitectura para audio generativo... ¡Es increíble!",
        "url": "https://twitter.com/ai_news/status/123456"
    }
    message = format_tweet_message(sample_data)
    print("Mensaje formateado:")
    print(message)

    sample_data_with_markdown = {
        "author": "test_user",
        "text": "Este es un texto con *estrellas* y _guiones bajos_.",
        "url": "https://example.com/tweet_with_special_chars"
    }
    message_escaped = format_tweet_message(sample_data_with_markdown)
    print("\nMensaje formateado con caracteres especiales escapados:")
    print(message_escaped)