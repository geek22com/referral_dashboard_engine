# -*- coding: utf-8 -*-

def create_dict(unset=None, **kwargs):
	return dict([(key, value) for key, value in kwargs.iteritems() if value != unset])

