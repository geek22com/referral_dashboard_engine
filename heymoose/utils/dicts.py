UNSET = object()

def create_dict(**kwargs):
	return dict([(key, value) for key, value in kwargs.iteritems() if value != UNSET])