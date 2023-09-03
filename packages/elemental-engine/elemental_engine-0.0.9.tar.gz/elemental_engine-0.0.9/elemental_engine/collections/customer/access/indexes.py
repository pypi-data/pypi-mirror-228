from pymongo.operations import IndexModel


def get_indexes():

	# put the index information that you want to apply to your collection
	new_indexes = [
		IndexModel([('token', 1)], unique=True),
	]
	return new_indexes
