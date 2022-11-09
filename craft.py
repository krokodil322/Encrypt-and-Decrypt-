from hashlib import sha256
from cryptography.fernet import Fernet

def craft_password(password:str = "qwerty") -> str:
	"""Крафт пароля в виде хэша, шоб никакая гадина его не подглядела в файле"""
	return sha256(password.encode()).hexdigest()

def generate_key_cipher() -> str:
	"""Если надо поменять ключ шифрования"""
	return Fernet.generate_key()

if __name__ == "__main__":
	print(craft_password())
	print(generate_key_cipher())

	



	

