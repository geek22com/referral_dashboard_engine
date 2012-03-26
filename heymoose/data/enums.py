# -*- coding: utf-8 -*-
from base.enums import Enum, e

class Roles(Enum):
	CUSTOMER = e('CUSTOMER', name=u'рекламодатель', shortname=u'рекл.')
	DEVELOPER = e('DEVELOPER', name=u'разработчик', shortname=u'разр.')
	ADMIN = e('ADMIN', name=u'администратор', shortname=u'админ.')
	AFFILIATE = e('AFFILIATE', name=u'партнер', shortname=u'парт.')
	ADVERTISER = e('ADVERTISER', name=u'рекламодатель', shortname=u'рекл.')

class MessengerTypes(Enum):
	SKYPE = e('SKYPE', name=u'Skype')
	JABBER = e('JABBER', name=u'Jabber')
	ICQ = e('ICQ', name=u'ICQ')

class OrderTypes(Enum):
	REGULAR = e('REGULAR', name=u'обычный')
	BANNER = e('BANNER', name=u'баннер')
	VIDEO = e('VIDEO', name=u'видео')

class FilterTypes(Enum):
	NONE = e('', name=u'не учитывать')
	INCLUSIVE = e('INCLUSIVE', name=u'только указанные')
	EXCLUSIVE = e('EXCLUSIVE', name=u'все, кроме указанных')