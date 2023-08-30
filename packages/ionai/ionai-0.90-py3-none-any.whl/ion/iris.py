#
# [name]    ion.iris.py
# [comment] library to connect to InterSystems IRIS database
#
# Written by Yoshikazu NAKAJIMA
#

import irisnative


_TMDUBMI_IRIS_IP = '192.168.0.47'
_TMDUBMI_IRIS_PORT = 1972
_TMDUBMI_NAMESPACE = 'FS'
_TMDUBMI_USERNAME = '_SYSTEM'
_TMDUBMI_PASSWORD = 'bmi-2718'

_DEFAULT_IRIS_IP = _TMDUBMI_IRIS_IP
_DEFAULT_IRIS_PORT = _TMDUBMI_IRIS_PORT
_DEFAULT_IRIS_NAMESPACE = _TMDUBMI_NAMESPACE
_DEFAULT_IRIS_USERNAME = _TMDUBMI_USERNAME
_DEFAULT_IRIS_PASSWORD = _TMDUBMI_PASSWORD

class iris():
	_classname = 'ion.iris'

	def __init__(self):
		self._connection = None
		self._ip = _DEFAULT_IRIS_IP
		self._port = _DEFAULT_IRIS_PORT
		self._namespace = _DEFAULT_IRIS_NAMESPACE
		self._username = _DEFAULT_IRIS_USERNAME
		self._password = _DEFAULT_IRIS_PASSWORD

	@classmethod
	@property
	def classname(cls):
		return cls._classname

	@property
	def connection(self):
		return self._connection

	"""
	@connection.setter
	def connection(self, c):
		self._connection = c
	"""

	@property
	def ip(self):
		return self._ip

	@ip.setter
	def ip(self, ip_):
		self._ip = ip_

	@property
	def port(self):
		return self._port

	@port.setter
	def port(self, p):
		self._port = p

	@property
	def namespace(self):
		return self._namespace

	@namespace.setter
	def namespace(self, ns):
		self._namespace = ns

	@property
	def ns(self):
		return self.namespace

	@ns.setter
	def ns(self, ns_):
		self.namespace = ns_

	@property
	def username(self):
		return self._username

	@username.setter
	def username(self, name):
		self._username = name

	@property
	def userid(self):
		return self.username

	@userid.setter
	def userid(self, name):
		self.username = name

	@property
	def user(self):
		return self.username

	@user.setter
	def user(self, name):
		self.username = name

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, pw):
		self._password = pw

	@property
	def pw(self):
		return self.password

	@pw.setter
	def pw(self, pw_):
		self.password = pw_

	def open(self):
		self._connection = irisnative.createConnection(_IRIS_IP, _IRIS_PORT, _TMDUBMI_NAMESPACE, _TMDUBMI_USERNAME, _TMDUBMI_PASSWORD)
		iris_native = irisnative.createIris(self._connection)

	def close(self):
		self._connection.close()
		self._connection = None

	def connected(self):
		return (self._connection is not None)

	def not_connected(self):
		return (self._connection is None)

	def get_semantics(self, )
