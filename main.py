import telebot
import random
import datetime
import json
import os
import threading
import time
import schedule
import urllib.parse
import urllib.request
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReactionTypeEmoji
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from PIL import Image, ImageDraw, ImageFont

import ast
token = "a token"
bot = telebot.TeleBot(token)

DATA_FILE = "user_data.json"

# ---------------- LOAD USER DATA ----------------

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        user_data = json.load(f)
else:
    user_data = {}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False)

# ---------------- DAILY WELCOME ----------------

def check_daily_welcome(message):
    user_id = str(message.from_user.id)
    today = str(datetime.date.today())

    if user_id not in user_data:
        user_data[user_id] = {"last_seen": ""}

    if user_data[user_id]["last_seen"] != today:
        user_data[user_id]["last_seen"] = today
        save_data()

        username = message.from_user.username
        name = f"@{username}" if username else message.from_user.first_name

        bot.send_message(message.chat.id, f"Welcome back {name}! 🎉")

# ---------------- DATA ----------------

jokes = [
    "Why did the chicken cross the road? To get to the other side!",
    "What do you call cheese that isn’t yours? Nacho cheese.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet."
]

jokesRu = [
    "Почему курица перешла дорогу? Чтобы попасть на другую сторону!",
    "Как называется сыр, который не твой? Начо-сыр."
]
coin_en = ["Heads", "Tails"]
coin_ru = ["Орёл", "Решка"]

yes_no_questions = [
    "Should I drink more water today?",
    "Should I go for a walk right now?",
    "Should I finish my work before gaming?",
    "Is today a good day to try something new?"
]

# ---------------- BUTTON QUESTION ----------------

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Yes", callback_data="cb_yes"),
        InlineKeyboardButton("No", callback_data="cb_no"),
        InlineKeyboardButton("Maybe", callback_data="cb_maybe")
    )
    return markup

@bot.callback_query_handler(func=lambda call: call.data in ["cb_yes", "cb_no", "cb_maybe"])
def callback_query(call):

    bot.answer_callback_query(call.id)

    responses = {
        "cb_yes": "Answer is: Yes",
        "cb_no": "Answer is: No",
        "cb_maybe": "Answer is: Maybe"
    }

    bot.send_message(call.message.chat.id, responses[call.data])

@bot.message_handler(commands=['question'])
def question_command(message):

    bot.send_message(
        message.chat.id,
        random.choice(yes_no_questions),
        reply_markup=gen_markup()
    )

# ---------------- SCHEDULED MESSAGES ----------------

def send_scheduled_message(chat_id, text):
    bot.send_message(chat_id, text=text)

@bot.message_handler(commands=['set'])
def set_timer(message):

    args = message.text.split(maxsplit=2)

    if len(args) < 3 or not args[1].isdigit():
        bot.reply_to(message, "Usage: /set <seconds> <message>")
        return

    sec = int(args[1])
    scheduled_text = args[2]

    schedule.clear(message.chat.id)

    schedule.every(sec).seconds.do(
        send_scheduled_message,
        message.chat.id,
        scheduled_text
    ).tag(message.chat.id)

    bot.reply_to(message, f'Sending "{scheduled_text}" every {sec} seconds.')

@bot.message_handler(commands=['unset'])
def unset_timer(message):

    schedule.clear(message.chat.id)
    bot.reply_to(message,"Timer stopped.")

# -------- List of Global disasters --------
global_problems = [
    "Climate change",
    "Poverty",
    "Inequality",
    "War",
    "Disease",
    "Pollution",
    "Deforestation",
    "Overpopulation",
    "Resource depletion",
    "Corruption",
    "Unemployment",
    "Food insecurity",
    "Lack of education",
    "Human rights abuses",
    "Terrorism",
    "Natural disasters",
    "Cybersecurity threats",
    "Mental health crisis",
    "Refugee crisis",
    "Global pandemics",
    "refugee rights",
    "ocean pollution",
    "plastic waste",
    "healthcare",
    "disability rights",
    "LGBTQ+ rights",
    "racial justice",
    "reproductive justice",
    "freedom of speech",
    "children's rights",
    "animal welfare",
    "gender equality",
    "access to clean water",
    "cybersecurity",
    "Disinformation",
    "Freedom of the press",
    "Debt crises",
    "Corruption",
    "Nuclear proliferation",
    "Authoritarianism",
    "Religious extremism",
    "Human trafficking",
    "global cooperation",
    "sustainable development",
]
global_problemsRu = [
    "Изменение климата",
    "Бедность",
    "Неравенство",
    "Война",
    "Болезни",
    "Загрязнение окружающей среды",
    "Вырубка лесов",
    "Перенаселение",
    "Истощение ресурсов",
    "Коррупция",
    "Безработица",
    "Продовольственная нестабильность",
    "Отсутствие образования",
    "Нарушения прав человека",
    "Терроризм",
    "Стихийные бедствия",
    "Угрозы кибербезопасности",
    "Кризис в сфере психического здоровья",
    "Кризис беженцев",
    "Глобальные пандемии",
    "права беженцев",
    "загрязнение океанов",
    "пластиковые отходы",
    "здравоохранение",
    "права людей с инвалидностью",
    "права ЛГБТК+",
    "расовая справедливость",
    "репродуктивная справедливость",
    "свобода слова",
    "права детей",
    "благополучие животных",
    "гендерное равенство",
    "доступ к чистой воде",
    "кибербезопасность",
    "дезинформация",
    "свобода прессы",
    "долговые кризисы",
    "коррупция",
    "распространение ядерного оружия",
    "авторитаризм",
    "религиозный экстремизм",
    "торговля людьми",
    "глобальное сотрудничество",
    "устойчивое развитие",
]
@bot.message_handler(commands=['global_problem'])
def global_problem_command(message):

    problem = random.choice(global_problems)
    bot.reply_to(message, f"One global problem is: {problem}. if you would like to search it you can do /search {problem}")
@bot.message_handler(commands=['global_problemRu'])
def global_problem_commandRu(message):
    problemRu = random.choice(global_problemsRu)
    bot.reply_to(message, f"Одна из глобальных проблем: {problemRu}. Если вы хотите её поискать, используйте /search {problemRu}")


# ---------------- MINI APP ----------------

WEB_URL = "https://ryancherches.com/telegram%20bot/index.html"

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "images", "very tiny image.png")

@bot.message_handler(commands=["image"])
def send_photo(message):
    with open(IMAGE_PATH, "rb") as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=["start"])
def start(message):

    reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard_markup.row(
        KeyboardButton("Start MiniApp", web_app=WebAppInfo(WEB_URL))
    )

    inline_keyboard_markup = InlineKeyboardMarkup()
    inline_keyboard_markup.row(
        InlineKeyboardButton("Start MiniApp", web_app=WebAppInfo(WEB_URL))
    )

    bot.reply_to(
        message,
        "Click the button to start the Mini App",
        reply_markup=inline_keyboard_markup
    )

    bot.send_message(
        message.chat.id,
        "Or use the keyboard button",
        reply_markup=reply_keyboard_markup
    )

# ---------------- FONT ----------------

try:
    font = ImageFont.truetype("arial.ttf",70)
except:
    font = ImageFont.load_default()

# ---------------- GIF EFFECTS ----------------

def rainbow_gif(text):

    frames=[]
    colors=["red","orange","yellow","green","blue","purple"]

    for shift in range(12):

        img=Image.new("RGB",(900,300),"white")
        draw=ImageDraw.Draw(img)

        x=80
        y=100

        for i,letter in enumerate(text):
            draw.text((x,y),letter,font=font,fill=colors[(i+shift)%len(colors)])
            x+=45

        frames.append(img)

    path="rainbow.gif"

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0
    )

    return path


def neon_gif(text):

    frames=[]

    for glow in range(1,8):

        img=Image.new("RGB",(900,300),"black")
        draw=ImageDraw.Draw(img)

        for offset in range(glow):
            draw.text((100-offset,100-offset),text,font=font,fill="cyan")

        draw.text((100,100),text,font=font,fill="white")

        frames.append(img)

    path="neon.gif"

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0
    )

    return path


def sparkle_gif(text):

    frames=[]

    for frame in range(12):

        img=Image.new("RGB",(900,300),"white")
        draw=ImageDraw.Draw(img)

        draw.text((100,100),text,font=font,fill="purple")

        for i in range(25):
            draw.text(
                (random.randint(0,900),random.randint(0,300)),
                "✨",
                font=font,
                fill="gold"
            )

        frames.append(img)

    path="sparkle.gif"

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0
    )

    return path


def explode_gif(text):

    frames=[]

    for frame in range(10):

        img=Image.new("RGB",(900,300),"white")
        draw=ImageDraw.Draw(img)

        draw.text((100,100),text,font=font,fill="red")

        for i in range(frame*8):
            draw.text(
                (random.randint(0,900),random.randint(0,300)),
                "💥",
                font=font,
                fill="orange"
            )

        frames.append(img)

    path="explode.gif"

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0
    )

    return path

# ---------------- MINI APP DATA ----------------

@bot.message_handler(content_types=['web_app_data'])
def web_app(message):

    data=json.loads(message.web_app_data.data)

    text=data.get("message","Hello")
    effect=data.get("effect","rainbow")

    if effect=="rainbow":
        path=rainbow_gif(text)

    elif effect=="neon":
        path=neon_gif(text)

    elif effect=="sparkle":
        path=sparkle_gif(text)

    elif effect=="explode":
        path=explode_gif(text)

    else:
        path=rainbow_gif(text)

    with open(path,"rb") as gif:
        bot.send_animation(message.chat.id,gif)

# ---------------- HEH COMMAND ----------------

@bot.message_handler(commands=['heh'])
def handle_heh(message):

    try:
        count=int(message.text.split()[1])
    except:
        count=5

    bot.reply_to(message,"he"*count)

# ---------------- CHAT RESPONSES ----------------

def is_command(message):
    return bool(message.text) and message.text.strip().startswith("/")

def get_command_name(message):
    text = (message.text or "").strip()
    if not text.startswith("/"):
        return ""
    command = text.split()[0][1:]
    if "@" in command:
        command = command.split("@", 1)[0]
    return command.lower()

KNOWN_COMMANDS = {
    "start",
    "image",
    "question",
    "set",
    "unset",
    "joke",
    "rujoke",
    "coinflip",
    "coinflipru",
    "heh",
    "math",
    "search",
    "help",
    "global_problem",
    "global_problemru"
}

def eval_math_expression(expression):
    try:
        node = ast.parse(expression, mode="eval")
    except SyntaxError:
        return None

    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
        ast.FloorDiv,
        ast.UAdd,
        ast.USub,
        ast.Constant
    )

    for subnode in ast.walk(node):
        if not isinstance(subnode, allowed_nodes):
            return None
        if isinstance(subnode, ast.Constant) and not isinstance(subnode.value, (int, float)):
            return None

    try:
        result = eval(compile(node, "<math>", "eval"), {"__builtins__": {}})
    except Exception:
        return None

    return result

def do_math(message, expression):
    if not expression:
        bot.reply_to(message, "Usage: /math <expression> or math <expression>")
        return

    result = eval_math_expression(expression)
    if result is None:
        bot.reply_to(message, "Invalid expression. Example: /math 5*5")
        return

    bot.reply_to(message, str(result))

def do_search(message, query):
    if not query:
        bot.reply_to(message, "Usage: /search <query> or search <query>")
        return

    try:
        allowed_labels = [".gov", ".edu", ".org", ".int", ".mil"]

        ddg_url = "https://duckduckgo.com/lite/?" + urllib.parse.urlencode({"q": query})
        request = urllib.request.Request(
            ddg_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")

        raw_links = re.findall(r'href="([^"]+)"', html)
        links = []
        for link in raw_links:
            if link.startswith("/l/?"):
                link = "https://duckduckgo.com" + link
            if "duckduckgo.com/l/?" in link:
                parsed = urllib.parse.urlparse(link)
                q = urllib.parse.parse_qs(parsed.query)
                uddg = q.get("uddg", [""])[0]
                if uddg:
                    link = urllib.parse.unquote(uddg)
                else:
                    continue
            if link.startswith("http://") or link.startswith("https://"):
                links.append(link)

        if not links:
            bot.reply_to(message, "No results found.")
            return

        selected_url = None
        for link in links:
            parsed = urllib.parse.urlparse(link)
            host = parsed.netloc.lower()
            if not host:
                continue
            for label in allowed_labels:
                if host.endswith(label) or (label + ".") in host:
                    selected_url = link
                    break
            if selected_url:
                break

        if not selected_url:
            bot.reply_to(message, "No factual-domain results found.")
            return

        bot.reply_to(message, selected_url)
    except Exception:
        bot.reply_to(message, "Search failed. Please try again later.")

@bot.message_handler(commands=["math"])
def math_command(message):
    args = message.text.split(maxsplit=1)
    expression = args[1] if len(args) > 1 else ""
    do_math(message, expression)

@bot.message_handler(commands=["help"])
def help_command(message):
    commands = [
        "/start - Start the mini app buttons",
        "/image - Send an image",
        "/question - Ask a yes/no/maybe question",
        "/set <seconds> <message> - Repeating timer",
        "/unset - Stop the timer",
        "/joke - Tell a joke",
        "/rujoke - Tell a Russian joke",
        "/coinflip - Flip a coin",
        "/coinflipru - Flip a coin (RU)",
        "/heh [count] - Repeat he",
        "/math <expression> - Calculate math",
        "/search <query> - Find an article link",
        "/help - Show this help message",
        "/global_problem - Get a random global problem to search",
        "/global_problemRu - Получить случайную глобальную проблему для поиска"
    ]

    bot.reply_to(message, "Commands:\n" + "\n".join(commands))

@bot.message_handler(commands=["search"])
def search_command(message):
    args = message.text.split(maxsplit=1)
    query = args[1].strip() if len(args) > 1 else ""
    do_search(message, query)


@bot.message_handler(commands=["joke", "rujoke", "coinflip", "coinflipru"])
def handle_text_commands(message):

    command = message.text.split()[0].lstrip("/").lower()

    if command == "joke":
        bot.reply_to(message, random.choice(jokes))
        return

    if command == "rujoke":
        bot.reply_to(message, random.choice(jokesRu))
        return

    if command == "coinflip":
        bot.reply_to(message, random.choice(coin_en))
        return

    if command == "coinflipru":
        bot.reply_to(message, random.choice(coin_ru))
        return



@bot.message_handler(content_types=["text"])
def handle_message(message):

    raw_text = (message.text or "").strip()
    text = raw_text.lower()

    check_daily_welcome(message)

    if is_command(message):
        command = get_command_name(message)
        if command in KNOWN_COMMANDS:
            return
        bot.reply_to(message, "Unknown command. Use /help to see all commands.")
        return

    if text == "math" or text.startswith("math "):
        parts = raw_text.split(maxsplit=1)
        expression = parts[1] if len(parts) > 1 else ""
        do_math(message, expression)
        return

    if text == "search" or text.startswith("search "):
        parts = raw_text.split(maxsplit=1)
        query = parts[1] if len(parts) > 1 else ""
        do_search(message, query)
        return

    if text=="joke":
        bot.reply_to(message,random.choice(jokes))
        return

    elif text=="rujoke":
        bot.reply_to(message,random.choice(jokesRu))
        return

    elif text=="coinflip":
        bot.reply_to(message,random.choice(coin_en))
        return

    elif text=="coinflipru":
        bot.reply_to(message,random.choice(coin_ru))
        return

    elif text in ["hi","hello"]:
        bot.reply_to(message,"Hello 👋")
        return

    elif "how are you" in text:
        bot.reply_to(message,"Running smoothly ⚡")
        return

    elif text=="bye":
        bot.reply_to(message,"Bye 👋")
        return

    elif "thanks" in text:
        bot.reply_to(message,"You're welcome 😊")
        return
    else:
        bot.reply_to(message, "I didn't understand that. Try /help.")
        return

# ---------------- BOT LOOP ----------------

print("Bot is running...")


def schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


threading.Thread(
    target=schedule_loop,
    daemon=True
).start()

bot.infinity_polling()


