import tkinter as tk  # Импорт модуля для создания графического интерфейса
from threading import Thread  # Импорт модуля для работы с многопоточностью
import keyboard  # Импорт модуля для работы с клавиатурой

class Command:  # Определение базового класса Command
    def execute(self):  # Метод для выполнения команды
        pass

    def undo(self):  # Метод для отмены команды
        pass

class LaunchBrowserCommand(Command):  # Определение класса LaunchBrowserCommand, который наследуется от Command
    def execute(self):  # Переопределение метода execute для запуска браузера
        print("Launching browser")

    def undo(self):  # Переопределение метода undo для закрытия браузера
        print("Closing browser")

class Key:  # Определение класса Key
    def init(self, command):  # Метод инициализации с передачей команды
        self.command = command

    def press(self):  # Метод для нажатия клавиши
        self.command.execute()

    def release(self):  # Метод для отпускания клавиши
        self.command.undo()

class VirtualKeyboard:  # Определение класса VirtualKeyboard
    def init(self, root):  # Метод инициализации с передачей корневого окна
        self.root = root
        self.root.title("Virtual Keyboard")  # Установка заголовка окна
        self.text = tk.StringVar()  # Создание переменной для хранения текста
        self.text.set("")  # Установка начального значения текста
        self.key_mapping = {  # Создание словаря для отображения клавиш
            'Q': 'A',
            'A': 'Q',
        }
        self.text_entry = tk.Entry(root, textvariable=self.text)  # Создание текстового поля
        self.text_entry.pack()  # Размещение текстового поля в окне
        self.button_frame = tk.Frame(root)  # Создание фрейма для кнопок клавиатуры
        self.button_frame.pack()  # Размещение фрейма в окне
        self.create_keyboard_buttons()  # Вызов метода для создания кнопок клавиатуры
        self.undo_button = tk.Button(root, text="Отменить", command=self.undo_action)  # Создание кнопки "Отменить"
        self.undo_button.pack()  # Размещение кнопки "Отменить" в окне
        self.history = []  # Создание списка для хранения истории действий
        self.pending_1 = False  # Переменная для отслеживания состояния нажатия клавиши "1"
        self.keyboard_thread = Thread(target=self.listen_keyboard)  # Создание потока для отслеживания клавиатуры
        self.keyboard_thread.daemon = True  # Установка потока как демонического
        self.keyboard_thread.start()  # Запуск потока

    def create_keyboard_buttons(self):  # Метод для создания кнопок клавиатуры
        keyboard_layout = [  # Определение раскладки клавиатуры
            '1234567890',
            'QWERTYUIOP',
            'ASDFGHJKL',
            'ZXCVBNM',
        ]
        for row in keyboard_layout:  # Перебор строк раскладки клавиатуры
            row_frame = tk.Frame(self.button_frame)  # Создание фрейма для строки клавиатуры
            row_frame.pack()  # Размещение фрейма строки в окне
            for char in row:  # Перебор символов в строке
                command = Key(LaunchBrowserCommand())  # Создаем экземпляр класса Key с командой LaunchBrowserCommand
                button = tk.Button(row_frame, text=char, command=lambda c=char: self.add_character(c))  # Создание кнопки с символом и привязкой к методу add_character
                button.pack(side=tk.LEFT)  # Размещение кнопки внутри строки

    def add_character(self, char):  # Метод для добавления символа в текстовое поле
        if self.pending_1:  # Если ожидается вторая часть символа "1"
            if char == '2':  # Если нажата клавиша "2"
                self.text.set(self.text.get() + 'B')  # Добавление символа "B" в текстовое поле
                self.pending_1 = False  # Сброс ожидания второй части символа "1"
            else:
                self.text.set(self.text.get() + '1' + char)  # Добавление символа "1" и следующего символа в текстовое поле
        else:
            if char == '1':  # Если нажата клавиша виша "1"
                self.pending_1 = True  # Установка ожидания второй части символа "1"
            mapped_char = self.key_mapping.get(char, char)  # Получение отображенного символа из словаря или использование исходного символа
            self.text.set(self.text.get() + mapped_char)  # Добавление символа в текстовое поле
            self.history.append(char)  # Добавление символа в историю действий

    def undo_action(self):  # Метод для отмены последнего действия
        if self.history:  # Если есть элементы в истории действий
            last_char = self.history.pop()  # Удаление последнего символа из истории
            if self.pending_1:  # Если ожидается вторая часть символа "1"
                self.pending_1 = False  # Сброс ожидания второй части символа "1"
            current_text = self.text.get()  # Получение текущего текста из текстового поля
            if current_text:  # Если текстовое поле не пусто
                self.text.set(current_text[:-1])  # Удаление последнего символа из текстового поля

    def run(self):  # Метод для запуска главного цикла обработки событий окна
        self.root.mainloop()

    def listen_keyboard(self):  # Метод для отслеживания нажатий клавиш на клавиатуре
        while True:  # Бесконечный цикл отслеживания событий клавиатуры
            event = keyboard.read_event(suppress=True)  # Чтение события клавиатуры с подавлением вывода на экран
            if event.event_type == keyboard.KEY_DOWN:  # Если событие - нажатие клавиши на клавиатуре
                self.add_character(event.name)  # Добавление символа в текстовое поле

def simulate_typing(keyboard, text_to_type):  # Функция для имитации ввода текста с клавиатуры
    for char in text_to_type:  # Перебор символов в тексте для ввода
        keyboard.add_character(char)  # Добавление символа в текстовое поле

if name == "main":  # Проверка на то, что скрипт запущен как основной (не импортирован как модуль)
    root = tk.Tk()  # Создание корневого окна приложения
    keyboard_app = VirtualKeyboard(root)  # Создание экземпляра класса VirtualKeyboard с передачей корневого окна
    simulation_thread = Thread(target=simulate_typing, args=(keyboard_app, "Hello, World!"))  # Создание потока для имитации ввода текста с клавиатуры
    simulation_thread.start()  # Запуск потока имитации ввода текста с клавиатуры
    keyboard_app.run()  # Запуск главного цикла обработки событий окна приложения