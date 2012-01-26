# -*- coding: utf-8 -*-
# Небольшая особенность работы с etree:
# etree_element.xpath(path) - возращает все элементы, даже если etree_element это child_node
# etree_element.findtext(text) - возвращает 1 встретившийся элемент child_node'а
# Таким образом возможен следующий вариант разбора xml (Смотри код функций)

def get_text(etree_element, text):
	el = etree_element.findtext(text)

	if not el:
		return None

	return el

def get_text_attr(etree_element, name):
	el = etree_element.attrib[name]
	if not el:
		return None

	return el

def get_attr(etree_element, name, constr=unicode):
	try:
		text_attr = get_text_attr(etree_element, name)
	except KeyError:
		return None
	return constr(text_attr)

def get_value(etree_element, text, constr=unicode):
	text = get_text(etree_element, text)
	if not text:
		return None
	if text=="true":
		return bool(True)
	elif text=="false":
		return bool(False)
	return constr(text)

def get_child(etree_element, name):
	return etree_element.find(name)
