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

class TransactionTypes(Enum):
	UNKNOWN = e('UNKNOWN', desc=u'--')
	TRANSFER = e('TRANSFER', desc=u'Перевод')
	RESERVATION = e('RESERVATION', desc=u'Резервирование')
	ACTION_APPROVED = e('ACTION_APPROVED', desc=u'Оплата за клики')
	MLM = e('MLM', desc=u'MLM')
	RESERVATION_CANCELLED = e('RESERVATION_CANCELLED', desc=u'Отмена резервирования')
	REPLENISHMENT_ROBOKASSA = e('REPLENISHMENT_ROBOKASSA', desc=u'Пополнение счета с помощью системы "RoboKassa"')
	WITHDRAW = e('WITHDRAW', desc=u'Выплата разработчику')
	REPLENISHMENT_ADMIN = e('REPLENISHMENT_ADMIN', desc=u'Пополнение счета администрацией')
	WITHDRAW_DELETED = e('WITHDRAW_DELETED', desc=u'Отмена выплаты разработчику')

class OrderTypes(Enum):
	REGULAR = e('REGULAR', name=u'обычный')
	BANNER = e('BANNER', name=u'баннер')
	VIDEO = e('VIDEO', name=u'видео')

class FilterTypes(Enum):
	NONE = e('', name=u'не учитывать')
	INCLUSIVE = e('INCLUSIVE', name=u'только указанные')
	EXCLUSIVE = e('EXCLUSIVE', name=u'все, кроме указанных')


class PayMethods(Enum):
	CPA = e('CPA', name=u'за действие')
	CPC = e('CPC', name=u'за клик')

class CpaPolicies(Enum):
	PERCENT = e('PERCENT', name=u'процент')
	FIXED = e('FIXED', name=u'фиксированная')

class Regions(Enum):
	RUSSIA = e('RU')
	UKRAINE = e('UA')
	BELARUS = e('BY')
