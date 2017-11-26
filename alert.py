import random, socket, time

#Very basic wrapper class to send rcon data to a JA server
class Rcon(object):
	MAX_SVSAY_LEN = 140
	MAX_TRY = 3
	TRY_SLEEP = 3

	def __init__(self, iip, iport, ipass):
		self.rconSocket = None
		self.rconIP = iip
		self.rconPort = iport
		self.rconPass = ipass

	def connect(self):
		try:
			self.rconSocket.close()
		except:
			pass

		self.rconSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.rconSocket.settimeout(1)
		self.rconSocket.connect((self.rconIP, self.rconPort))

	def _send(self, payload, buffer_size=1024):
		tries = 1
		while tries != Rcon.MAX_TRY:
			try:
				self.connect()
				self.rconSocket.send(payload)
				self.rconSocket.recv(buffer_size)
				self.rconSocket.close()
				return True
			except socket.timeout:
				tries += 1
				time.sleep(Rcon.TRY_SLEEP)
			except socket.error:
				return False

	def say(self, msg):
		if len(msg) >= Rcon.MAX_SVSAY_LEN:
			self._send("\xff\xff\xff\xffrcon %s say %s" % (self.rconPass, msg), 2048)
		else:
			self._send("\xff\xff\xff\xffrcon %s svsay %s" % (self.rconPass, msg))

#Config
MY_PREFIX = "[^2ALERT^7] "
MY_ALERTS = ["Use !rank to view your rank", "Use !top to view the top players", "Use !rtv to rock the vote"]
MY_IP = "localhost"
MY_PORT = 29070
MY_PASS = "some rcon password"

#Run
rcon = Rcon(MY_IP, MY_PORT, MY_PASS)
rcon.say(MY_PREFIX + random.choice(MY_ALERTS))
