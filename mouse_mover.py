import pyautogui
import random
import time
import threading
from pynput import keyboard
import sys # Импортируем sys для корректного завершения программы

# --- ГЛОБАЛЬНЫЕ НАСТРОЙКИ И ФЛАГ ---

# Флаг, который контролирует работу цикла движения курсора
running = True 

# Получаем разрешение экрана один раз
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
print(f"Разрешение экрана: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

# --- ФУНКЦИЯ ДВИЖЕНИЯ КУРСОРА (ПОТОК 1) ---

def move_mouse_randomly():
    """
    Постоянно перемещает курсор мыши на случайные координаты с случайной скоростью и паузой.
    """
    global running
    
    print("Начат поток движения мыши. Курсор начнет движение.")
    
    # Отключаем защитную паузу, чтобы движения были мгновенными
    pyautogui.PAUSE = 0.0

    # Цикл продолжается, пока флаг 'running' равен True
    while running:
        try:
            # 1. Выбираем случайные координаты (X и Y)
            # Координаты должны быть меньше, чем разрешение экрана
            target_x = random.randint(0, SCREEN_WIDTH - 1)
            target_y = random.randint(0, SCREEN_HEIGHT - 1)
            
            # 2. Выбираем случайную длительность перемещения (от 0.5 до 3.0 секунд)
            duration = random.uniform(0.5, 3.0)
            
            # 3. Выбираем случайное время ожидания (пауза) (от 1.0 до 10.0 секунд)
            sleep_time = random.uniform(1.0, 10.0)
            
            # Двигаем курсор
            pyautogui.moveTo(target_x, target_y, duration=duration)
            
            # print(f"Перемещено в ({target_x}, {target_y}) за {duration:.2f} сек. Пауза {sleep_time:.2f} сек.")
            
            # Пауза перед следующим движением
            time.sleep(sleep_time)

        except Exception as e:
            # Это может помочь поймать редкие ошибки, но в целом цикл будет просто ждать
            print(f"Произошла ошибка в потоке мыши: {e}")
            time.sleep(1)
            
    print("Поток движения мыши завершен.")

# --- ФУНКЦИЯ ОТСЛЕЖИВАНИЯ КЛАВИШ (ПОТОК 2) ---

def on_key_press(key):
    """
    Обрабатывает событие нажатия любой клавиши.
    При нажатии устанавливает флаг 'running' в False и останавливает прослушиватель.
    """
    global running
    
    # Устанавливаем флаг в False, чтобы остановить цикл движения курсора
    running = False
    
    # Возвращаем False, чтобы остановить прослушиватель pynput
    # Это чистый способ выйти из потока-прослушивателя
    print("\nКлавиша нажата. Программа будет завершена.")
    return False 

def keyboard_listener_thread():
    """
    Запускает прослушиватель клавиатуры.
    """
    # Создаем и запускаем прослушиватель
    # on_press=on_key_press - вызывает нашу функцию при любом нажатии
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()
        
    print("Поток прослушивания клавиатуры завершен.")

# --- ЗАПУСК ПРОГРАММЫ ---

if __name__ == "__main__":
    print("--- Программа Анти-Сон Запущена ---")
    print("Для завершения программы нажмите ЛЮБУЮ клавишу.")
    
    # 1. Создаем потоки
    mouse_thread = threading.Thread(target=move_mouse_randomly)
    keyboard_thread = threading.Thread(target=keyboard_listener_thread)
    
    # 2. Запускаем потоки одновременно
    mouse_thread.start()
    keyboard_thread.start()
    
    # 3. Ожидаем завершения потоков
    # Мы ждем, пока оба потока выполнят свою работу (то есть, пока running не станет False)
    mouse_thread.join()
    keyboard_thread.join()
    
    # 4. Чистое завершение всей программы
    print("Программа завершена. Спасибо за использование!")
    # Используем sys.exit() для окончательного выхода, особенно полезно при запуске без консоли
    sys.exit(0)