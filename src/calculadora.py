"""from datetime import datetime

# Este método es el constructor de la clase CalculadoraLiquidacion.
# Toma un parámetro opcional valor_uvt que representa el valor de la Unidad de Valor Tributario (UVT) por defecto,
# el cual se establece en 39205 si no se proporciona otro valor.
# Inicializa el atributo self.valor_uvt con el valor proporcionado o el valor predeterminado.

class CalculadoraLiquidacion:
    def __init__(self, valor_uvt=39205):
        self.valor_uvt = valor_uvt

# Este método calcula los resultados de la liquidación para un trabajador dados su salario básico, fecha de inicio de labores,
# fecha de las últimas vacaciones y días acumulados de vacaciones.
# Llama a varios métodos internos de la clase CalculadoraLiquidacion para realizar los cálculos necesarios.
# Los resultados de la liquidación incluyen la indemnización, vacaciones, cesantías, intereses de cesantías, prima,
# retención en la fuente y el total a pagar después de la retención.
# Estos resultados se devuelven como una tupla en el siguiente orden:
# (indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar)

    def calcular_resultados_prueba(self, salario_basico, fecha_inicio_labores, fecha_ultimas_vacaciones, dias_acumulados_vacaciones):
        indemnizacion = self.calcular_liquidacion(salario_basico, fecha_inicio_labores, fecha_ultimas_vacaciones)
        vacaciones = self.calcular_vacaciones(salario_basico, dias_acumulados_vacaciones)
        cesantias = self.calcular_cesantias(salario_basico, dias_acumulados_vacaciones)
        intereses_cesantias = self.calcular_intereses_cesantias(cesantias, vacaciones)
        primas = self.calcular_prima(salario_basico, dias_acumulados_vacaciones)
        retencion_fuente = self.calcular_retencion(indemnizacion + vacaciones + cesantias + intereses_cesantias + primas)
        total_pagar = indemnizacion + vacaciones + cesantias + intereses_cesantias + primas - retencion_fuente
        return indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar

# Este método calcula la indemnización a pagar al trabajador en caso de despido, renuncia o retiro.
# Toma el salario básico del trabajador, la fecha de inicio de labores y la fecha de terminación como parámetros.
# Primero verifica que el salario no sea negativo. Si lo es, se lanza una excepción ValueError.
# Luego, convierte las fechas de inicio y fin de labores al tipo datetime.
# Calcula el número de días totales trabajados, sumando 1 al resultado de la diferencia entre las fechas.
# Calcula los días faltantes del mes de finalización del trabajo restando el día de la fecha de finalización del total de días del mes.
# Calcula el valor diario del salario dividiendo el salario mensual entre 30 días.
# Finalmente, calcula la indemnización multiplicando el valor diario por los días faltantes del mes y redondea el resultado.
# Retorna el valor de la indemnización.

    def calcular_liquidacion(self, salario, fecha_inicio, fecha_fin):
        if salario < 0:
            raise ValueError("El salario básico no puede ser negativo")
    
        fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
        dias_totales = (fecha_fin - fecha_inicio).days + 1
        dias_faltantes = 30 - fecha_fin.day
        valor_diario = salario / 30
        liquidacion = valor_diario * dias_faltantes
        return round(liquidacion)

# Este método calcula la indemnización a pagar al trabajador en caso de despido, renuncia o retiro.
# Toma el salario básico del trabajador, el motivo de terminación y los meses trabajados como parámetros.
# Verifica si el motivo de terminación proporcionado es válido. Si no lo es, lanza una excepción ValueError.
# Luego, determina el factor de despido según el motivo proporcionado.
# Calcula el valor de la indemnización multiplicando el salario por los meses trabajados y el factor de despido.
# Retorna el valor de la indemnización.

    def calcular_indemnizacion(self, salario, motivo, meses_trabajados):
        motivos_validos = ['despido', 'renuncia', 'retiro']
        motivo_lower = motivo.lower()
        if motivo.lower() not in motivos_validos:
            raise ValueError("El motivo de terminación no es válido")
        if motivo_lower not in motivos_validos:
            raise ValueError(f"El motivo de terminación '{motivo}' no es válido. Los motivos válidos son: {', '.join(motivos_validos)}")
        factor_despido = 0.5 if motivo_lower == 'despido' else 0.0
        valor_indemnizacion = salario * meses_trabajados * factor_despido
        return valor_indemnizacion

# Este método calcula el valor de las vacaciones proporcionales para el trabajador.
# Toma el salario mensual del trabajador y los días acumulados de vacaciones como parámetros.
# Primero verifica si los días acumulados de vacaciones son negativos. Si lo son, lanza una excepción ValueError.
# Luego, calcula el valor diario del salario dividiendo el salario mensual entre 30 días.
# Calcula el valor de las vacaciones dividiendo el salario mensual por 720 (que corresponde a los días hábiles de trabajo en dos años).
# Redondea el valor de las vacaciones y lo devuelve.

    def calcular_vacaciones(self, salario_mensual, dias_trabajados):
        if dias_trabajados < 0:
            raise ValueError("Los días acumulados de vacaciones no pueden ser negativos")
        valor_diario = salario_mensual / 30
        valor_vacaciones = (salario_mensual * dias_trabajados) / 720
        return round(valor_vacaciones)

# Este método calcula la indemnización a pagar al trabajador en caso de despido, renuncia o retiro.
# Toma el salario básico del trabajador, el motivo de terminación y los meses trabajados como parámetros.
# Verifica si el motivo de terminación proporcionado es válido. Si no lo es, lanza una excepción ValueError.
# Determina el factor de despido según el motivo proporcionado.
# Calcula el valor de la indemnización multiplicando el salario por los meses trabajados y el factor de despido.
# Retorna el valor de la indemnización.

    def calcular_indemnizacion(self, salario, motivo, meses_trabajados):
        motivos_validos = ['despido', 'renuncia', 'retiro']
        motivo_lower = motivo.lower()
        if motivo_lower not in motivos_validos:
            raise ValueError(f"El motivo de terminación '{motivo}' no es válido. Los motivos válidos son: {', '.join(motivos_validos)}")
        factor_despido = 0.5 if motivo_lower == 'despido' else 0.0
        valor_indemnizacion = salario * meses_trabajados * factor_despido
        return valor_indemnizacion
    
# Este método calcula el valor de las cesantías proporcionales para el trabajador.
# Toma el salario mensual del trabajador y los días trabajados como parámetros.
# Verifica si los días trabajados son negativos. Si lo son, lanza una excepción ValueError.
# Calcula el valor de las cesantías dividiendo el salario mensual por 360 (que corresponde a los días hábiles de trabajo en un año).
# Redondea el valor de las cesantías y lo devuelve.

    def calcular_cesantias(self, salario_mensual, dias_trabajados):
        if dias_trabajados < 0:
            raise ValueError("Los días trabajados no pueden ser negativos")
        cesantias = (salario_mensual * dias_trabajados) / 360
        return round(cesantias)
    
    # Este método calcula los intereses sobre las cesantías acumuladas.
# Toma el valor de las cesantías y el valor de las vacaciones como parámetros.
# Verifica si el valor de las cesantías o el valor de las vacaciones son negativos.
# Si alguno de ellos es negativo, lanza una excepción ValueError.
# Calcula el valor de los intereses de cesantías como el 12% de la suma de las cesantías y las vacaciones.
# Retorna el valor de los intereses de cesantías.

    def calcular_intereses_cesantias(self, cesantias, vacaciones):
        if cesantias < 0:
            raise ValueError("El valor de las cesantías no puede ser negativo")
        if vacaciones < 0:
            raise ValueError("El valor de las vacaciones no puede ser negativo")
        valor_intereses_cesantias = (cesantias + vacaciones) * 0.12
        return valor_intereses_cesantias
    
# Este método calcula el valor de la prima de servicios para el trabajador.
# Toma el salario mensual del trabajador y los días trabajados como parámetros.
# Calcula la prima dividiendo el salario mensual por 360 (que corresponde a los días hábiles de trabajo en un año),
# y luego multiplicando este resultado por los días trabajados.
# Finalmente, redondea la mitad del valor de la prima y lo devuelve.

    def calcular_prima(self, salario_mensual, dias_trabajados):
        prima = salario_mensual * (dias_trabajados / 360)
        return round(prima / 2)

# Este método calcula la retención en la fuente sobre los ingresos del trabajador.
# Toma el salario básico del trabajador como parámetro.
# Verifica si el salario básico es un número (int o float). Si no lo es, lanza una excepción ValueError.
# Inicializa la retención en 0.
# Convierte el salario básico a tipo float.
# Comprueba el rango en el que se encuentra el salario básico y calcula la retención correspondiente.
# Si el salario básico es menor o igual a 42,412 UVT (Unidad de Valor Tributario), la retención es 0.
# Si el salario básico está entre 42,412 y 636,132 UVT, calcula la retención según una fórmula específica.
# Retorna el valor de la retención, redondeado al entero más cercano.

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
        return round(retencion)

    def imprimir_resultados(self, indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar):
        if total_pagar < 0:
            raise ValueError("El total a pagar no puede ser negativo")
"""