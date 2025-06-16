import os  # Para rutas absolutas y gestión de archivos temporales
import random  # Para elegir un enlace aleatorio
import webbrowser  # Para abrir URLs
import sys  # Para gestionar argumentos del sistema y cerrar la app
from ventana import Ui_MainWindow  # Interfaz gráfica generada por Qt Designer
from PyQt5.QtWidgets import QApplication, QMainWindow  # Componentes de la interfaz
from PyQt5.QtCore import QTime, QTimer  # Manejo de tiempo y temporizador en tiempo real



def programar_alarma_cron(hora_qtime):

    '''Extrae hora y minuto desde un QTime.

       Genera una línea cron con el script a ejecutar a esa hora.

       Borra alarmas anteriores generadas por la app (buscando el comentario # Alarma añadida por app PyQt).

       Añade la nueva entrada al crontab'''

    hora = hora_qtime.hour()
    minuto = hora_qtime.minute()

    script_path = os.path.abspath("alarma_disparada.py")
    cron_line = f"{minuto} {hora} * * * DISPLAY=:0 /home/balili92/miniconda3/bin/python3 \"{script_path}\" # Alarma añadida por app PyQt\n"

    existing_cron = os.popen("crontab -l 2>/dev/null").read()

    # Quitar alarmas anteriores con el mismo comentario
    filtered_cron = "\n".join(
        line for line in existing_cron.splitlines()
        if "Alarma añadida por app PyQt" not in line )

    # Agregar nueva línea
    final_cron = filtered_cron + "\n" + cron_line

    with open("temp_cron.txt", "w") as f:
        f.write(final_cron)

    os.system("crontab temp_cron.txt")
    os.remove("temp_cron.txt")


def borrar_alarmas_cron():
    '''Lee el crontab actual del usuario.

       Elimina todas las entradas con el comentario de tu app.

       Reescribe el crontab sin esas entradas.'''
    # Lee el contenido actual del crontab
    cron_actual = os.popen("crontab -l 2>/dev/null").read()
    
    if not cron_actual.strip():
        print("El crontab está vacío. No hay alarmas para borrar.")
        return

    # Comentario que identifica tus alarmas
    marcador = "# Alarma añadida por app PyQt"

    # Filtra todas las líneas que NO tengan ese comentario
    lineas_filtradas = [
        linea for linea in cron_actual.splitlines()
        if marcador not in linea.strip()
    ]

    # Si no se elimina ninguna línea, avisa
    if len(lineas_filtradas) == len(cron_actual.splitlines()):
        print("No se encontraron alarmas creadas por la app.")
        return

    # Crear nuevo contenido del crontab
    nuevo_cron = "\n".join(lineas_filtradas) + "\n"

    # Guardarlo en un archivo temporal
    with open("temp_cron.txt", "w") as f:
        f.write(nuevo_cron)

    # Reemplaza el crontab actual con el filtrado
    resultado = os.system("crontab temp_cron.txt")
    os.remove("temp_cron.txt")

    if resultado == 0:
        print("✔ Alarmas eliminadas correctamente del crontab.")
    else:
        print("❌ Hubo un error al actualizar el crontab.")


class MainApp(QMainWindow): # Clase principal que hereda de QMainWindow
    def __init__(self):
        '''Carga la UI generada con Qt Designer.

        Inicia el reloj (actualizado cada segundo).

        Conecta los botones de "establecer alarma" y "borrar alarma".

        Carga los enlaces desde enlaces.txt.'''
        super().__init__()
        self.alarma = None  # Variable para almacenar la hora de la alarma

        # Carga la interfaz gráfica creada con Qt Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Aplica la interfaz al objeto actual

        self.iniciar_reloj()  # Llama a la función que inicia el reloj actual
        

        # Conecta los botones a sus funciones correspondientes
        self.ui.establecer_alarma.clicked.connect(self.guardar_hora)
        self.ui.borrar_alarma.clicked.connect(self.borrar_alarma)

        # Intenta leer los enlaces desde un archivo de texto
        try:
            with open("enlaces.txt", "r") as file:
                self.lineas = file.readlines()  # Guarda todas las líneas en una lista
        except FileNotFoundError:
            self.lineas = []  # Si no se encuentra el archivo, crea una lista vacía
            self.ui.label_mensaje.setText("Archivo de enlaces no encontrado")  # Muestra un mensaje al usuario

        # Selecciona un enlace aleatorio si hay líneas disponibles
        if self.lineas:
            self.numero_aleatorio = random.randint(0, len(self.lineas) - 1)
        else:
            self.numero_aleatorio = None

    # Función para guardar la hora establecida por el usuario como alarma
    def guardar_hora(self):

        '''Toma la hora del widget de la UI.

            Si es una hora futura, la guarda como alarma.

            Muestra mensaje al usuario.

            Programa una tarea cron con esa hora.'''
        
        hora = self.ui.hora_alarma.time()  # Obtiene la hora seleccionada en el widget de tiempo
        if hora > self.hora_actual:  # Verifica que sea posterior a la hora actual
            self.alarma = hora  # Guarda la hora como alarma
            hora_string = hora.toString("HH:mm")  # Convierte la hora a string para mostrarla
            self.ui.label_mensaje.setText(f"Hora guardada: {hora_string}")
            programar_alarma_cron(self.alarma)
           
        else:
            self.ui.label_mensaje.setText("La hora de la alarma debe ser mayor que la hora actual")

    # Inicializa y arranca un temporizador que actualiza la hora cada segundo
    def iniciar_reloj(self):
        '''Actualiza el reloj en tiempo real cada segundo.

        Si llega la hora de la alarma, abre un enlace aleatorio y borra la alarma tanto de la app como del crontab.'''

        self.timer = QTimer(self)  # Crea un temporizador
        self.timer.timeout.connect(self.actualizar_hora)  # Conecta la señal timeout a la función que actualiza la hora
        self.timer.start(1000)  # El temporizador se dispara cada 1000 ms (1 segundo)
        self.actualizar_hora()  # Llama inmediatamente para mostrar la hora sin esperar 1 segundo

    # Función que actualiza la hora actual y verifica si es hora de activar la alarma
    def actualizar_hora(self):

        '''Actualiza el reloj en tiempo real cada segundo.

        Si llega la hora de la alarma, abre un enlace aleatorio y borra la alarma tanto de la app como del crontab.'''
        try:
            self.hora_actual = QTime.currentTime()  # Obtiene la hora actual del sistema
            self.ui.reloj.setText(self.hora_actual.toString("HH:mm"))  # Actualiza el texto del reloj en la interfaz

            # Verifica si hay una alarma configurada y si es el momento de activarla
            if self.alarma is not None and self.hora_actual >= self.alarma:
                if self.numero_aleatorio is not None:
                    url = self.lineas[self.numero_aleatorio].strip()  # Quita saltos de línea
                    webbrowser.open(url)  # Abre el enlace en el navegador
                    self.ui.label_mensaje.setText(f"Alarma activada a las {self.alarma.toString('HH:mm')}")
                    self.alarma = None  # Resetea la alarma
                    borrar_alarmas_cron()

                # Elige un nuevo enlace aleatorio para la próxima alarma (si hay)
                if self.lineas:
                    self.numero_aleatorio = random.randint(0, len(self.lineas) - 1)
                else:
                    self.numero_aleatorio = None
        except AttributeError as e:
            print("Error:", e)  # En caso de error con atributos, lo muestra por consola
            
    # Función para borrar la alarma activa
    def borrar_alarma(self):
            '''Resetea la alarma en memoria.

                Llama a borrar_alarmas_cron() para limpiarla del sistema.'''


            if self.alarma is not None:
                self.alarma = None  # Elimina la hora de la alarma
                self.ui.label_mensaje.setText("Alarma eliminada")  # Muestra mensaje al usuario
                borrar_alarmas_cron()
            


    

    

# Código que arranca la aplicación
app = QApplication(sys.argv)  # Crea la instancia principal de la app
window = MainApp()            # Crea la ventana principal
window.show()                 # Muestra la ventana
sys.exit(app.exec_())         # Ejecuta el bucle de eventos de la app y sale correctamente al cerrarla
