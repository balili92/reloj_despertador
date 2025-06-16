# ⏰ Alarma con PyQt5 + Cron en Ubuntu

Una aplicación de escritorio en Python con PyQt5 que permite establecer alarmas. Cuando llega la hora programada, se abre automáticamente un enlace aleatorio desde un archivo de texto. La alarma se programa en el sistema usando `cron`, por lo que funciona aunque cierres la aplicación.

---

## 🖥️ Requisitos

- Python 3.8 o superior
- PyQt5
- Sistema operativo Linux (probado en Ubuntu)
- `cron` instalado y configurado

---

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/alarma-pyqt-cron.git
cd alarma-pyqt-cron
```

2. Instala las dependencias necesarias:

```bash
pip install PyQt5
```

3. Crea un archivo `enlaces.txt` en el mismo directorio que `main.py`, con una URL por línea. Ejemplo:

```txt
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://open.spotify.com/track/...
```

---

## 🚀 Uso

1. Ejecuta la app:

```bash
python3 main.py
```

2. Establece una hora de alarma y pulsa el botón **Establecer alarma**.

3. Si cierras la aplicación, el sistema ejecutará el script automáticamente a la hora programada gracias a `cron`.

4. Para eliminar alarmas programadas previamente desde la app, pulsa **Borrar alarma**.

---

## ⚙️ ¿Cómo funciona?

- Usa PyQt5 para la interfaz gráfica.
- Muestra la hora actual en vivo.
- Permite al usuario establecer una hora para la alarma.
- El script genera una entrada en el `crontab` del usuario.
- A la hora exacta, se ejecuta `alarma_disparada.py`, que abre un enlace aleatorio del archivo `enlaces.txt`.
- Las entradas del cron tienen un comentario identificador para ser eliminadas posteriormente si es necesario.

---

## 📁 Estructura del Proyecto

```
alarma-pyqt-cron/
├── main.py                # Código principal de la aplicación
├── alarma_disparada.py    # Script ejecutado por cron que lanza el navegador
├── ventana.py             # Interfaz generada por Qt Designer
├── enlaces.txt            # Lista de URLs para la alarma
```
