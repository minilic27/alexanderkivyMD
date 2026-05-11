from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivy.clock import Clock
import sqlite3
from datetime import datetime

# ================== DATABASE ==================

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
        self.cursor.execute("INSERT INTO notas VALUES(NULL,?,?,?)", (user,score,fecha))
        self.conn.commit()

    def get_last(self, user):
        self.cursor.execute("SELECT calificacion FROM notas WHERE usuario=?", (user,))
        data = self.cursor.fetchall()
        return data[-1][0] if data else 0

# ================== DATA ==================

INTRO = [
    "Python es un lenguaje de programación interpretado, creado para ser fácil de leer y escribir.",
    "Se utiliza en inteligencia artificial, desarrollo web, análisis de datos y automatización.",
    "Su sintaxis es simple, lo que lo hace ideal para principiantes.",
    "En este curso aprenderás desde lo básico hasta lógica aplicada.",
    "Al finalizar deberás aprobar un examen para obtener tu certificación."
]

COURSE = [
    ("Variables","Las variables almacenan información como números, texto o valores booleanos."),
    ("Condicionales","Permiten tomar decisiones usando if, elif y else."),
    ("Bucles","Permiten repetir acciones automáticamente."),
    ("Funciones","Bloques de código reutilizables."),
    ("Listas","Estructuras que almacenan múltiples valores.")
]

QUIZ = [
    ("¿Qué es Python principalmente?",["Un lenguaje de programación","Un sistema operativo","Un juego"],0),
    ("¿Para qué sirven las variables?",["Guardar datos","Mostrar errores","Crear pantallas"],0),
    ("¿Qué hace un 'if'?",["Toma decisiones","Repite código","Guarda archivos"],0),
    ("¿Qué es un bucle?",["Repetición de código","Un error","Un tipo de dato"],0),
    ("¿Qué es una función?",["Bloque reutilizable","Variable especial","Pantalla"],0),
    ("¿Qué tipo de lenguaje es Python?",["Interpretado","Compilado","Binario"],0),
    ("¿Qué estructura guarda varios valores?",["Lista","Variable simple","Clase"],0),
    ("¿Qué hace 'print'?",["Muestra información","Borra datos","Crea funciones"],0),
    ("¿Qué palabra clave crea funciones?",["def","func","create"],0),
    ("¿Python es fácil de aprender?",["Sí","No","Imposible"],0),
]

# ================== APP STATE ==================

class State:
    user = ""

# ================== SCREENS ==================

class Inicio(Screen):
    def __init__(self, app, **k):
        super().__init__(**k)
        self.app = app

        layout = MDBoxLayout(orientation="vertical", padding=30, spacing=20)

        layout.add_widget(MDTopAppBar(title="Curso Python Pro"))

        self.input = MDTextField(hint_text="Escribe tu nombre")

        layout.add_widget(self.input)

        layout.add_widget(MDRaisedButton(
            text="Iniciar",
            on_release=self.enter
        ))

        self.add_widget(layout)

    def enter(self, *args):
        if self.input.text.strip():
            State.user = self.input.text
            self.manager.current = "intro"

# ------------------

class Intro(Screen):
    def __init__(self, app, **k):
        super().__init__(**k)
        self.app = app
        self.i = 0

        layout = MDBoxLayout(orientation="vertical", padding=30, spacing=20)

        self.label = MDLabel(
            halign="center",
            font_style="H6"
        )

        layout.add_widget(self.label)

        self.add_widget(layout)

        Clock.schedule_once(self.animate, 1)

    def animate(self, dt):
        self.show()

    def show(self):
        if self.i < len(INTRO):
            self.label.text = INTRO[self.i]
            self.i += 1
            Clock.schedule_once(lambda dt: self.show(), 2)
        else:
            self.manager.current = "menu"

# ------------------

class Menu(Screen):
    def __init__(self, app, **k):
        super().__init__(**k)
        self.app = app

        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)

        self.info = MDLabel(halign="center")
        layout.add_widget(self.info)

        self.progress = MDProgressBar(value=0)
        layout.add_widget(self.progress)

        layout.add_widget(MDRaisedButton(text="Iniciar Curso", on_release=self.start))

        self.add_widget(layout)

    def on_pre_enter(self):
        self.info.text = f"👤 {State.user}"

    def start(self, *args):
        t = self.manager.get_screen("tema")
        t.reset()
        self.manager.current = "tema"

# ------------------

class Tema(Screen):
    def __init__(self, **k):
        super().__init__(**k)
        self.i = 0

        self.label = MDLabel(halign="center")

        self.add_widget(self.label)

        self.add_widget(MDRaisedButton(text="Siguiente", on_release=self.next))

    def reset(self):
        self.i = 0
        self.show()

    def show(self):
        t = COURSE[self.i]
        self.label.text = f"{t[0]}\n\n{t[1]}"

    def next(self, *args):
        self.i += 1
        if self.i < len(COURSE):
            self.show()
        else:
            q = self.manager.get_screen("quiz")
            q.reset()
            self.manager.current = "quiz"

# ------------------

class Quiz(Screen):
    def __init__(self, app, **k):
        super().__init__(**k)
        self.app = app

        self.i = 0
        self.score = 0

        # CONTENEDOR PRINCIPAL
        layout = MDBoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        # TITULO
        layout.add_widget(MDTopAppBar(title="Examen Final"))

        # PREGUNTA (CENTRADA)
        self.label = MDLabel(
            halign="center",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=100
        )
        layout.add_widget(self.label)

        # CONTENEDOR DE RESPUESTAS (CENTRADO)
        self.answers_box = MDBoxLayout(
            orientation="vertical",
            spacing=15,
            size_hint=(1, None),
            height=250,
            padding=10
        )

        self.buttons = []
        for _ in range(3):
            btn = MDRaisedButton(
                pos_hint={"center_x": 0.5},
                size_hint=(0.8, None),
                height=50,
                on_release=self.answer
            )
            self.buttons.append(btn)
            self.answers_box.add_widget(btn)

        layout.add_widget(self.answers_box)

        self.add_widget(layout)

    def reset(self):
        self.i = 0
        self.score = 0
        self.show()

    def show(self):
        q = QUIZ[self.i]
        self.label.text = q[0]

        for j, op in enumerate(q[1]):
            self.buttons[j].text = op

    def answer(self, btn):
        q = QUIZ[self.i]

        if btn.text == q[1][q[2]]:
            self.score += 1
            self.label.text = "✔ Correcto"
        else:
            self.label.text = "✖ Incorrecto"

        self.i += 1
        Clock.schedule_once(lambda dt: self.next(), 0.6)

    def next(self):
        if self.i < len(QUIZ):
            self.show()
        else:
            self.finish()

    def finish(self):
        self.app.db.save(State.user, self.score)

        if self.score >= 8:
            self.label.text = f"🎉 Aprobado {self.score}/10"
            Clock.schedule_once(lambda dt: setattr(self.manager,"current","certificado"),2)
        else:
            self.label.text = f"❌ {self.score}/10"

# ------------------

class Certificado(Screen):
    def __init__(self, app, **k):
        super().__init__(**k)
        self.app = app

        self.label = MDLabel(
            halign="center",
            font_style="H6"
        )

        self.add_widget(self.label)

        self.add_widget(MDRaisedButton(
            text="Volver al inicio",
            on_release=lambda x: setattr(self.manager,"current","menu")
        ))

    def on_pre_enter(self):
        score = self.app.db.get_last(State.user)

        self.label.text = f"""
🎓 CERTIFICADO OFICIAL 🎓

Se certifica que:

{State.user}

Ha completado el curso de Python

Calificación final: {score}/10

Estado: APROBADO ✔

_________________________
Firma del sistema educativo
        """

# ================== APP ==================

class ProApp(MDApp):
    def build(self):
        self.db = Database()

        sm = ScreenManager()

        sm.add_widget(Inicio(self, name="inicio"))
        sm.add_widget(Intro(self, name="intro"))
        sm.add_widget(Menu(self, name="menu"))
        sm.add_widget(Tema(name="tema"))
        sm.add_widget(Quiz(self, name="quiz"))
        sm.add_widget(Certificado(self, name="certificado"))

        return sm

ProApp().run()