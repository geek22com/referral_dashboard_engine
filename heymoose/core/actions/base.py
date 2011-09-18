def get_text(etree_element, path):
	el = etree_element.xpath(path)
	if len(el) == 0:
		return None

	if len(el) > 1:
		raise Exception("Not text element by path=%s" % path)

	return el[0].text

def get_text_attr(etree_element, path):
	el = etree_element.xpath(path)
	if len(el) == 0:
		return None

	if len(el) > 1:
		raise Exception("Not text element by path=%s" % path)

	return el[0]

def get_attr(etree_element, path, constr=str):
	text_attr = get_text_attr(etree_element, path)
	if not text_attr:
		return None
	return constr(text_attr)

def get_value(etree_element, path, constr=str):
	text = get_text(etree_element, path)
	if not text:
		return None
	return constr(text)