import re

def checkString(tested_string, min, max):
	if (len(tested_string) < min) or (len(tested_string) >= max):
		print "Desculpe, quantidade de caracteres invalida, tente novamente \n"
		return False
	tested_string = tested_string.replace(" ", "")
	res = re.match("[A-Z]|[a-z]", tested_string)
	if (res is None):
		print 'Desculpe, os caracteres digitados sao invalidos. Tente novamente \n\n'
		return False
	return True

def checkInteger(value, min, max):	
	if (len(value) < min) or (len(value) > max):
		print "Desculpe, quantidade de caracteres invalida, tente novamente\n"
		return False	
	try:
		value = int(value)
		return value
	except ValueError:
		print 'Desculpe, os caracteres digitados sao invalidos. Tente novamente \n\n'
		return False
	

def checkPassword(pass1):
	if (len(pass1) < 3):
		print "Senha muito curta! tente novamente\n"
		return False
	return True

	