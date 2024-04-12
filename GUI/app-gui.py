from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from datetime import datetime

# Añade la ruta donde está la fuente Roboto
resource_add_path('fonts')

class CalculadoraLiquidacion:
    def __init__(self, valor_uvt=39205):
        self.valor_uvt = valor_uvt

    def calcular_resultados_prueba(self, salario_basico, fecha_inicio_labores, fecha_ultimas_vacaciones, dias_acumulados_vacaciones, motivo_salida):
        indemnizacion = self.calcular_liquidacion(salario_basico, fecha_inicio_labores, fecha_ultimas_vacaciones)
        vacaciones = self.calcular_vacaciones(salario_basico, dias_acumulados_vacaciones)
        cesantias = self.calcular_cesantias(salario_basico, dias_acumulados_vacaciones)
        intereses_cesantias = self.calcular_intereses_cesantias(cesantias, dias_acumulados_vacaciones)
        primas = self.calcular_prima(salario_basico, dias_acumulados_vacaciones)
        retencion_fuente = self.calcular_retencion(indemnizacion + vacaciones + cesantias + intereses_cesantias + primas)
        total_pagar = indemnizacion + vacaciones + cesantias + intereses_cesantias + primas - retencion_fuente
        return indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar

    def calcular_liquidacion(self, salario, fecha_inicio, fecha_fin):
        if salario < 0:
            raise ValueError("El salario básico no puede ser negativo")
    
        fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
        dias_totales = (fecha_fin - fecha_inicio).days + 1
        dias_faltantes = 30 - fecha_fin.day
        valor_diario = salario / 30
        liquidacion = valor_diario * dias_faltantes
        return round(liquidacion, 2)

    def calcular_vacaciones(self, salario_mensual, dias_trabajados):
        if dias_trabajados < 0:
            raise ValueError("Los días acumulados de vacaciones no pueden ser negativos")
        valor_vacaciones = (salario_mensual * dias_trabajados) / 720
        return round(valor_vacaciones, 2)

    def calcular_cesantias(self, salario_mensual, dias_trabajados):
        if dias_trabajados < 0:
            raise ValueError("Los días trabajados no pueden ser negativos")
        cesantias = (salario_mensual * dias_trabajados) / 360
        return round(cesantias, 2)

    def calcular_intereses_cesantias(self, cesantias, dias_trabajados):
        if cesantias < 0:
            raise ValueError("El valor de las cesantías no puede ser negativo")
        if dias_trabajados < 0:
            raise ValueError("Los días trabajados no pueden ser negativos")
        intereses_cesantias = (cesantias * dias_trabajados * 0.12) / 360
        return round(intereses_cesantias, 2)

    def calcular_prima(self, salario_mensual, dias_trabajados):
        if dias_trabajados < 0:
            raise ValueError("Los días trabajados no pueden ser negativos")
        prima = (salario_mensual * dias_trabajados * 0.0833) / 360  # 1/12 = 0.0833
        return round(prima, 2)

    def calcular_retencion(self, salario_basico):
        if not isinstance(salario_basico, (int, float)):
            raise ValueError("El salario básico debe ser un número")
        retencion = 0
        salario_basico = float(salario_basico)
        if salario_basico <= 42412:
            pass
        elif salario_basico <= 636132:
            ingreso_uvt = salario_basico / self.valor_uvt
            base_uvt = ingreso_uvt - 95
            base_pesos = base_uvt * self.valor_uvt
            retencion = (base_pesos * 0.19) + (10 * self.valor_uvt)
        return round(retencion, 2)

class ResultadosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, padding=20, spacing=10)
        self.add_widget(self.layout)

        # Color
        Window.clearcolor = get_color_from_hex('2272FF')

        self.resultados_label = Label(text="", font_name='fonts/Roboto-Regular.ttf', font_size=14, halign='left', valign='top', color=get_color_from_hex('1D1D1'))
        self.layout.add_widget(self.resultados_label)

    def mostrar_resultados(self, resultados_text):
        self.resultados_label.text = resultados_text

class LiquidacionApp(App):
    def build(self):
        self.calculadora = CalculadoraLiquidacion()

        # Configura el administrador de pantallas
        self.screen_manager = ScreenManager()

        # Crea y agrega la pantalla de ingreso de datos
        self.ingreso_screen = Screen(name="ingreso")
        self.ingreso_layout = GridLayout(cols=2, padding=20, spacing=10)
        self.ingreso_screen.add_widget(self.ingreso_layout)

        self.ingreso_layout.add_widget(Label(text="Motivo de salida (renuncia/despido):", font_name='fonts/Roboto-Regular.ttf', color=get_color_from_hex('#FFFFFF')))
        self.motivo_salida_input = TextInput(hint_text="Motivo de salida", multiline=False)
        self.ingreso_layout.add_widget(self.motivo_salida_input)

        self.ingreso_layout.add_widget(Label(text="Salario básico:", font_name='fonts/Roboto-Regular.ttf', color=get_color_from_hex('#FFFFFF')))
        self.salario_input = TextInput(hint_text="Salario básico", multiline=False)
        self.ingreso_layout.add_widget(self.salario_input)

        self.ingreso_layout.add_widget(Label(text="Fecha inicio (dd/mm/yyyy):", font_name='fonts/Roboto-Regular.ttf', color=get_color_from_hex('#FFFFFF')))
        self.fecha_inicio_input = TextInput(hint_text="Fecha inicio", multiline=False)
        self.ingreso_layout.add_widget(self.fecha_inicio_input)

        self.ingreso_layout.add_widget(Label(text="Fecha últimas vacaciones (dd/mm/yyyy):", font_name='fonts/Roboto-Regular.ttf', color=get_color_from_hex('#FFFFFF')))
        self.fecha_vacaciones_input = TextInput(hint_text="Fecha últimas vacaciones", multiline=False)
        self.ingreso_layout.add_widget(self.fecha_vacaciones_input)

        self.ingreso_layout.add_widget(Label(text="Días acumulados de vacaciones:", font_name='fonts/Roboto-Regular.ttf', color=get_color_from_hex('#FFFFFF')))
        self.dias_vacaciones_input = TextInput(hint_text="Días de vacaciones", multiline=False)
        self.ingreso_layout.add_widget(self.dias_vacaciones_input)

        self.calcular_button = Button(text="Calcular", size_hint_x=None, width=150, font_name='fonts/Roboto-Regular.ttf')
        self.calcular_button.bind(on_press=self.calcular)
        self.ingreso_layout.add_widget(self.calcular_button)

        # Agrega la pantalla de ingreso a la administración de pantallas
        self.screen_manager.add_widget(self.ingreso_screen)

        # Crea y agrega la pantalla de resultados
        self.resultados_screen = ResultadosScreen(name="resultados")
        self.screen_manager.add_widget(self.resultados_screen)

        return self.screen_manager

    def calcular(self, instance):
        salario = float(self.salario_input.text)
        fecha_inicio = self.fecha_inicio_input.text
        fecha_vacaciones = self.fecha_vacaciones_input.text
        dias_vacaciones = int(self.dias_vacaciones_input.text)
        motivo_salida = self.motivo_salida_input.text

        indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar = self.calculadora.calcular_resultados_prueba(
            salario_basico=salario,
            fecha_inicio_labores=fecha_inicio,
            fecha_ultimas_vacaciones=fecha_vacaciones,
            dias_acumulados_vacaciones=dias_vacaciones,
            motivo_salida=motivo_salida  # Se pasa el motivo de salida como parámetro
        )

        resultado_text = f"Indemnización: {indemnizacion}\nVacaciones: {vacaciones}\nCesantías: {cesantias}\nIntereses sobre cesantías: {intereses_cesantias}\nPrima de servicios: {primas}\nRetención en la fuente: {retencion_fuente}\nTotal a pagar: {total_pagar}"
        self.resultados_screen.mostrar_resultados(resultado_text)
        self.screen_manager.current = "resultados"  # Cambia a la pantalla de resultados

    def on_start(self):
        self.root_window.title = "Bienvenido a la Calculadora Definitiva"

if __name__ == "__main__":
    LiquidacionApp().run()
