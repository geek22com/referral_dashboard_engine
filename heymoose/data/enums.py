# -*- coding: utf-8 -*-
from base.enum import Enum, e

class Roles(Enum):
	CUSTOMER = e('CUSTOMER', name=u'рекламодатель', shortname=u'рекл.')
	DEVELOPER = e('DEVELOPER', name=u'разработчик', shortname=u'разр.')
	ADMIN = e('ADMIN', name=u'администратор', shortname=u'админ.')

class ExtendedRoles(Roles):
	PARTNER	= e('PARTNER', name=u'партнер', shortname=u'парт.')
	ADVERTISER = e('ADVERTISER', name=u'рекламодатель', shortname=u'рекл.')

class MessengerTypes(Enum):
	SKYPE = e('SKYPE', name=u'Skype')
	JABBER = e('JABBER', name=u'Jabber')
	ICQ = e('ICQ', name=u'ICQ')