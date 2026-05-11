from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.label import MDLabel


class MyApp(MDApp):

    def build(self):
        screen = Screen()

        # Menú
        menu_items = [
            {"text": "Opción 1"},
            {"text": "Opción 2"},
            {"text": "Opción 3"},
        ]

        menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

        # Barra de herramientas
        toolbar = MDToolbar(
            title="Mi aplicación",
            left_action_items=[
                ["language-python", lambda x: None],
            ],
            right_action_items=[
                ["settings", lambda x: None],
            ],
            pos_hint={"top": 1}
        )

        # Pantalla de inicio
        home_screen = Screen()
        home_screen.add_widget(
            MDLabel(
                text="Bienvenido a mi aplicación",
                halign="center",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
        )

        # Agregar widgets a la pantalla
        screen.add_widget(toolbar)
        screen.add_widget(home_screen)

        return screen


if __name__ == "__main__":
    MyApp().run()