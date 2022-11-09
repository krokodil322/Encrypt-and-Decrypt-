from tkinter_window_form import InputPassword, MainApp

if __name__ == "__main__":
	window_for_pass = InputPassword()
	window_for_pass.mainloop()

	if window_for_pass.autorization_status:
		window_for_app = MainApp()
		window_for_app.mainloop()

# window_for_app = MainApp()
# window_for_app.mainloop()