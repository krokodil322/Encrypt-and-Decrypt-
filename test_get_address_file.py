from tkinter import filedialog as fd, Tk

def get_address_file() -> str:
	"""Открывает окно выбора файла, после выбора возвращает адрес файла"""
	return str(fd.askopenfile()).split("'")[1]

def get_name_file(address_file: str) -> str:
	"""Из адреса получает имя файла"""
	return address_file.split("/")[-1]

if __name__ == "__main__":
	window = Tk()
	window.geometry("400x100")
	address_file = get_address_file()
	print(f"Полный адрес файла:\n{address_file}\nИмя файла: {get_name_file(address_file)}")
	window.mainloop()