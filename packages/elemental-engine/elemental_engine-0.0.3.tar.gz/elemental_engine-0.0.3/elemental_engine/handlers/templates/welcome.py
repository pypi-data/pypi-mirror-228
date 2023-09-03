class template:
	header = '''<!DOCTYPE html>
	<html>
	<head>
	    <title>Elemental - Welcome</title>
	</head>
	<body>
	'''
	footer = '''
	</body>
	</html>
	'''

	def __init__(self,	username: str, device_auth_link: str):
		self.username = username
		self.device_auth_link = device_auth_link

	def pt_br(self):
		self.mailbody = f"""
		<h1>
		Olá {self.username} 
		Verificamos um novo acesso à sua conta por um novo dispositivo, para autorizar o acesso,
		clique no botão abaixo:
		</h1>
            <td>
                <a href="{self.device_auth_link}" target="_blank" style="display: inline-block; background-color: #007bff; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Habilitar Dispositivo</a>
            </td>
		"""

		return self.header + self.mailbody + self.footer