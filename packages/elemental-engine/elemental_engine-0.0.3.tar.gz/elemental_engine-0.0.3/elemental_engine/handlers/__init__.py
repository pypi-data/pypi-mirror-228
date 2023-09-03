import base64
import smtplib
import uuid
import random
from email.mime.text import MIMEText

from bson import ObjectId
from fastapi import Header
from fastapi import HTTPException, Cookie, Request, Header

from elemental_engine.config import app_config
from elemental_engine.collections.email.smtp_config import smtp_config

class email:

	def __init__(self, smtp_email, smtp_password, smtp_server, smtp_port, sender=None, destination=None):
		self.sender = sender
		self.destination = destination
		self.smtp_email = smtp_email
		self.smtp_password = smtp_password
		self.smtp_server = smtp_server
		self.smtp_port = smtp_port

	def check_config(self):
		try:
			# Connect to the SMTP server
			smtpServer = smtplib.SMTP(self.smtp_server, int(self.smtp_port))
			smtpServer.starttls()
			try:
				smtpServer.login(self.smtp_email, password().decrypt(self.smtp_password))
			except:
				raise Exception("Your smtp looks fine, maybe the problem is on your login information.")

			return True

		except Exception as e:
			raise Exception(f"Error registering e-mail: {e}")

	def send_email(self, subject, message):
		msg = MIMEText(message)
		msg['From'] = self.sender
		msg['To'] = self.destination
		msg['Subject'] = subject

		try:
			# Connect to the SMTP server
			smtpServer = smtplib.SMTP(host=self.smtp_server, port=self.smtp_port)
			smtpServer.starttls()
			# Login to the server
			smtpServer.login(self.smtp_email, self.smtp_password)
			# Send the email
			print(smtpServer.sendmail(self.smtp_email, self.destination, msg.as_string()))
			return {'message': 'E-mail sent successfully.'}

		except Exception as e:
			raise Exception(f"Error sending email: {e}")

class token:

	def generate(length: int):
		token = uuid.uuid4().bytes
		return base64.urlsafe_b64encode(token).rstrip(b'=').decode('utf-8')

	def auth(self, app_key: str = Header(title='Application secret obtained registering.', example=app_config.demo_key), app_secret: str = Header(title='Application secret obtained registering.', example=app_config.demo_secret)):

		valid_token = None

		valid_refresh_token_condition = {
			"_id": ObjectId(app_key),
			'app_secret': str(app_secret)
		}

		valid_user = smtp_config().find_one(valid_refresh_token_condition)

		if valid_user is not None:
			result = valid_user
			return result
		else:
			raise HTTPException(status_code=401, detail='Invalid access information.')

class password:

	def encrypt(self, string: str):

		def validFloat(digit, randomIntegerTimes):
			randomIntegerTimes += 1
			multiplyFactor = random.randint(2, 50)
			floatValue = ord(digit) / multiplyFactor
			floatActualLength = len(str(floatValue).replace('.', ''))
			floatMaxLength = 5
			if floatActualLength > floatMaxLength:
				return False
			else:
				return floatValue, str(randomIntegerTimes), multiplyFactor

		def retrieveCode(digit):
			randomIntegerTimes = 0
			seedValue = ord(digit)
			random.seed(seedValue)
			floatValue = validFloat(digit, randomIntegerTimes)
			while not floatValue:
				floatValue = validFloat(digit, randomIntegerTimes)

			periodPos = [i for i, e in enumerate(str(floatValue[0])) if e == '.'][0]

			ordinary = str(floatValue[0]).replace('.', '')

			multiplyFactor = floatValue[2]

			return f"{str(multiplyFactor).zfill(5)}{str(seedValue).zfill(5)}{str(periodPos).zfill(5)}{str(ordinary).zfill(5)}"

		encoded = [f"{retrieveCode(e)}" for e in string]
		return ' '.join(encoded)

	def decrypt(self, encrypted_string):

		def retrieveCode(digit):
			multiplyFactor = int(digit[-19:-15])
			seedValue = int(digit[-15:-9])
			periodPos = int(digit[-9:-5])
			ordinary = int(digit[-5:])
			floatValue = str()
			for index, char in enumerate(str(int(ordinary))):
				if int(index) == int(periodPos):
					floatValue += '.'
				floatValue += char

			return int(float(floatValue) * int(multiplyFactor))

		encoded_numbers = encrypted_string.split()

		for num in encoded_numbers:
			retrieveCode(num)
		decrypted_string = ''.join(chr(retrieveCode(str(num))) for num in encoded_numbers)

		return decrypted_string
