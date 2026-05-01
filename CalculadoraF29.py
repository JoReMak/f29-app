from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock


def pesos_chilenos(numero):
    numero = int(numero)
    return "$" + f"{numero:,}".replace(",", ".")


class FondoMorado(BoxLayout):

    def _init_(self, **kwargs):
        super()._init_(**kwargs)

        with self.canvas.before:
            Color(0.35, 0.15, 0.55, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class CalculadoraF29(App):

    def build(self):

        root = FondoMorado(orientation="vertical", padding=20, spacing=15)

        titulo = Label(
            text="Calculadora F29",
            font_size=28,
            size_hint=(1, 0.15)
        )

        root.add_widget(titulo)

        grid = GridLayout(
            cols=2,
            spacing=10,
            size_hint=(1, None),
            height=300
        )

        def entrada():
            return TextInput(
                multiline=False,
                size_hint_y=None,
                height=40
            )

        self.debito = entrada()
        self.credito = entrada()
        self.debito_rec = entrada()
        self.credito_rec = entrada()
        self.remanente = entrada()

        grid.add_widget(Label(text="IVA ventas", size_hint_y=None, height=40))
        grid.add_widget(self.debito)

        grid.add_widget(Label(text="IVA compras", size_hint_y=None, height=40))
        grid.add_widget(self.credito)

        grid.add_widget(Label(text="Nota de débito", size_hint_y=None, height=40))
        grid.add_widget(self.debito_rec)

        grid.add_widget(Label(text="Nota de crédito", size_hint_y=None, height=40))
        grid.add_widget(self.credito_rec)

        grid.add_widget(Label(text="Remanente anterior", size_hint_y=None, height=40))
        grid.add_widget(self.remanente)

        root.add_widget(grid)

        boton = Button(
            text="Calcular",
            size_hint=(1, 0.15),
            background_color=(0.6, 0.3, 0.8, 1)
        )

        boton.bind(on_press=self.calcular)
        root.add_widget(boton)

        scroll = ScrollView(size_hint=(1, 0.4))

        self.resultado = Label(
            text="",
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        self.resultado.bind(
            width=lambda s, w: setattr(s, "text_size", (w, None)),
            texture_size=lambda s, v: setattr(s, "height", v[1])
        )

        scroll.add_widget(self.resultado)
        root.add_widget(scroll)

        return root


    def calcular(self, instance):

        try:

            debito = float(self.debito.text or 0)
            credito = float(self.credito.text or 0)
            debito_rec = float(self.debito_rec.text or 0)
            credito_rec = float(self.credito_rec.text or 0)
            remanente = float(self.remanente.text or 0)

            total_debito = debito + debito_rec
            total_credito = credito + credito_rec

            iva_final = total_debito - total_credito - remanente

            texto = f"""
Paso 1
Débito fiscal (ventas): {pesos_chilenos(debito)}

Paso 2
Se suma nota de débito: {pesos_chilenos(debito_rec)}

Total débitos = {pesos_chilenos(total_debito)}

Paso 3
Crédito fiscal (compras): {pesos_chilenos(credito)}

Paso 4
Nota de crédito: {pesos_chilenos(credito_rec)}

Total créditos = {pesos_chilenos(total_credito)}

Paso 5
Remanente anterior: {pesos_chilenos(remanente)}

Resultado final:
{pesos_chilenos(iva_final)}
"""

            if iva_final > 0:
                texto += "\nDebes pagar este IVA."
            else:
                texto += f"\nNo pagas IVA. Nuevo remanente: {pesos_chilenos(abs(iva_final))}"

            self.texto = texto
            self.resultado.text = ""
            self.i = 0

            Clock.schedule_interval(self.escribir, 0.02)

        except:
            self.resultado.text = "Error: ingresa solo números."


    def escribir(self, dt):

        if self.i < len(self.texto):

            self.resultado.text += self.texto[self.i]
            self.i += 1

        else:
            return False


CalculadoraF29().run()