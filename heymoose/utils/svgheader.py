from lxml import etree

def parse(input):
	header = {}
	if hasattr(input, 'read'):
		input.seek(0)
	else:
		input = open(input, 'r')
		
	xml = etree.fromstring(input.read())
	if '}' in xml.tag:
		_before, _sep, tag = xml.tag.partition('}')
	else:
		tag = xml.tag
		
	if tag.lower() != 'svg':
		raise ValueError('Invalid SVG file')
	
	try:
		header['width'] = int(xml.get('width', '0').replace('px', ''))
	except:
		header['width'] = 0
		
	try:
		header['height'] = int(xml.get('height', '0').replace('px', ''))
	except:
		header['height'] = 0
		
	return header