import sys
import traceback
import threading

import tornado
import tornado.web
import tornado.gen
from tornado.ioloop import IOLoop
from objects import Context

class asyncRequestHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self, *args, **kwargs):
		try:
			yield tornado.gen.Task(runBackground, (self.asyncGet, tuple(args), dict(kwargs)))
		finally:
			if not self._finished:
				self.finish()


	@tornado.web.asynchronous
	@tornado.gen.engine
	def post(self, *args, **kwargs):
		try:
			yield tornado.gen.Task(runBackground, (self.asyncPost, tuple(args), dict(kwargs)))
		finally:
			if not self._finished:
				self.finish()

	def asyncGet(self, *args, **kwargs):
		self.send_error(405)

	def asyncPost(self, *args, **kwargs):
		self.send_error(405)

	def getRequestIP(self):
		"""
		get the real ip behind cloudflare
		"""
		if "CF-Connecting-IP" in self.request.headers:
			return self.request.headers.get("CF-Connecting-IP")
		elif "X-Forwarded-For" in self.request.headers:
			return self.request.headers.get("X-Forwarded-For")
		else:
			return self.request.remote_ip

	def runThread(self, fun, args, kwargs):
		fun(*args, **kwargs)
		if not self._finished:
			self.finish()
	
	def redirect(self, path):
		self.set_status(302)
		self.set_header("Location", path)

	@property
	def isLoggedIn(self):
		Auth = self.get_secure_cookie("Authorization")
		id = Context.mysql.fetch("Select uid from tokens where token = %s", Auth)
		if id is None:
			return False
		else:
			return True
	
	@property
	def userContext(self):
		if not self.isLoggedIn:
			return None
		else:
			return Context.mysql.fetch("SELECT u.id, u.username, u.first_name, u.last_name, u.email, u.type FROM airmod.tokens t join users u on t.uid = u.id where t.token = %s;", self.get_secure_cookie("Authorization"))
		

def runBackground(data, callback):
	"""
	Run a function in the background.
	Used to handle multiple requests at the same time

	:param data: (func, args, kwargs)
	:param callback: function to call when `func` (data[0]) returns
	:return:
	"""
	func, args, kwargs = data
	def _callback(result):
		IOLoop.instance().add_callback(lambda: callback(result))
	Context.pool.apply_async(func, args, kwargs, _callback)

def checkArguments(arguments, requiredArguments):
	"""
	Check that every requiredArguments elements are in arguments

	:param arguments: full argument list, from tornado
	:param requiredArguments: required arguments list
	:return: True if all arguments are passed, False if not
	"""
	for i in requiredArguments:
		if i not in arguments:
			return False
	return True

def printArguments(t):
	"""
	Print passed arguments, for debug purposes

	:param t: tornado object (self)
	"""
	msg = "ARGS::"
	for i in t.request.arguments:
		msg += "{}={}\r\n".format(i, t.get_argument(i))
	#log.debug(msg)

