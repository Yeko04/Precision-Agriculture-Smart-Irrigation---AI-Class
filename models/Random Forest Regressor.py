
class MotorInferenciaHibrido:
    def __init__(self, nombre_sistema):
        self.nombre_sistema = nombre_sistema
        self.hechos = {}
        self.reglas = []

    def agregar_hecho(self, variable, valor):
        self.hechos[variable] = valor

    def agregar_regla(self, condiciones, conclusion, valor_conclusion):
        self.reglas.append({
            "condiciones": condiciones,  # Diccionario {variable: condicion}
            "conclusion": conclusion,
            "valor_conclusion": valor_conclusion
        })

    def _evaluar_condicion(self, valor_actual, condicion_esperada):
        if valor_actual is None:
            return False
        
        # Si la condición es una cadena que representa una comparación numérica (ej. ">0.80")
        if isinstance(condicion_esperada, str):
            if condicion_esperada.startswith(">="):
                return float(valor_actual) >= float(condicion_esperada[2:])
            elif condicion_esperada.startswith("<="):
                return float(valor_actual) <= float(condicion_esperada[2:])
            elif condicion_esperada.startswith(">"):
                return float(valor_actual) > float(condicion_esperada[1:])
            elif condicion_esperada.startswith("<"):
                return float(valor_actual) < float(condicion_esperada[1:])
                
        # Comparación directa para booleanos o strings exactos
        return valor_actual == condicion_esperada

    def ejecutar(self):
        print(f"\n================ [{self.nombre_sistema}] ================")
        cambios = True
        ciclo = 1
        
        while cambios:
            cambios = False
            for regla in self.reglas:
                conclusion = regla["conclusion"]
                if conclusion in self.hechos:
                    continue
                
                # Evaluar todas las condiciones de la regla
                se_cumplen_condiciones = True
                for var, cond in regla["condiciones"].items():
                    valor_actual = self.hechos.get(var)
                    if not self._evaluar_condicion(valor_actual, cond):
                        se_cumplen_condiciones = False
                        break
                
                if se_cumplen_condiciones:
                    self.agregar_hecho(conclusion, regla["valor_conclusion"])
                    print(f"⚙️ [REGLA ACTIVADA] Por {regla['condiciones']} -> Se deduce '{conclusion}': {regla['valor_conclusion']}")
                    cambios = True
            ciclo += 1
            
        print(f"================ [Fin de Ejecución] ================\n")
        return self.hechos
    
agro = MotorInferenciaHibrido("Riego Automatizado - Smart Farm")

# 1. Hechos detectados (Sensores del suelo + Predicción de clima ML)
agro.agregar_hecho("humedad_suelo_porcentaje", 18)     # Crítico (suelo seco)
agro.agregar_hecho("probabilidad_lluvia_ml", 0.15)     # El ML estima un 15% de probabilidad de lluvia
agro.agregar_hecho("tipo_cultivo", "tomate")

# 2. Reglas del Sistema Experto (Leyes Agronómicas)
# Regla A: Si el suelo está seco y la probabilidad de lluvia es baja, se necesita agua.
agro.agregar_regla(
    condiciones={"humedad_suelo_porcentaje": "<20", "probabilidad_lluvia_ml": "<0.30"},
    conclusion="necesita_irrigacion",
    valor_conclusion=True
)

# Regla B: Si el tomate necesita agua, configurar el goteo a alta presión.
agro.agregar_regla(
    condiciones={"necesita_irrigacion": True, "tipo_cultivo": "tomate"},
    conclusion="comando_valvula",
    valor_conclusion="Abrir Válvula de Goteo 20 minutos (Alta Presión)"
)

# 3. Ejecutar
resultado = agro.ejecutar()
print(f"🌱 Decisión Agrícola: {resultado.get('comando_valvula', 'No regar por ahora')}")
