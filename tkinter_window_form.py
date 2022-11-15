import tkinter as tk
from tkinter import Tk, ttk, Label, Entry, Text, Scrollbar
from tkinter import filedialog as fd

from cipher2 import *
from craft import craft_password

#КЛАСС АВТОРИЗАЦИИ 
class InputPassword(Tk):
	def __init__(self):
		Tk.__init__(self)
		x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
		y = (self.winfo_screenheight() - self.winfo_reqheight()) / 2
		self.wm_geometry("+%d+%d" % (x, y))
		self.geometry("400x100")
		self.resizable(False, False)
		self.title("STRONGBOX")

		self.autorization_status, self.counter_attempt = False, 0
		#если пароль найден
		if self.look_password():
			self.mod = "login"
			self.__set_text()
			self.__set_ui()
		#если пароля нет
		else:
			self.mod = "regist"
			self.__set_text()
			self.__set_ui()

	#устанавливает текст и текстовое поле
	def __set_text(self):
		if self.mod == "login":
			Label(self, text="Введите пароль:").pack()
			self.user_text = Entry(self, width=15, show="*")
			self.user_text.pack()
		elif self.mod == "regist":
			Label(self, text="Введите новый пароль:").pack()
			self.user_text = Entry(self, width=15)
			self.user_text.pack()

	#Набор графического интерфейса
	def __set_ui(self):
		if self.mod == "login":
			ttk.Button(self, text="Ввод", command=self.check_password).pack()
		elif self.mod == "regist":
			ttk.Button(self, text="Зарегистрироваться", command=self.check_password).pack()

	#только смотрит есть ли пароль в файле
	def look_password(self) -> bool:
		try:
			self.data = unloader("loader.txt")
		except:
			raise "Файл loader.txt был удалён"
		if self.data != []: 
			return True
		else:
			return False

	#функция вызывается только через кнопку
	def check_password(self):
		password = craft_password(self.user_text.get())
		if self.mod == "login":
			if password == "".join(self.data):
				self.autorization_status = True
				self.destroy()
			else:
				if self.counter_attempt >= 1:
					self.fail.destroy()
				self.fail = Label(self, text="Неправильный пароль.")
				self.fail.pack()
				self.counter_attempt += 1
		elif self.mod == "regist":
			with open("loader.txt", "w", encoding="utf-8") as file:
				file.write(password)
			Label(self, text="Новый пароль успешно сохранён.").pack()
			self.autorization_status = True
			self.destroy()


#ДИСПЕТЧЕР ВСЕЙ ПРОГРАММЫ
class MainApp(Tk):	
	def __init__(self):
		Tk.__init__(self)
		self.geometry("800x710")
		self.resizable(False, False)
		self.title("STRONGBOX")

		self.status_open_file, self.status_scroll = False, False

		self.__set_text()
		self.__set_ui()

	def __set_text(self):
		Label(self, text="Действия:").place(relx=0.55, y=20)
		#не срабатывает только при первом запуске
		if self.status_scroll:
			self.scrollbar.destroy()

		self.user_text = Text(self, width=90, height=38)
		
		self.scrollbar = ttk.Scrollbar(command=self.user_text.yview)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.status_scroll = True
		
		self.user_text.config(yscrollcommand=self.scrollbar.set)
		self.user_text.place(relx=0.05, y=50)
		self.menu = tk.Menu(self, tearoff=0)
		self.menu.add_command(label="Вырезать", command=self.cut_text)
		self.menu.add_command(label="Копировать", command=self.copy_text)
		self.menu.add_command(label="Вставить", command=self.paste_text)
		self.menu.add_command(label="Удалить", command=self.delete_text)
		self.user_text.bind("<Button-3>", self.show_popup)

	def __set_ui(self):
		ttk.Button(self, text="Открыть файл", 
				   command=self.get_address_file).place(relx=0.05, y=20)
		ttk.Button(self, text="Создать новый", 
				   command=self.create_file).place(relx=0.2, y=20)
		self.save_but = ttk.Button(self, text="Сохранить",
				   					 command=self.save_file, state="disabled")
		self.save_but.place(relx=0.355, y=20)
		self.combo_win = ttk.Combobox(self, values=["Зашифровать", "Расшифровать"], 
									    state="readonly")
		self.combo_win.current(0)
		self.combo_win.place(relx=0.65, y=22)
		self.start_but = ttk.Button(self, text="Старт", state="disabled", command=self.start_crypto)
		self.start_but.place(relx=0.86, y=20)

	#выводит данные из файла
	def show_data_file(self):
		with open(self.address_file, encoding="utf-8") as file:
			#строка ниже обновляет текстовое поле
			self.__set_text()
			self.show_name_file()
			for item in file:
				self.user_text.insert(tk.END, item)
		self.start_but["state"], self.save_but["state"] = "enable", "enable"

	#выводит расшифрованные данные из списка
	def show_data(self):
		self.__set_text()
		self.show_name_file()
		for item in self.crypto_data:
			self.user_text.insert(tk.END, item)

	def show_name_file(self):
		self.name = self.name.split("/")[-1]
		self.user_text.insert(tk.END, "\t\t\tНазвание файла: " + self.name + '\n')
			
	#все функции ниже срабатывают от кнопок и комбобокса
	def save_file(self):
		self.user_text.delete(1.0, 2.0)
		loader(self.user_text.get(1.0, tk.END), self.address_file)
		self.__set_text()
		self.user_text.insert(tk.END, "\t\tДАННЫЕ УСПЕШНО СОХРАНЕНЫ В ФАЙЛ " + self.name)
		self.start_but["state"], self.save_but["state"] = "disabled", "disabled"

	#открывает меню выбора файла для открытия	
	def get_address_file(self):
		self.address_file = fd.askopenfile()
		#если была нажата кнопка, но не выбран файл, то
		#присваивается имя None и чтобы оно не выводилось:
		if self.address_file is not None:
			self.address_file = str(self.address_file).split("'")[1]
			self.name, self.status_open_file = self.address_file, True
			self.show_name_file() 
			self.show_data_file()

	#открывает меню для создания файла
	def create_file(self):
		if self.status_open_file is False:
			self.address_file = fd.asksaveasfile()
		else:
			self.address_new_file = fd.asksaveasfile()
		#тут та же история
		if self.address_new_file is not None:
			self.address_file = self.address_new_file
			self.address_file = str(self.address_file).split("'")[1]
			self.name = self.address_file
			self.__set_text()
			self.show_name_file()
			self.start_but["state"], self.save_but["state"] = "enable", "enable"

	#управляет шифровкой и расшифровкой данных
	def start_crypto(self):
		#шифровка
		if self.combo_win.current() == 0:
			self.user_text.delete(1.0, 2.0)
			self.user_text = self.user_text.get(1.0, tk.END)
			self.user_text = self.user_text.split("|")
			self.user_text = encrypto(self.user_text)
			self.crypto_data = [str(item) for item in self.user_text]
			self.show_data()
		#расшифровка
		elif self.combo_win.current() == 1:
			#если не сможет расшифровать значит данные ещё не зашифрованы
			try:
				self.user_text.delete(1.0, 2.0)
				self.user_text = self.user_text.get(1.0, tk.END)
				#self.user_text - это большая строка
				self.user_text, self.crypto_data = decrypto(self.user_text), list()
				for item in self.user_text:
					if item != '':
						self.crypto_data.append(item)
				self.show_data()
			except:
				self.__set_text()
				self.user_text.insert(tk.END, "\t\tДАННЫЕ ПОКА НЕ ЗАШИФРОВАНЫ!")
				self.start_but["state"], self.save_but["state"] = "disabled", "disabled"

	"""КОНТЕКСТНОЕ МЕНЮ"""
	def show_popup(self, event):
		"""Выводит контекстное меню"""
		self.menu.post(event.x_root, event.y_root)

	def cut_text(self):
		"""Копирует и удаляет выделенный текст"""
		self.copy_text()
		self.delete_text()

	def copy_text(self):
		"""Копирует выделенный текст"""
		selection = self.user_text.tag_ranges(tk.SEL)
		if selection:
			self.clipboard_clear()
			self.clipboard_append(self.user_text.get(*selection))

	def paste_text(self):
		"""Вставляет текст из буфера обмена"""
		self.user_text.insert(tk.INSERT, self.clipboard_get())

	def delete_text(self):
		"""Удаляет выделенный текст"""
		selection = self.user_text.tag_ranges(tk.SEL)
		if selection:
			self.user_text.delete(*selection)
