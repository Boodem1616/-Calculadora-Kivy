from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


class Calculadora(Screen):
    def __init__(self):
        super().__init__()
        self.numero = ""
        self.primer_numero = 0
        self.operador = ""
        self.name = "calculadora"

        # Contenedor principal vertical.
        pantalla = BoxLayout(orientation="vertical", padding=10, spacing=5)
        self.resultado = MDLabel(
            text="0", halign="right", font_size="32sp",
            size_hint_y=None, height=70
        )
        pantalla.add_widget(self.resultado)

        # Teclado de 4 columnas y 5 filas.
        teclado = GridLayout(cols=4, rows=5, spacing=5, padding=5)
        botones = [
            "C", "DEL", "*", "-",
            "7", "8", "9", "+",
            "4", "5", "6", "=",
            "1", "2", "3", "0",
            ".", "%", "", ""
        ]
        for texto in botones:
            boton = Button(text=texto)
            boton.bind(on_release=self.presionar)
            teclado.add_widget(boton)

        pantalla.add_widget(teclado)
        self.add_widget(pantalla)

    def presionar(self, boton):
        texto = boton.text

        if texto.isdigit() or texto == ".":
            if texto == "." and "." in self.numero:
                return
            self.numero += texto
            self.resultado.text = self.numero
        elif texto == "C":
            self.limpiar()
        elif texto == "DEL":
            self.borrar_digito()
        elif texto in "+-*/":
            self.primer_numero = float(self.numero or 0)
            self.operador = texto
            self.numero = ""
        elif texto == "=":
            self.calcular()
        elif texto == "%":
            self.porcentaje()

    def calcular(self):
        segundo_numero = float(self.numero or 0)

        if self.operador == "+":
            respuesta = self.primer_numero + segundo_numero
        elif self.operador == "-":
            respuesta = self.primer_numero - segundo_numero
        elif self.operador == "*":
            respuesta = self.primer_numero * segundo_numero
        elif self.operador == "/":
            if segundo_numero == 0:
                self.resultado.text = "Error"
                self.limpiar_numero()
                return
            respuesta = self.primer_numero / segundo_numero
        else:
            return

        if respuesta.is_integer():
            self.numero = str(int(respuesta))
        else:
            self.numero = str(respuesta)
        self.resultado.text = self.numero

    def limpiar_numero(self):
        self.numero = ""

    def borrar_digito(self):
        self.numero = self.numero[:-1]
        self.resultado.text = self.numero or "0"

    def porcentaje(self):
        self.numero = str(float(self.numero or 0) / 100)
        self.resultado.text = self.numero

    def limpiar(self):
        self.numero = ""
        self.primer_numero = 0
        self.operador = ""
        self.resultado.text = "0"


class Aplicacion(MDApp):
    def build(self):
        Window.size = (400, 600)
        return Calculadora()


Aplicacion().run()
