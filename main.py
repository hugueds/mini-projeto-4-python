#!/usr/bin/env python

import os, time, getpass
from colors import bcolors as colors
import connection
import validation
import Client

#Auxiliar para limpar a tela do terminal
def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

#Mensagem da tela inicial
def welcome():
	print ("""
		---------- BEM VINDO AO BUGGINHO BANKING! ---------

				$$$$$$$$$$$$$$$$$$$$$                                               
				$       $  $        $                                                 
				$       $  $        $                                                 
				$      $$$$$$$$     $                                                 
				$    $  $  $    $   $                                                 
				$   $   $  $        $                                                 
				$   $   $  $        $                                                                                            
				$    $$$$$$$$$$     $                                                                                         
				$       $  $    $   $                                                                                              
				$       $  $    $   $                                                 
				$   $   $  $   $    $                                                 
				$    $$$$$$$$$$     $                                                 
				$       $  $        $                                                 
				$       $  $        $                                                 
				$$$$$$$$$$$$$$$$$$$$$ 

		---------------------------------------------------

		COMO PODEMOS AJUDA-LO?
		  """)

#Home page da aplicacao
def home():	
	ans = True 
	while ans:
		print ("""
	DIGITE O NUMERO CORRESPONDENTE PARA REALIZAR AS OPERACOES

	1) ACESSAR CONTA BANCARIA
	2) CRIAR CONTA
	3) SAIR

	PRESSIONE CRTL+C A QUALQUER MOMENTO PARA RETORNAR A TELA INICIAL OU SAIR
		""")
		try:
			ans = int(raw_input(">>"))
			if (ans < 1) or (ans > 3):
				raise ValueError
		except ValueError:
			print "Por ,favor, informe um numero valido"
			continue
		if (ans == 1):
			ans = False
			validateLogin()
		elif (ans == 2):
			ans = False
			createAccount()		
		elif (ans == 3):
			ans = True
			leave()
	
#Valida login antes de acessar a conta	
def validateLogin():
	clear()
	ag = False	
	acc = False
	val = False
	try :
		while True:
			while val is False:
				ag = raw_input('######  Informe sua agencia ####### \n>>')	
				val = validation.checkInteger(ag, 1, 4)
			val = False
			while val is False:
				acc = raw_input('###### Informe o numero de sua conta ####### \n>>')
				val = validation.checkInteger(acc, 1, 4)
			val = False
			c = Client.Client()
			check = c.getUser(ag, acc)
			if not(check):
				clear()				
				del c
				continue
			else:
				clear()
				print "BEM VINDO {} \t --- AGENCIA {} --- \t --- CONTA {} ---".format(c.name.upper(), c.ag, c.acc)
				while val is False:
					passw = getpass.getpass('DIGITE SUA SENHA: ')
					val = c.login(passw)
				accessAccount(c)

	except KeyboardInterrupt:
		print "\nCRTL+C PRESSIONADO"		
		leave()



#com login validado, informa as opcoes disponiveis para o cliente
def accessAccount(c):		
	while True:
		print ("""
		DIGITE UM NUMERO PARA PROSSEGUIR COM AS OPERACOES

		1) CONSULTAR SEU SALDO
		2) EXTRADO DAS ULTIMAS ATIVIDADES
		3) DEPOSITO NA PROPRIA CONTA
		4) DEPOSITO NA CONTA DE OUTRO TITULAR
		5) TRANFERENCIA ENTRE CONTAS
		6) SAQUE EM DINHEIRO 
		7) LOG OUT 
			""")
		while True:
			ans = raw_input(">> ")
			ans = validation.checkInteger(ans, 1, 1)
			if (ans < 1) or (ans > 7):
				clear()
				print "Por favor, selecione uma opcao valida\n"
				break
			if (ans == 1):
				clear()
				c.print_balance()
			elif (ans == 2):
				clear()
				c.print_extract()
			elif (ans == 3):
				clear()
				c.deposit()
			elif (ans == 4):
				clear()
				c.deposit_third()
			elif (ans == 5):
				clear()
				c.transfer()
			elif (ans == 7):
				c.logout()
				clear()
				main()
			else:
				break
			break


def createAccount(): #REALIZAR VALIDACAO DOS DADOS ANTES DE INSERIR NO BANCO
	ans = True
	name = False
	lastname = False
	fullname = False
	agency = False
	account = False
	passw = False
	val = False
	while ans:
		clear()
		print (""" 
PARA SE CADASTRAR EM NOSSO BANCO SERAO NECESSARIOS: NOME, SOBRENOME, AGENCIA, CONTA E SENHA

DIGITE-OS CONFORME SAO REQUERIDOS
			""")
		while val is False:
			name = raw_input("Informe seu nome: ")
			val = validation.checkString(name, 3, 20)
		val = False
		while val is False:			
			lastname = raw_input("Informe seu sobrenome: ")
			val = validation.checkString(lastname, 3, 20)
		fullname = '{} {}'.format(name, lastname)
		val = False
		while val is False:
			agency = raw_input("Informe sua agencia: ")
			val = validation.checkInteger(agency, 3, 4)
		val = False
		while val is False:
			account = raw_input("Informe o numero de sua conta: ")
			val = validation.checkInteger(account, 3, 10)
		val = False
		while val is False:
			passw = getpass.getpass("Informe sua senha (minimo 3 Digitos): ")
			val = validation.checkPassword(passw)
			if (not val):
				continue
			passw2 = getpass.getpass("Repita a senha, por favor: ")
			if (passw != passw2):
				val = False
				print "Senhas nao coecidem, preencha novamente\n"
				continue

		print ("""
SEUS DADOS SAO
	NOME: {}
	SOBRENOME: {}
	AGENCIA: {}
	CONTA: {}
		 """.format(name, lastname, agency, account))
		ans = raw_input("Confirma seus dados? \n 1)SIM \n 2)NAO, RETORNAR AO MENU PRINCIPAL \n>> ")
		ans = validation.checkInteger(ans, 1, 1)
		if (ans == 2):
			main()
		elif(ans == 1):
			u = Client.Client()
			res = u.createUser(name, fullname, agency, account, passw)
			if (res):
				print "Usuario criado com sucesso!, retornando a pagina inicial"
				time.sleep(5)
			del u	
			main()

def leave():
	ans = raw_input("DESEJA SAIR?\n 1)SIM \n 2)RETORNAR A TELA PRINCIPAL\n>>")
	ans = validation.checkInteger(ans, 1, 1)
	if (ans == 1):
		print "$$$$$$$$$$$       ATE A PROXIMA AMIGUINHO!       $$$$$$$$$$$\n"
		exit()
	elif(ans == 2):
		main()
	


def main():
	clear()
	welcome()
	home()		


#Loop inicial
if __name__ == "__main__":

	try:
		main()

	except KeyboardInterrupt:
		clear()		
		leave()
		

		
	