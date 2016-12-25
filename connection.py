import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("""
	CREATE TABLE IF NOT EXISTS CLIENTS(
	id INTEGER PRIMARY KEY, 
	first_name TEXT NOT NULL, 
	full_name TEXT NOT NULL, 	
	password TEXT NOT NULL,
	agency INTEGER NOT NULL UNIQUE,
	account INTEGER NOT NULL UNIQUE,
	balance INTEGER DEFAULT 0,
	FOREIGN KEY(id) REFERENCES TRANSACTIONS(client_id)
);
""")

c.execute("""
	CREATE TABLE IF NOT EXISTS TRANSACTIONS(
	id INTEGER PRIMARY KEY, 
	client_id INTEGER NOT NULL,
	destination_id INTEGER,
	operation_id INTEGER NOT NULL,
	value INTEGER,
	timestamp DATE DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME'))
);
""")

c.execute("""	
CREATE TABLE IF NOT EXISTS OPERATIONS(	
	op_number INTEGER NOT NULL UNIQUE,
	description TEXT NOT NULL UNIQUE,
	FOREIGN KEY(op_number) REFERENCES TRANSACTIONS(operation_id)
);
""")

c.execute("""	
INSERT or REPLACE INTO OPERATIONS (op_number, description) VALUES 
('3', 'DEPOSITO NA PROPRIA CONTA'), 
('4', 'DEPOSITO EM OUTRA CONTA'), 
('5', 'TRANSFERENCIA'), 
('6', 'SAQUE') 		
""")

conn.commit()
conn.close()