from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.clock import Clock
import sqlite3
from datetime import datetime

# ================= DATABASE =================

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("app.db")
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            calificacion INTEGER,
            fecha TEXT
        )
        """)
        self.conn.commit()

    def save(self, user, score):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cursor.execute(
            "INSERT INTO notas VALUES(NULL,?,?,?)",
            (user, score, fecha)
        )
        self.conn.commit()

# ================= DATOS =================

COURSE = [
    ("Variables", "Las variables almacenan información."),
    ("Condicionales", "Permiten tomar decisiones."),
    ("Bucles", "Repiten acciones automáticamente."),
    ("Funciones", "Código reutilizable."),
    ("Listas", "Guardan múltiples valores.")
]

QUIZ = [
    ("¿Qué es Python?", ["Lenguaje", "Juego", "Sistema"], 0),
    ("¿Qué hace un if?", ["Decisión", "Repetición", "Error"], 0),
    ("¿Qué es una lista?", ["Colección", "Pantalla", "Función"], 0),
]

# ================= ESTADO =================

class State:
    user = ""

# ================= PANTALLA LOGIN =================

class Inicio(MDScreen):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        main = MDBoxLayout(
            orientation="vertical",
            padding=30,
            spacing=25
        )

        toolbar = MDTopAppBar(
            title="Hiub Learning",
            elevation=4
        )

        main.add_widget(toolbar)

        card = MDCard(
            orientation="vertical",
            padding=30,
            spacing=20,
            radius=[20],
            elevation=6,
            size_hint=(0.9, None),
            height=350,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        title = MDLabel(
            text="Bienvenido",
            halign="center",
            font_style="H4"
        )

        subtitle = MDLabel(
            text="Curso Profesional de Python",
            halign="center",
            theme_text_color="Secondary"
        )

        self.input = MDTextField(
            hint_text="Ingresa tu nombre",
            helper_text="Escribe tu usuario",
            helper_text_mode="on_focus",
            icon_right="account"
        )

        btn = MDRaisedButton(
            text="INGRESAR",
            pos_hint={"center_x": 0.5},
            on_release=self.enter
        )

        card.add_widget(title)
        card.add_widget(subtitle)
        card.add_widget(self.input)
        card.add_widget(btn)

        main.add_widget(card)

        self.add_widget(main)

    def enter(self, *args):
        if self.input.text.strip():
            State.user = self.input.text
            self.manager.current = "menu"

# ================= MENU =================

class Menu(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        main.add_widget(MDTopAppBar(
            title="Panel Principal"
        ))

        self.user_label = MDLabel(
            halign="center",
            font_style="H5"
        )

        self.progress = MDProgressBar(
            value=0
        )

        card = MDCard(
            orientation="vertical",
            padding=20,
            spacing=20,
            radius=[20],
            elevation=5
        )

        card.add_widget(self.user_label)
        card.add_widget(self.progress)

        btn = MDRaisedButton(
            text="COMENZAR CURSO",
            pos_hint={"center_x": 0.5},
            on_release=self.start_course
        )

        card.add_widget(btn)

        main.add_widget(card)

        self.add_widget(main)

    def on_pre_enter(self):
        self.user_label.text = f"👤 Bienvenido {State.user}"

    def start_course(self, *args):
        tema = self.manager.get_screen("tema")
        tema.reset()
        self.manager.current = "tema"

# ================= TEMAS =================

class Tema(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.index = 0

        self.layout = MDBoxLayout(
            orientation="vertical",
            padding=25,
            spacing=20
        )

        self.layout.add_widget(MDTopAppBar(
            title="Curso Python"
        ))

        self.card = MDCard(
            orientation="vertical",
            padding=30,
            radius=[20],
            elevation=5
        )

        self.title = MDLabel(
            halign="center",
            font_style="H4"
        )

        self.content = MDLabel(
            halign="center"
        )

        self.btn = MDRaisedButton(
            text="SIGUIENTE",
            pos_hint={"center_x": 0.5},
            on_release=self.next_topic
        )

        self.card.add_widget(self.title)
        self.card.add_widget(self.content)
        self.card.add_widget(self.btn)

        self.layout.add_widget(self.card)

        self.add_widget(self.layout)

    def reset(self):
        self.index = 0
        self.show_topic()

    def show_topic(self):
        topic = COURSE[self.index]
        self.title.text = topic[0]
        self.content.text = topic[1]

    def next_topic(self, *args):
        self.index += 1

        if self.index < len(COURSE):
            self.show_topic()
        else:
            quiz = self.manager.get_screen("quiz")
            quiz.reset()
            self.manager.current = "quiz"

# ================= QUIZ =================

class Quiz(MDScreen):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app
        self.index = 0
        self.score = 0

        main = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        main.add_widget(MDTopAppBar(
            title="Examen Final"
        ))

        self.question = MDLabel(
            halign="center",
            font_style="H5"
        )

        main.add_widget(self.question)

        self.buttons = []

        for i in range(3):
            btn = MDRaisedButton(
                text="",
                pos_hint={"center_x": 0.5},
                on_release=self.answer
            )

            self.buttons.append(btn)
            main.add_widget(btn)

        self.add_widget(main)

    def reset(self):
        self.index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        q = QUIZ[self.index]

        self.question.text = q[0]

        for i, option in enumerate(q[1]):
            self.buttons[i].text = option

    def answer(self, btn):

        q = QUIZ[self.index]

        if btn.text == q[1][q[2]]:
            self.score += 1

        self.index += 1

        if self.index < len(QUIZ):
            self.show_question()
        else:
            self.finish()

    def finish(self):

        self.app.db.save(State.user, self.score)

        result = self.manager.get_screen("resultado")
        result.show_result(self.score)

        self.manager.current = "resultado"

# ================= RESULTADO =================

class Resultado(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main = MDBoxLayout(
            orientation="vertical",
            padding=30,
            spacing=30
        )

        main.add_widget(MDTopAppBar(
            title="Resultado"
        ))

        self.label = MDLabel(
            halign="center",
            font_style="H4"
        )

        btn = MDRaisedButton(
            text="VOLVER AL MENU",
            pos_hint={"center_x": 0.5},
            on_release=self.back
        )

        main.add_widget(self.label)
        main.add_widget(btn)

        self.add_widget(main)

    def show_result(self, score):

        if score >= 2:
            self.label.text = f"""
🎓 FELICIDADES

{State.user}

Aprobaste el curso

Puntuación: {score}/3
"""
        else:
            self.label.text = f"""
❌ REPROBADO

Puntuación: {score}/3
"""

    def back(self, *args):
        self.manager.current = "menu"

# ================= APP =================

class HiubApp(MDApp):

    def build(self):

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        self.db = Database()

        sm = MDScreenManager()

        sm.add_widget(Inicio(self, name="inicio"))
        sm.add_widget(Menu(name="menu"))
        sm.add_widget(Tema(name="tema"))
        sm.add_widget(Quiz(self, name="quiz"))
        sm.add_widget(Resultado(name="resultado"))

        return sm

HiubApp().run()
