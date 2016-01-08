import MySQLdb as mdb

class MySQLreq:
	def __init__(self, params): # constructor, which connects to db
		self.HOST = params[0]
		self.USER = params[1]
		self.PASS = params[2]
		self.DB = params[3]
		db = mdb.connect(self.HOST,self.USER,self.PASS,self.DB)
		self.cur = db.cursor()

	def getData(self, q):  # make request to DB and return result list
		self.cur.execute(q)
		return self.cur.fetchall()
	def setData(self,q):
		self.cur.execute(q)
		self.cur.execute("COMMIT;")			