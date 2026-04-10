import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. CAPA LÓGICA (Totalmente Encapsulada)
# ==========================================
class FaseAcotamiento:
    def __init__(self, funcion, nombre_funcion="f(x)"):
        self.__funcion = funcion
        self.__nombre = nombre_funcion
        self.__historial_x = [] 

    def encontrar_intervalo(self, x0: float, delta: float):
        f = self.__funcion
        delta = abs(delta) 
        self.__historial_x.clear()
        
        f_minus = f(x0 - delta)
        f_x0 = f(x0)
        f_plus = f(x0 + delta)
        
        if f_minus >= f_x0 >= f_plus:
            paso = delta      
        elif f_minus <= f_x0 <= f_plus:
            paso = -delta     
        elif f_minus >= f_x0 and f_x0 <= f_plus:
            return (x0 - delta, x0 + delta)
        else:
            raise ValueError("La función no es unimodal en este sector.")
            
        x_k_minus_1 = x0
        x_k = x0 + paso
        k = 1
        
        self.__historial_x.extend([x_k_minus_1, x_k])
        
        while True:
            x_k_plus_1 = x_k + (2**k) * paso
            self.__historial_x.append(x_k_plus_1)
            
            if f(x_k_plus_1) < f(x_k):
                x_k_minus_1 = x_k
                x_k = x_k_plus_1
                k += 1
            else:
                limite_inf = min(x_k_minus_1, x_k_plus_1)
                limite_sup = max(x_k_minus_1, x_k_plus_1)
                return (limite_inf, limite_sup)

    def graficar(self, intervalo, x_min_plano, x_max_plano):
        x_vals = np.linspace(x_min_plano, x_max_plano, 400)
        y_vals = self.__funcion(x_vals)
        
        plt.figure(figsize=(9, 5))
        plt.plot(x_vals, y_vals, label=self.__nombre, color='steelblue', linewidth=2)
        plt.axvspan(intervalo[0], intervalo[1], color='lightgreen', alpha=0.3, label='Intervalo Acotado')
        
        y_hist = [self.__funcion(x) for x in self.__historial_x]
        plt.plot(self.__historial_x, y_hist, 'ro-', alpha=0.7, label='Saltos del Algoritmo')
        plt.scatter(self.__historial_x[0], y_hist[0], color='black', zorder=5, label='Inicio (x0)')
        
        plt.title(f"Fase de Acotamiento | {self.__nombre}")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()

# ==========================================
# 2. CAPA DE PRESENTACIÓN (Interfaz de Usuario)
# ==========================================
def iniciar_menu_interactivo():
    # Diccionario con las funciones solicitadas en la tarea
    funciones_disponibles = {
        "1": (lambda x: np.exp(x) - 5*x, "f(x) = e^x - 5x"),
        "2": (lambda x: x**4 - 3*x**3 + 2, "f(x) = x^4 - 3x^3 + 2"),
        "3": (lambda x: x**2 - np.log(x), "f(x) = x^2 - ln(x)")
    }

    while True:
        print("\n" + "="*50)
        print("   OPTIMIZADOR: MÉTODO DE FASE DE ACOTAMIENTO")
        print("="*50)
        print("Seleccione la función que desea optimizar:")
        print("  1. Función Exponencial: f(x) = e^x - 5x")
        print("  2. Función Polinomial:  f(x) = x^4 - 3x^3 + 2")
        print("  3. Función Logarítmica: f(x) = x^2 - ln(x)")
        print("  4. Salir del programa")
        print("-" * 50)
        
        opcion = input("Ingrese el número de su opción (1-4): ")

        if opcion == "4":
            print("\n¡Cerrando el optimizador! Éxito en tu tarea.")
            break

        if opcion in funciones_disponibles:
            f_seleccionada, nombre_f = funciones_disponibles[opcion]
            
            try:
                print(f"\nHa seleccionado: {nombre_f}")
                # El usuario provee el punto inicial y el incremento
                x0 = float(input(" -> Ingrese el punto inicial (x0): "))
                delta = float(input(" -> Ingrese el incremento inicial (Delta): "))
                
                # Instanciamos nuestra clase matemática pasándole los datos limpios
                optimizador = FaseAcotamiento(f_seleccionada, nombre_f)
                
                # Ejecutamos el algoritmo
                intervalo_final = optimizador.encontrar_intervalo(x0, delta)
                
                print("\n" + "*"*45)
                print(f" RESULTADO EXITOSO")
                print(f" El mínimo se encuentra en el intervalo:")
                print(f" [{intervalo_final[0]:.4f}, {intervalo_final[1]:.4f}]")
                print("*"*45)
                
                # Preguntamos si desea ver la gráfica
                ver = input("\n¿Desea generar la gráfica de los saltos? (s/n): ").strip().lower()
                if ver == 's':
                    # Calculamos un margen visual agradable para la gráfica basado en el intervalo
                    margen = abs(intervalo_final[1] - intervalo_final[0])
                    # Evitamos que log(x) evalúe números negativos o cero en la gráfica
                    lim_inf = max(0.001, intervalo_final[0] - margen) if opcion == "3" else intervalo_final[0] - margen
                    optimizador.graficar(intervalo_final, lim_inf, intervalo_final[1] + margen)
                    
            except ValueError as e:
                print(f"\n[ERROR] Por favor ingrese valores numéricos válidos.")
                print(f"Detalle técnico: {e}")
        else:
            print("\n[ERROR] Opción no válida. Por favor, seleccione 1, 2, 3 o 4.")

# Punto de entrada del script
if __name__ == "__main__":
    iniciar_menu_interactivo()