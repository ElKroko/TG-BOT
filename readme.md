# CodevsBot

**CodevsBot** es un bot de Telegram creado para la comunidad **Codevs**. Permite:

* 🔁 **Reenvío de mensajes** reenviados: los administradores pueden reenviar mensajes de otros chats y el bot los publica en un canal/grupo designado.
* 🌐 **Integración con Reddit**: comando `/reddit <subreddit> [cantidad]` para publicar los posts más populares de un subreddit.

---

## 📂 Estructura del proyecto

```
codevs_bot/
├── config.py           # Variables de entorno y configuración
├── main.py             # Punto de entrada y registro de handlers
├── handlers.py         # Lógica de comandos y reenvío de mensajes
├── fetchers/
│   ├── reddit.py       # Módulo para obtener posts de Reddit (PRAW)
│   └── twitter.py      # (Comentado) Funciones de scraping de Twitter
├── utils/
│   └── formatter.py    # Formateadores de mensajes para Telegram
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación de uso (este archivo)
```

---

## 🚀 Requisitos previos

* Python 3.8 o superior
* Telegram Bot creado con @BotFather
* Cuenta de Reddit con una App (tipo "script")
* Un canal o grupo de Telegram donde el bot tenga permisos de publicación

---

## ⚙️ Instalación

1. **Clona el repositorio**

   ```bash
   git clone https://github.com/tu_usuario/codevs_bot.git
   cd codevs_bot
   ```

2. **Crea un entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   # o
   venv\Scripts\activate       # Windows
   ```

3. **Instala dependencias**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔧 Configuración

1. **Crea un archivo `.env`** en la raíz del proyecto con las siguientes variables:

   ```dotenv
   BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
   ADMIN_IDS=12345678,87654321
   TARGET_CHANNEL_ID=@tu_canal_o_-1001234567890

   REDDIT_CLIENT_ID=TuClientID
   REDDIT_CLIENT_SECRET=TuClientSecret
   REDDIT_USER_AGENT=codevs_bot_v1 by /u/tu_usuario
   ```

2. **Verifica** que `config.py` carga estas variables correctamente.

---

## 🏃 Uso

1. **Inicia el bot**:

   ```bash
   python main.py
   ```

2. **Comandos disponibles** (escribe `/` en el chat con el bot para ver el menú):

   * `/start`  : Ver mensaje de bienvenida.
   * `/reddit <subreddit> [cantidad]` : Publica los posts “hot” de un subreddit.

3. **Reenvío de mensajes**:

   * Reenvía cualquier mensaje de otro chat hacia el bot. Si eres admin, el bot lo publicará en el canal configurado.

---

## 🔄 Desarrollo y extiensión

* Para agregar nuevas fuentes (Twitter, Instagram, Hacker News), crea un nuevo módulo en `fetchers/` y ajusta el `formatter`.
* Registra nuevos comandos importando tu handler en `main.py`.
* Puedes automatizar fetch periódicos usando `apscheduler` o un cron externo.

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. ¡Contribuciones bienvenidas!

---

*Hecho con 💙 por Kroko y la comunidad Codevs*
