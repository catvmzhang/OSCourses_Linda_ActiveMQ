import stomp
import time
import ast
import Queue

class systemTuple():
	def __init__(self):
		self.tupleList = []
		self.waitingQueue = Queue.Queue()
		self.var = dict()
	
	def append_by_string(self, tupleString):
		thisTuple = eval(tupleString)
		self.tupleList.append(thisTuple)
	
	def show_all_tuple(self):
		print('[all tuple in system]')
		if not self.tupleList:
			print('<EMPTY>')
		else:
			for thisTuple in self.tupleList:
				print('%s' % (thisTuple,) )

	def toWait(self, clientQueue, tupleString, toRemove):
		thisTuple = eval(tupleString)
		qItem = {'clientQueue':clientQueue, 'tuple':thisTuple, 'toRemove':toRemove};
		self.waitingQueue.put(qItem)

	def check_waitingQueue(self):
		tempQueue = Queue.Queue()
		while not self.waitingQueue.empty():
			qItem = self.waitingQueue.get()
			returnTuple = self.check_tupleList(qItem.get('tuple'))
			if returnTuple:
				tupleString = self.tuple_to_string(returnTuple)
				conn.send(destination=qItem.get('clientQueue'), body=tupleString )
				print('[RESULT]%s '% (returnTuple,))
				if qItem.get('toRemove'):
					self.tupleList.remove(returnTuple)
			else:
				tempQueue.put(qItem)
		self.waitingQueue = tempQueue
	
	def check_tupleList(self, askTuple):
		for thisTuple in self.tupleList:
			checkResult = True
			tempVal = dict()
			for i in range(0, len(askTuple)):
#				print('[ask]%s [list]%s' % (askTuple[i], thisTuple[i]))
				if type(askTuple[i]) == str:
					if askTuple[i].startswith('?'):
						tempVal[askTuple[i][1:]] = thisTuple[i]
						continue		
				if not askTuple[i] == thisTuple[i]:
					checkResult = False
					break
			if checkResult:
				self.var.update(tempVal)
				print('[val]%s' % (self.var,))
				return thisTuple
		return None

	def tuple_to_string(self, thisTuple):
		res = '('
		for i in range(0, len(thisTuple)):
			if type(thisTuple[i]) == int:
				res = res + str(thisTuple[i])
			else:
				res = res + '"' + thisTuple[i] + '"'
			if not i == len(thisTuple)-1:
				res = res + ', '
		res = res + ')'
		return res

	def replaceVar(self, tupleString):
		res = tupleString
		for key, val in self.var.items():
			if type(val) == str:
				val_s = '\'' + val + '\''
			else:
				val_s = str(val)
#			print(key, val_s)
			res = res.replace(str(key), str(val_s))
		return res


class lindaListener(stomp.ConnectionListener):
	def __init__(self, conn):
		self.conn = conn
	
	def on_message(self, headers, cmd):
		operation = cmd.split(" ")[0]
		tupleString = cmd.split(" ",1)[1]
		tupleString = system.replaceVar(tupleString)
		print('\n[operation]%s [tuple]%s' % (operation, tupleString))
		if operation == 'in':
			clientQueue = self.get_ClientQueue(headers)
			self._in(clientQueue, tupleString)
		elif operation == 'out':
			self.out(tupleString)
		elif operation == 'read':
			clientQueue = self.get_ClientQueue(headers)
			self.read(clientQueue, tupleString)
		else:
			print('undefined cmd')
		system.show_all_tuple()

	def get_ClientQueue(self, headers):
		clientInfo = ast.literal_eval(headers.get('header'))
		return clientInfo.get('clientQueue')

	def _in(self, clientQueue, tupleString):
		system.toWait(clientQueue, tupleString, toRemove=True)
		system.check_waitingQueue()

	def out(self, tupleString):
		system.append_by_string(tupleString)
		system.check_waitingQueue()
	
	def read(self, clientQueue, tupleString):
		system.toWait(clientQueue, tupleString, toRemove=False)
		system.check_waitingQueue()



system = systemTuple()

conn = stomp.Connection([('140.113.194.138', 61613)])
conn.start()
conn.connect('admin', 'admin')

conn.set_listener('', lindaListener(conn)) 
conn.subscribe(destination='linda/cmd', id=1, ack='auto')
while 1:
	time.sleep(10)
