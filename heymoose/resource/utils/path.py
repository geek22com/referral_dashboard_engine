class Path(object):
	def __init__(self):
		self.parts = []
	
	def path(self, part):
		self.parts.append(str(part))
		return self
	
	def build(self):
		return '/'.join(self.parts)


def path(part):
	return Path().path(part)