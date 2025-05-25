# CodevsBot

**CodevsBot** es un bot de Telegram para la comunidad **Codevs**, que facilita:

* 🔄 **Reenvío de mensajes** reenviados: administradores pueden reenviar mensajes desde otros chats y el bot los publica en el canal o grupo designado.
* 🌐 **Integración con Reddit**: `/reddit <subreddit> [n]` publica los `n` posts más populares de un subreddit.
* 🚀 **Integración con Hacker News**: `/hackernews [n]` publica los `n` artículos principales de Hacker News.
* 👤 **Roles internos**: `/iamdev`, `/iamux`, `/iamcrypto` asignan un rol; `/myroles` muestra tu rol.
* 🗞️ **Noticias programadas**: envía un resumen diario de noticias a las 09:00 (hora de Santiago) y permite `/testdaily` para envío inmediato.
* 💡 `/help` y `/start` muestran comandos y bienvenida.

---

## 📂 Estructura del proyecto

```
codevs_bot/
├── config.py           # Configuración y variables de entorno
├── main.py             # Punto de entrada, handlers y jobs
├── handlers.py         # Lógica de comandos, moderación y programación
├── fetchers/
│   ├── reddit.py       # Obtención de posts de Reddit (PRAW)
│   ├── hackernews.py   # Lectura de RSS de Hacker News
│   └── twitter.py      # (En pausa) scraping de Twitter
├── utils/
│   └── formatter.py    # Formateadores de mensajes para Telegram
├── requirements.txt    # Dependencias del proyecto
├── run_bot.bat         # Script para arrancar en Windows con bucle
└── README.md           # Documentación de uso (este archivo)
```

---

## 🚀 Requisitos previos

* Python 3.8+
* Bot de Telegram creado con @BotFather
* Aplicación de Reddit (tipo "script") en [https://reddit.com/prefs/apps](https://reddit.com/prefs/apps)
* Canal o grupo de Telegram donde el bot tenga permisos de publicación

---

## ⚙️ Instalación rápida

1. **Clona el repositorio**

   ```bash
   ```

git clone [https://github.com/tu\_usuario/codevs\_bot.git](https://github.com/tu_usuario/codevs_bot.git)
cd codevs\_bot

````

2. **Crea y activa el entorno virtual**
   ```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
````

3. **Instala dependencias**

   ```bash
   ```

pip install -r requirements.txt

````

---

## 🔧 Configuración (`.env`)

Crea un archivo `.env` en la raíz con:

```dotenv
BOT_TOKEN=tu_telegram_bot_token
ADMIN_IDS=12345678,87654321
TARGET_CHANNEL_ID=@tu_canal_o_-1001234567890

REDDIT_CLIENT_ID=TuClientID
REDDIT_CLIENT_SECRET=TuClientSecret
REDDIT_USER_AGENT=codevs_bot_v1 by /u/tu_usuario

SPAM_DOMAIN_BLACKLIST=bit.ly,t.co,dominio-prohibido.com
MAX_LINKS_PER_MESSAGE=2
````

El `config.py` carga estas variables al iniciar.

---

## 🏃 Uso básico

1. **Arranca el bot**

   * En desarrollo:

     ```bash
     python main.py
     ```
   * En Windows como tarea programada: usa `run_bot.bat` y el Programador de Tareas.

2. **Comandos principales**

   * `/start`      – Ver bienvenida rápida
   * `/help`       – Ver ayuda detallada
   * `/reddit <subreddit> [n]` – Publicar top `n` posts de un subreddit
   * `/hackernews [n]` – Publicar top `n` artículos de Hacker News
   * `/iamdev`, `/iamux`, `/iamcrypto` – Asignarte un rol interno
   * `/myroles`    – Ver tu rol asignado
   * `/testdaily`  – Enviar al canal las noticias de prueba inmediatamente
   * *Reenvío de mensajes* – Reenvía mensajes de otros chats para publicarlos (solo admins)

---

## ✨ Ejecución en Windows (segundo plano)

1. **`run_bot.bat`**

   ```bat
   @echo off
   :start
   cd /d F:\Codes\CODEVS\TG-BOT
   call venv\Scripts\activate
   python main.py >> bot.log 2>&1
   timeout /t 10 /nobreak
   goto start
   ```

2. **Programador de Tareas**

   * Crea una tarea "CodevsBot" que ejecute `run_bot.bat` al iniciar sesión o al arrancar.
   * Marca “Ejecutar aunque el usuario no haya iniciado sesión” y “Reiniciar la tarea si falla”.

---

## 🏗️ Desarrollo y extensiones

* **Añadir nuevas fuentes**: crea módulos en `fetchers/` y formateadores en `utils/formatter.py`.
* **Comandos extra**: registra nuevos handlers en `main.py` con `CommandHandler`.
* **JobQueue**: usa `app.job_queue.run_daily(...)` para programar envíos periódicos.

---

## 📝 Licencia

MIT. ¡Contribuciones bienvenidas!

*Hecho con 💙 por Kroko y la comunidad Codevs*
