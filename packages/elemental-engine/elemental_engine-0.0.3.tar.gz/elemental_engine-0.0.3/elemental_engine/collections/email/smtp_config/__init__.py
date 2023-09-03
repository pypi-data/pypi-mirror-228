import os
from elemental_engine.database import connect
from elemental_engine.config import app_config

# it's also a good practice to keep a particular name to each collection to avoid conflicts when using multiple collections at the same time
def smtp_config():
	# here we can define a mongo uri
	scope = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
	db = connect(app_config.mongo_email_db, scope)
	return db.collection('smtp_config')
