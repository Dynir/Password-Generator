import random as rand
import webbrowser
from tkinter import *

import pyperclip
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome, DesiredCapabilities
from selenium.webdriver.common.by import By


class Parol:
    def __init__(self):
        self.kol_sim = rand.randint(9, 13)
        self.str_en = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        self.num_amount = rand.randint(2, 4)
        self.random_num_place = []
        self.symbols_s = r'!"#$%&()*+,-./:;<=>?@[\]^_`{|}~'
        self.symbols_place = []
        self.symbols_amount = rand.randint(2, 4)
        self.symbols = list(self.symbols_s)
        self.symbols.append("'")
        self.line = ''

    def parol_generator(self):
        for i in range(1, self.symbols_amount + 1):
            a6 = rand.randint(1, self.kol_sim)
            if a6 not in self.random_num_place and a6 not in self.symbols_place:
                self.random_num_place.append(a6)

        for i in range(1, self.num_amount + 1):
            a7 = rand.randint(1, self.kol_sim)
            if a7 not in self.symbols_place and a7 not in self.random_num_place:
                self.symbols_place.append(a7)

        for i in range(1, self.kol_sim + 1):
            a = rand.randint(0, 1)  # 0 - строчная, 1 - заглавная
            if i in self.random_num_place:
                self.line += str(rand.randint(0, 9))
            elif i in self.symbols_place:
                self.line += rand.choice(self.symbols)
            else:
                self.line += str(rand.choice(self.str_en) if a != 1 else rand.choice(self.str_en).upper())
        # print(self.line)

    def parsing(self):
        url = r'https://www.passwordmonster.com/'
        ua = dict(DesiredCapabilities.CHROME)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        input_tab = browser.find_element(By.XPATH, r'//*[@id="lgd_out_pg_pass"]')
        input_tab.send_keys(self.line)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        self.st = soup.find(id='first_estimate').text.strip()
        print('Закрытие браузера')
        browser.close()
        print('Браузер закрыт')

    def window(self):
        print('Запуск окна Tkinter')
        root = Tk()
        root.configure(bg='#F5F5DC')
        root.geometry('380x200+200+200')
        root.title("Генератор паролей")
        root.resizable(False, False)

        def show():
            but_parol.config(text=self.line)

        def again():
            but_parol.config(text=f'{len(self.line) * "*"}', command=copy)
            self.line = ''
            h = Parol
            h.parol_generator(self)
            h.parsing(self)
            lab_info.config(text=f'Этот пароль можно будет взломать через {self.st}*')

        def copy():
            pyperclip.copy(self.line)

        def callback(event):
            webbrowser.open_new(r"https://www.passwordmonster.com/")

        label_hello = Label(text='Генератор паролей', height=1, background='#DAA520')
        label_hello.pack()
        but_parol = Button(text=f'{len(self.line) * "*"}', command=copy)
        but_parol.pack()
        but_copy = Button(text='Показать пароль', command=show)
        but_copy.pack()
        but_again = Button(text='Переделать пароль', command=again)
        but_again.pack()
        lab_info = Label(text=f'Этот пароль можно будет взломать через {self.st}*')
        lab_info.pack()
        lab_lc = Label(text='*На основании веб-сервиса')
        lab_lb = Label(text='passwordmonster.com', fg="blue", cursor="hand2")
        lab_lc.pack()
        lab_lb.pack()
        lab_lb.bind("<Button-1>", callback)

        print('Окно Tkinter запущено')
        root.mainloop()


par = Parol()
par.parol_generator()
par.parsing()
par.window()
