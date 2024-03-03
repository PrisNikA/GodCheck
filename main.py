import logic
from tkinter import *
from threading import Thread
from datetime import datetime
from time import sleep
from PIL import Image, ImageTk
from tkinter import ttk
from plyer import notification

class App():
    """Класс приложения"""
    def __init__(self):
        """Создание главного меню"""
        self.root = Tk()
        self.root.title("GodCheck 1.0")
        self.root.resizable(0, 0)
        self.root.iconbitmap("icon.ico")

        # Создание логотипа
        image = Image.open("logo.png")
        logo = image.resize((100, 100))
        photo = ImageTk.PhotoImage(logo)
        Label(self.root, image=photo).pack(pady=20)

        Label(self.root, text="GodCheck 1.0", font=("Arial", 30)).pack(pady=20, padx=50)

        # Поля для ввода имени бога и токена
        Label(self.root, text="Введите имя бога:", font=("Arial", 15)).pack()
        self.entry_godname = Entry(self.root, font=("Arial", 15))
        self.entry_godname.pack(pady=10)
        Label(self.root, text="Введите API-токен (в профиле):", font=("Arial", 15)).pack()
        self.entry_API = Entry(self.root, font=("Arial", 15))
        self.entry_API.pack(pady=10)

        # Кнопка для запуска следилки
        Button(self.root, text="Запустить", command=self.root_window, font=("Arial", 20)).pack(pady=30)

        self.root.mainloop()

    def root_window(self):
        """Главное окно следилки"""

        # Получаем из полей токен и имя бога
        self.API = self.entry_API.get()
        self.godname = self.entry_godname.get()

        # Закрываем меню
        self.root.destroy()

        # Открываем поток для обновления данных раз в минуту
        self.thread = Thread(target=self.update_data)
        self.thread.start()

        # Создаем новое окно
        self.check = Tk()
        self.check.title("GodCheck 1.0")
        self.check.resizable(0, 0)
        self.check.iconbitmap("icon.ico")

        # Фрейм для героя и питомца
        self.frame_hero_pet = Frame(self.check)

        # Фрейм с информацией о герое
        self.frame_hero = LabelFrame(self.frame_hero_pet, text="Герой", fg="Blue", font=("Arial", 12))

        # Создаем нужные метки
        self.lab_godname = Label(self.frame_hero, text="Имя бога:", font=("Arial", 12))
        self.lab_name = Label(self.frame_hero, text="Имя героя:", font=("Arial", 12))
        self.lab_gender = Label(self.frame_hero, text="Пол:", font=("Arial", 12))
        self.lab_aura = Label(self.frame_hero, text="Аура:", font=("Arial", 12))
        self.lab_clan = Label(self.frame_hero, text="Гильдия:", font=("Arial", 12))
        self.lab_arena = Label(self.frame_hero, text="PVP-статистика:", font=("Arial", 12))
        self.lab_motto = Label(self.frame_hero, text="Девиз:", font=("Arial", 12))
        self.lab_aignm = Label(self.frame_hero, text="Характер:", font=("Arial", 12))
        self.lab_gold = Label(self.frame_hero, text="", font=("Arial", 12))

        # Распаковываем метки
        self.lab_godname.grid(row=0, column=0, sticky=W)
        self.lab_name.grid(row=1, column=0, sticky=W)
        self.lab_gender.grid(row=2, column=0, sticky=W)
        self.lab_aura.grid(row=3, column=0, sticky=W)
        self.lab_clan.grid(row=4, column=0, sticky=W)
        self.lab_arena.grid(row=5, column=0, sticky=W)
        self.lab_motto.grid(row=6, column=0, sticky=W)
        self.lab_aignm.grid(row=7, column=0, sticky=W)
        self.lab_gold.grid(row=8, column=0, sticky=W)

        self.frame_hero.pack(side=LEFT, padx=5)

        # Фрейм с информацией о питомце
        self.frame_pet = LabelFrame(self.frame_hero_pet, text="Питомец", font=("Arial", 12), fg="Green")

        # Создаем нужные метки
        self.lab_pet_name = Label(self.frame_pet, font=("Arial", 12))
        self.lab_pet_type = Label(self.frame_pet, font=("Arial", 12))
        self.lab_pet_level = Label(self.frame_pet, font=("Arial", 12))

        # Распаковываем метки
        self.lab_pet_name.grid(row=0, column=0, sticky=W)
        self.lab_pet_type.grid(row=1, column=0, sticky=W)
        self.lab_pet_level.grid(row=2, column=0, sticky=W)

        self.frame_pet.pack(side=RIGHT, anchor=N, padx=5)

        self.frame_hero_pet.pack()

        # Фрейм перед дневником
        self.prelog_frame = Frame(self.check, width=70)

        # Прогрессбары
        self.progress_frame = Frame(self.prelog_frame)
        self.progress_hp = ttk.Progressbar(self.progress_frame, length=200, mode='determinate')
        self.progress_inv = ttk.Progressbar(self.progress_frame, length=200, mode='determinate')
        self.progress_power = ttk.Progressbar(self.progress_frame, length=200, mode='determinate')
        self.progress_quest = ttk.Progressbar(self.progress_frame, length=200, mode='determinate')
        self.progress_level = ttk.Progressbar(self.progress_frame, length=200, mode="determinate")

        Label(self.progress_frame, text="Здоровье", font=("Arial", 10)).grid(row=0, column=0, sticky=W)
        self.progress_hp.grid(row=0, column=1, sticky=W)
        Label(self.progress_frame, text="Прана", font=("Arial", 10)).grid(row=1, column=0, sticky=W)
        self.progress_power.grid(row=1, column=1, sticky=W)
        self.lab_quest = Label(self.progress_frame, font=("Arial", 10))
        self.lab_quest.grid(row=2, column=0, sticky=E)
        self.progress_quest.grid(row=2, column=1, sticky=E)
        Label(self.progress_frame, text="Сумка", font=("Arial", 10)).grid(row=3, column=0, sticky=W)
        self.progress_inv.grid(row=3, column=1, sticky=W)
        self.lab_level = Label(self.progress_frame, text = "Уровень: 10", font = ("Arial", 10))
        self.lab_level.grid(row = 4, column = 0, sticky = W)
        self.progress_level.grid(row = 4, column = 1, sticky = W)

        self.progress_frame.pack()

        self.lab_fight_type = Label(self.prelog_frame, text="", font=("Arial", 12))
        self.lab_fight_type.pack(pady=10)
        self.prelog_frame.pack()

        # Фрейм с дневником
        self.log = LabelFrame(self.check, text="Дневник", font=("Arial", 12))
        self.text_log = Text(self.log, width=80, height=8, wrap=WORD, font=("Arial", 11), bg="Yellow", state="disabled")
        self.text_log.pack(side=LEFT)
        self.scroll = Scrollbar(self.log, orient="vertical", command=self.text_log.yview)
        self.scroll.pack(side=RIGHT, fill="y")
        self.log.pack()

        self.check.mainloop()

    def update_data(self):
        """Функция для обновления данных"""

        # Переменная для текущей записи в дневнике
        self.old_string = ""

        while True:
            # Получаем данные о герое и питомце
            self.hero, self.pet = logic.get_hero(self.godname, self.API)

            # Записываем все в метки

            # Герой
            self.lab_godname.config(text=f"Имя бога: {self.hero['godname']}")
            self.lab_name.config(text=f"Имя героя: {self.hero['name']}")
            self.lab_gender.config(text=f"Пол: {self.hero['gender']}")
            self.lab_aura.config(text=f"Аура: {self.hero['aura']}")
            self.lab_clan.config(text=f"Гильдия: {self.hero['clan']}")
            self.lab_arena.config(text=f"PVP-статистика: {self.hero['arena']}")
            self.lab_motto.config(text=f"Девиз: {self.hero['motto']}")
            self.lab_aignm.config(text=f"Характер: {self.hero['alignment']}")
            self.lab_gold.config(text=f"Награбил {self.hero['gold']} чистых золотых")

            # Питомец
            self.lab_pet_name.config(text=f"Имя питомца: {self.pet['name']}")
            self.lab_pet_type.config(text=f"Вид: {self.pet['type']}")
            self.lab_pet_level.config(text=f"Уровень: {self.pet['level']}")

            # Предневник
            self.lab_fight_type.config(text=f"~ {self.hero["fight_type"]} ~")
            self.lab_quest.config(text=f"Задание: {self.hero["quest"][0]}")
            self.progress_hp.config(maximum=int(self.hero["health"][1]), value=int(self.hero["health"][0]))
            self.progress_power.config(maximum=100, value=int(self.hero["power"]))
            self.progress_quest.config(maximum=100, value=int(self.hero["quest"][1]))
            self.progress_inv.config(maximum=int(self.hero["inventory"][1]), value=int((self.hero["inventory"][0])))
            self.lab_level.config(text = f"Уровень: {self.hero["level"][0]}")
            self.progress_level.config(maximum=100, value = int(self.hero["level"][1]))

            # Дневник
            time = datetime.now().strftime("%H:%M")
            string = f"({time}) {self.hero['diary_last']}\n"

            # Сравнение новой строки со старой
            if string != self.old_string:
                self.text_log.config(state="normal")
                self.text_log.insert(END, string)
                self.text_log.config(state="disabled")
                self.old_string = string

            # Вызываем нужные push уведомления
            self.push()

            sleep(60)

    def push(self):
        """Функция для вызова push уведомлений"""

        if int(self.hero["health"][0]) <= 50:
            notification.notify(
                title="Мало здоровья!",
                message="У героя осталось мало здоровья! Он скоро двинет коней",
                app_name="GodCheck",
                timeout=5
            )

        if int(self.hero["quest"][1]) == 100:
            notification.notify(
                title="Задание выполнено!",
                message=f"Герой смог {self.hero['quest'][0]}.",
                app_name="GodCheck",
                timeout=5
            )
        
        if int(self.hero["level"][1]) == 100:
            notification.notify(
                title = "Новый уровень!",
                message = f"Герой наконец достиг {self.hero["level"][0]} уровня!",
                app_name = "GodCheck",
                timeout = 5
            )
        
        if (int(self.hero["health"][0])) == 0:
            notification.notify(
                title = "Ой-ой!",
                message = f"{self.hero["name"]} покинул сие мир...",
                app_name = "GodCheck",
                timeout = 5
            )

# Запуск программы
if __name__ == "__main__":
    app = App()
