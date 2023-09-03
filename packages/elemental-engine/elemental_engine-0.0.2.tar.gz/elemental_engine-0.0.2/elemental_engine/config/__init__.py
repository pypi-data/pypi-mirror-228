from dotenv import load_dotenv
import os

load_dotenv()

class app_config:
	app_secret = str(os.environ.get("APP_SECRET", default='000000123'))
	app_key = str(os.environ.get("APP_KEY", default='000000321'))

	# dev settings, please don't mess around
	debug = bool(os.environ.get("DEBUG", default=False))
	demo = bool(os.environ.get("DEMO", default=False))

	# api settings
	title = str(os.environ.get("TITLE"))
	version = str(os.environ.get("VERSION", default="1.0"))
	port = int(os.environ.get("PORT", default=80))
	host = str(os.environ.get("HOST"))

	# swagger settings
	summary = str(os.environ.get("SUMMARY", default=""))
	description = str(os.environ.get("DESCRIPTION", default=""))

	# mongo db settings
	mongo_customer_db = str(os.environ.get("MONGO_CUSTOMER_DB"))
	mongo_email_db = str(os.environ.get("MONGO_EMAIL_DB"))

	# doc settings
	show_doc = bool(os.environ.get("ENABLE_DOCUMENTATION"))
	doc_url = str(os.environ.get("DOC_URL", default="/docs"))

	customer_mail = str(os.environ.get("CUSTOMER_MAIL", default='info@tomneto.com'))
	customer_password = str(os.environ.get("CUSTOMER_PASSWORD", default='Mm12052015@'))

	customer_smtp_server = str(os.environ.get("CUSTOMER_SMTP_SERVER", default='smtpout.secureserver.net'))
	customer_smtp_port = int(os.environ.get("CUSTOMER_SMTP_PORT", default=587))

	# env level database and others settings
	if debug:
		environment = 'debug'
	else:
		environment = 'production'

	demo_key = '64f22f2f18036e766b01e6d8'
	demo_secret = 'azffw7zSQU6KJq4DrWrwhw'