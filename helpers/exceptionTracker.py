import sys
import traceback
from functools import wraps
from objects import Context
from helpers import console

from common.log import logUtils as log


def trackExceptions(moduleName=""):
	def _trackExceptions(func):
		def _decorator(request, *args, **kwargs):
			try:
				response = func(request, *args, **kwargs)
				return response
			except:
				if Context.debug:
					console.error("Unknown error{}!\n\n{}\n{}".format(" in "+moduleName if moduleName != "" else "", sys.exc_info(), traceback.format_exc()))
				else:
					console.error("An error has occured trying to handle {}".format(moduleName if moduleName != "" else " a request"))
					Context.errorLog.write("======================\n{}\n{}\n\n\n".format(sys.exc_info(), traceback.format_exc()))
		return wraps(func)(_decorator)
	return 