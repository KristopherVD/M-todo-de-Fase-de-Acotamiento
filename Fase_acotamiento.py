import numpy as np
import matplotlib.pyplot as plt

class FaseAcotamiento:
    """
    Clase que encapsula el Método de Fase de Acotamiento para optimización 1D.
    """
    def __init__(self, funcion, nombre_funcion="f(x)"):
        # Atributos privados para garantizar el encapsulamiento
        self.__funcion = funcion
        self.__nombre = nombre_funcion
        self.__historial_x = [] # Para almacenar los saltos y poder graficarlos

    def encontrar_intervalo(self, x0: float, delta: float):
        """
        Ejecuta el método de fase de acotamiento para encerrar el mínimo.
        Retorna una tupla con el intervalo [a, b].
        """
        f = self.__funcion
        delta = abs(delta) # Aseguramos que la magnitud inicial sea positiva
        self.__historial_x.clear()
        
        # PASO 1 y 2: Evaluar puntos iniciales y determinar dirección de búsqueda
        f_minus = f(x0 - delta)
        f_x0 = f(x0)
        f_plus = f(x0 + delta)
        
        if f_minus >= f_x0 >= f_plus:
            paso = delta      # La curva baja hacia la derecha, dirección positiva
        elif f_minus <= f_x0 <= f_plus:
            paso = -delta     # La curva baja hacia la izquierda, dirección negativa
        elif f_minus >= f_x0 and f_x0 <= f_plus:
            # Caso especial: El mínimo ya está encerrado en el primer intento
            return (x0 - delta, x0 + delta)
        else:
            raise ValueError("La función no es unimodal o el incremento inicial es muy grande.")
            
        # PASO 3: Inicialización del algoritmo
        x_k_minus_1 = x0
        x_k = x0 + paso
        k = 1
        
        # Guardamos los primeros dos puntos en el historial para la gráfica
        self.__historial_x.extend([x_k_minus_1, x_k])
        
        # PASO 4 y 5: Ciclo de crecimiento exponencial
        while True:
            # Fórmula de actualización exponencial: x^(k+1) = x^(k) + 2^k * paso
            x_k_plus_1 = x_k + (2**k) * paso
            self.__historial_x.append(x_k_plus_1)
            
            # Condición de parada: Si el nuevo valor de f(x) sube, hemos pasado el mínimo
            if f(x_k_plus_1) < f(x_k):
                # El valor sigue bajando, avanzamos nuestras variables y aumentamos k
                x_k_minus_1 = x_k
                x_k = x_k_plus_1
                k += 1
            else:
                # El valor subió. El mínimo quedó atrapado entre x^(k-1) y x^(k+1)
                # Ordenamos para siempre devolver [menor, mayor] sin importar la dirección
                limite_inf = min(x_k_minus_1, x_k_plus_1)
                limite_sup = max(x_k_minus_1, x_k_plus_1)
                return (limite_inf, limite_sup)

    def graficar(self, intervalo, x_min_plano, x_max_plano):
        """Genera una visualización del algoritmo y el intervalo acotado."""
        x_vals = np.linspace(x_min_plano, x_max_plano, 400)
        y_vals = self.__funcion(x_vals)
        
        plt.figure(figsize=(9, 5))
        plt.plot(x_vals, y_vals, label=self.__nombre, color='steelblue', linewidth=2)
        
        # Sombreado del intervalo acotado
        plt.axvspan(intervalo[0], intervalo[1], color='lightgreen', alpha=0.3, label='Intervalo Acotado')
        
        # Marcadores de los saltos exponenciales
        y_hist = [self.__funcion(x) for x in self.__historial_x]
        plt.plot(self.__historial_x, y_hist, 'ro-', alpha=0.7, label='Saltos del Algoritmo')
        
        # Destacar punto inicial y final
        plt.scatter(self.__historial_x[0], y_hist[0], color='black', zorder=5, label='Inicio (x0)')
        
        plt.title(f"Fase de Acotamiento | {self.__nombre}")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()

# ==========================================
# Pruebas Sugeridas (Script Principal)
# ==========================================
if __name__ == "__main__":
    
    # 1. Exponencial: f(x) = e^x - 5x | x0 = 0, Delta = 0.5
    f1 = lambda x: np.exp(x) - 5*x
    algoritmo1 = FaseAcotamiento(f1, "f(x) = e^x - 5x")
    int1 = algoritmo1.encontrar_intervalo(0, 0.5)
    print(f"1. Función Exponencial -> El mínimo está en el intervalo: [{int1[0]:.3f}, {int1[1]:.3f}]")
    algoritmo1.graficar(int1, -1, 4)

    # 2. Polinomial: f(x) = x^4 - 3x^3 + 2 | x0 = 0, Delta = 0.1
    f2 = lambda x: x**4 - 3*x**3 + 2
    algoritmo2 = FaseAcotamiento(f2, "f(x) = x^4 - 3x^3 + 2")
    int2 = algoritmo2.encontrar_intervalo(0, 0.1)
    print(f"2. Función Polinomial  -> El mínimo está en el intervalo: [{int2[0]:.3f}, {int2[1]:.3f}]")
    algoritmo2.graficar(int2, -0.5, 3.5)

    # 3. Logarítmica: f(x) = x^2 - ln(x) | x0 = 0.5, Delta = 0.2
    f3 = lambda x: x**2 - np.log(x)
    algoritmo3 = FaseAcotamiento(f3, "f(x) = x^2 - ln(x)")
    int3 = algoritmo3.encontrar_intervalo(0.5, 0.2)
    print(f"3. Función Logarítmica -> El mínimo está en el intervalo: [{int3[0]:.3f}, {int3[1]:.3f}]")
    algoritmo3.graficar(int3, 0.1, 1.5)