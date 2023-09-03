from pymongo.operations import IndexModel

def get_indexes():

	# put the index information that you want to apply to your collection
	new_indexes = [
		IndexModel([('smtp_config_id', 1)], unique=True),
		IndexModel([('email', 1)], unique=True),
		IndexModel([('message', 1)], unique=True),
		IndexModel([('status', 1)], unique=True),
		IndexModel([('destinations', 1)], unique=True),
		IndexModel([('subject', 1)], unique=True),
		IndexModel([('schedule', 1)], unique=True),
	]
	return new_indexes
