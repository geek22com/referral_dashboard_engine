from lxml import etree

def xpath_to_string(xml_string, path): #TODO: read lxml doc...
	document = etree.fromstring(xml_string)
	element = document.xpath(path)
	if not element:
		raise Exception()

	for i in element:
		try:
			res = i.text
		except:
			res = i.decode('utf8') # in case of attribute
		break
	return res
	

