# external modules
import os

import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# internal modules
from elemental_engine.config import app_config

collections = [collection for collection in os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'collections'))]

index_cache = []

def load_indexes(collection_scope, collection_name):
	try:
		module_name = f"elemental_engine.collections.{collection_scope}.{collection_name}"
		collection_module = __import__(module_name, fromlist=['indexes'])
		collection_indexes = getattr(collection_module, 'indexes')
		return collection_indexes.get_indexes()
	except ImportError:
		return None

def set_indexes(collection_scope, collection, collection_name):
	indexes = load_indexes(collection_scope, collection_name)
	if indexes is not None:
		for index in indexes:

			try:
				collection.create_indexes([index])
			except:
				pass


class connect:

	def __init__(self, uri: str, collection_scope: str):

		self.collection_scope = collection_scope

		if app_config.debug:
			self.mongo_client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
		else:
			self.mongo_client = MongoClient(uri, server_api=ServerApi('1'))

		self.db = self.mongo_client.database

		try:
			self.mongo_client.admin.command('ping')

		except Exception as e:
			raise e

	def collection(self, collection_name):
		collection_name = f'{collection_name}_{app_config.environment}'
		collection = self.db.__getattr__(collection_name)
		# load the indexes from the respective collection folder
		current_index_pk = str(collection) + str(collection_name)
		if current_index_pk not in index_cache:
			set_indexes(self.collection_scope, collection, collection_name.replace(f'_{app_config.environment}', ''))
			index_cache.append(current_index_pk)

		return collection
