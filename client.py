import stomp
import sys
import time

class lindaClient:
	def __init__(self, clientName):
		self.conn = stomp.Connection([('140.113.194.138', 61613)])
		self.conn.start()
		self.conn.connect('admin', 'admin')
		self.waitingQueue = 'client/' + clientName
		self.conn.subscribe(destination=self.waitingQueue, id=1)
		self.conn.set_listener('', self)

	def cmd(self, cmd):
		operation = cmd.split(" ")[0]
		tupleString = cmd.split(" ",1)[1]
		print('[operation]%s [tuple]%s\n' % (operation, tupleString))
		if operation == 'in':
			self.sendCmd(cmd)
			self.wait()
		elif operation == 'out':
			self.sendCmd(cmd)
		elif operation == 'read':
			self.sendCmd(cmd)
			self.wait()
		else:
			print('undefined cmd')
	
	def sendCmd(self, cmd):
		self.conn.send(destination='linda/cmd', body=cmd, header={'clientQueue': self.waitingQueue})
	
	def wait(self):
		self.waiting = True
		while self.waiting:
			time.sleep(1)
	
	def on_message(self, headers, message):
		self.waiting=False
		print(message)		


if not len(sys.argv) == 2:
	print('[usage] python client.py <clientName>')
	sys.exit()

clientName = sys.argv[1]
client = lindaClient(clientName)

while(1):
	cmd = raw_input('>> ')
	client.cmd(cmd)

