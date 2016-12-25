import sqlite3
import base64
import validation
import datetime
import time
conn = sqlite3.connect('database.db')
c = conn.cursor()

class Client(object):

	def __init__(self):
		self.client_id = 0
		self.tries = 0
		self.session = False
		self.balance = 0

	def getUser(self, ag, acc):
		self.ag = ag
		self.acc = acc
		for row in c.execute('SELECT id, first_name as NAME FROM CLIENTS WHERE agency = ? and account = ?', (ag, acc)):
			if (len(row) is not None):
				self.client_id = row[0]
				self.name = row[1]
				conn.commit()		
				return True	
		print "SISTEMA: Desculpe, nao foi possivel encontrar seu usuario, por favor tente novamente\n"						
		conn.commit()					
		return False
	

	def login(self, passw):
		passw = base64.b64encode(passw)
		for row in c.execute('SELECT * FROM CLIENTS WHERE id = ? and password = ?', (self.client_id, passw)):
			if (len(row) is not None):				
				self.session = True				
				conn.commit()		
				return True			
		conn.commit()	
		self.tries = self.tries + 1
		print "Desculpe, sua senha nao corresponde com a cadastrada no sistema | {} Tentativas\n".format(self.tries)
		return False

	def logout(self):
		self.session = False
		return True

	def createUser(self, n, fn, ag, acc, passw):
		passw = base64.b64encode(passw)
		try:
			c.execute('INSERT INTO CLIENTS(first_name, full_name, agency, account, password) VALUES (? , ? ,  ? ,  ? , ?)', (n, fn, ag, acc, passw))
			conn.commit()
		except sqlite3.IntegrityError as err:
			print "ERRO: USUARIO OU CONTA JA EXISTENTES, RETORNANDO A PAGINA INICIAL"
			return False	


	def print_extract(self):
		print "\t$$$$$$$$$$ EXTRATO DE ATIVIDADES $$$$$$$$$$"
		for row in c.execute("SELECT t.id, o.description, t.value, t.timestamp FROM TRANSACTIONS t, clients c, operations o WHERE t.client_id = c.id and o.op_number = t.operation_id and c.id = ? ; ", (str(self.client_id))):
			print ("""		
			# {}			
			OPERACAO: {}			
			VALOR: R${},00
			DATA: {}
		  ---------------------------------""".format(row[0], row[1], row[2], row[3]))	
		print "\t$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
		return True


	def print_balance(self): #OPCAO 1
		self.balance = self.getBalance()
		print "\n\t \t \tSEU SALDO ATUAL E DE: R${},00\n".format(self.balance)
		

	def deposit(self): #OPCAO 3
		self.balance = self.getBalance()
		val = False
		while val is False:
			ans = False
			val = raw_input("QUAL O VALOR DESEJA DEPOSITAR? \n>>")
			val = validation.checkInteger(val, 1, 3)
		self.balance += val
		c.execute('UPDATE CLIENTS SET balance = ? WHERE id = ? ', (str(self.balance), str(self.client_id)))
		self.updateActivities(self.client_id, 3, val)		#Activitie number, value
		conn.commit()
		print "\nO VALOR DE R${},00 FOI DEPOSITADO COM SUCESSO".format(val)
		return True


	def deposit_third(self): #OPCAO 4
		val = False
		ag = False
		acc = False
		while ag is False:
			ag = raw_input("INSIRA A AGENCIA PARA REALIZAR O DEPOSITO \n>>")
			ag = validation.checkInteger(ag, 1, 4)		
		while acc is False:
			acc = raw_input("INSIRA A CONTA DA PESSOA NA QUAL DESEJA REALIZAR O DEPOSITO \n>>")
			acc = validation.checkInteger(acc, 1, 4)	

		c.execute("SELECT id, full_name FROM CLIENTS WHERE agency = ? and account = ? ;", ( str(ag), str(acc) ))
		data = c.fetchone()
		if data is None:
				print 'CONTA SOLICITADA NAO EXISTE!'
				return False
		else:
			dest_id = data[0]
			dest_name = data[1]
			

		while val is False:
			val = raw_input("QUAL VALOR DESEJA DEPOSITAR? \n>>")
			val = validation.checkInteger(val, 1, 3)
		
		ans = False				
		while ans is False:
			ans = raw_input("Deseja depositar o valor de R${},00 para {} ?\n 1) SIM \n 2) NAO\n>>".format(val, dest_name))
			ans = validation.checkInteger(ans, 1, 1)		
			if ans == 1:		
				print "Valor depositado com sucesso"
				self.updateActivities(dest_id, 4, val)
				return True
			elif ans == 2:
				print "Operacao cancelada pelo usuario"
				return False
			else:
				print "Valor invalido, Escolha uma opcao novamente"
				ans = False		


	def transfer(self): #OPCAO 5
		val = False
		ag = False
		acc = False
		while ag is False:
			ag = raw_input("INSIRA A AGENCIA PARA REALIZAR O DEPOSITO \n>>")
			ag = validation.checkInteger(ag, 1, 4)		
		while acc is False:
			acc = raw_input("INSIRA A CONTA DA PESSOA NA QUAL DESEJA REALIZAR O DEPOSITO \n>>")
			acc = validation.checkInteger(acc, 1, 4)	

		c.execute("SELECT id, full_name, balance FROM CLIENTS WHERE agency = ? and account = ? ;", ( str(ag), str(acc) ))
		data = c.fetchone()
		if data is None:
				print 'CONTA SOLICITADA NAO EXISTE!'
				return False
		else:
			dest_id = data[0]
			dest_name = data[1]			
			dest_balance = data[2]			

		while val is False:
			val = raw_input("QUAL VALOR DESEJA TRANSFERIR? \n>>")
			val = validation.checkInteger(val, 1, 3)

		ans = False				
		while ans is False:
			ans = raw_input("Deseja transferir o valor de R${},00 para {} ?\n 1) SIM \n 2) NAO\n>>".format(val, dest_name))
			ans = validation.checkInteger(ans, 1, 1)		
			if ans == 1:		
				self.balance -= val				
				if (self.balance < 0):
					print "NAO PERMITIDO! VOCE NAO TEM SALDO SUFICIENTE"
					return False
				dest_balance += val				
				c.execute('UPDATE CLIENTS SET balance = ? WHERE id = ? ', (str(self.balance), str(self.client_id)))
				c.execute('UPDATE CLIENTS SET balance = ? WHERE id = ? ', (str(dest_balance), str(dest_id)))
				conn.commit()
				self.updateActivities(dest_id, 5, val)
				print "Valor transferido com sucesso"				
				return True
			elif ans == 2:
				print "Operacao cancelada pelo usuario"
				return False
			else:
				print "Valor invalido, Escolha uma opcao novamente"
				ans = False		


	def withdraw(): #OPCAO 6
		print "QUAL O VALOR DESEJA SACAR?"

	def getBalance(self):
		for row in c.execute('SELECT balance FROM CLIENTS WHERE id = ? ', (str(self.client_id))):
			return row[0]
	
	def updateActivities(self, destination, operation, value):
		c.execute('INSERT INTO TRANSACTIONS(client_id, destination_id, operation_id, value) VALUES (?, ?, ?, ?)', (str(self.client_id), str(destination), str(operation), str(value)))
		return True

		

