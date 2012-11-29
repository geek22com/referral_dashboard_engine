# -*- coding: utf-8 -*-
from base.enums import Enum, e

class Roles(Enum):
	ADMIN = e('ADMIN', name=u'администратор', shortname=u'админ.', label_class=u'info')
	AFFILIATE = e('AFFILIATE', name=u'партнер', shortname=u'парт.', label_class=u'notice')
	ADVERTISER = e('ADVERTISER', name=u'рекламодатель', shortname=u'рекл.', label_class=u'important')

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

class AccountingEvents(Enum):
	CLICK_CREATED = e('CLICK_CREATED', name=u'клик')
	ACTION_CREATED = e('ACTION_CREATED', name=u'совершение действия')
	ACTION_APPROVED = e('ACTION_APPROVED', name=u'подтверждение действия')
	ACTION_CANCELED = e('ACTION_CANCELED', name=u'отмена действия')
	OFFER_ACCOUNT_ADD = e('OFFER_ACCOUNT_ADD', name=u'оплата задолженности по офферу')
	ROBOKASSA_ADD = e('ROBOKASSA_ADD', name=u'пополнение счета с помощью системы "RoboKassa"')
	OFFER_ACCOUNT_REMOVE = e('OFFER_ACCOUNT_REMOVE', name=u'снятие средств со счета оффера')
	MLM = e('MLM', name=u'реферальная программа')
	CANCELLED = e('CANCELLED', name=u'отмена транзакции')
	WITHDRAW = e('WITHDRAW', name=u'заказ выплаты партнёру')
	ADVERTISER_ACCOUNT_ADD = e('ADVERTISER_ACCOUNT_ADD', name=u'пополнение счета рекламодателя')

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
	DOUBLE_FIXED = e('DOUBLE_FIXED', name=u'фиксированная за первое и последующие действия')

class Regions(Enum):
	RUSSIA = e('RUSSIA', code=u'RU', name=u'Россия')
	UKRAINE = e('UKRAINE', code=u'UA', name=u'Украина')
	BELARUS = e('BELARUS', code=u'BY', name=u'Белоруссия')
	POLAND = e('POLAND', code=u'PL', name=u'Польша')
	LATVIA = e('LATVIA', code=u'LV', name=u'Латвия')
	GERMANY = e('GERMANY', code=u'DE', name=u'Германия')
	CSI = e('CSI', code=u'CSI', name=u'СНГ')

class OfferActionStates(Enum):
	NOT_APPROVED = e('NOT_APPROVED', name=u'не подтверждено', css_class=u'black')
	APPROVED = e('APPROVED', name=u'подтверждено', css_class=u'green')
	CANCELED = e('CANCELED', name=u'отменено', css_class=u'red')

class OfferActionDateKinds(Enum):
	CREATION = e('CREATION', name=u'время создания')
	CHANGE = e('CHANGE', name=u'время изменения')

class DebtDateKinds(Enum):
	CREATION = e('CREATION', name=u'время подтверждения действия')
	ORDER = e('ORDER', name=u'время заказа выплаты')

class WithdrawalBases(Enum):
	AFFILIATE_REVENUE = e('AFFILIATE_REVENUE', name=u'Вознаграждение партнёра')
	FEE = e('FEE', name=u'Комиссия системы')
	MLM = e('MLM', name=u'Реферальная программа')

class ProductRevenueUnits(Enum):
	FIXED = e('fixed', sign=u'руб.')
	PERCENT = e('percent', sign=u'%')

class SiteTypes(Enum):
	GRANT = e('GRANT', name=u'Площадка по умолчанию', enabled=False)
	WEB_SITE = e('WEB_SITE', name=u'Веб-сайт', enabled=True)
	SOCIAL_NETWORK = e('SOCIAL_NETWORK', name=u'Страница или группа в социальной сети', enabled=True)
	CONTEXT = e('CONTEXT', name=u'Контекстная реклама', enabled=True)
	MAIL = e('MAIL', name=u'Почтовые рассылки', enabled=True)
	DOORWAY = e('DOORWAY', name=u'Сеть дорвеев', enabled=True)
	ARBITRAGE = e('ARBITRAGE', name=u'Арбитраж', enabled=True)

class ContextSystems(Enum):
	YANDEX_DIRECT = e('YANDEX_DIRECT', name=u'Яндекс.Директ')
	GOOGLE_ADWORDS = e('GOOGLE_ADWORDS', name=u'Google AdWords')
	YAHOO = e('YAHOO', name=u'Yahoo!')
	BEGUN = e('BEGUN', name=u'Бегун')
	OTHER = e('OTHER', name=u'другая')

class AdminStates(Enum):
	MODERATION = e('MODERATION', name=u'на модерации', tristate=None, message_class='info', link_class='danger')
	APPROVED = e('APPROVED', name=u'подтверждено', tristate=True, message_class='success', link_class='')
	BLOCKED = e('BLOCKED', name=u'заблокировано', tristate=False, message_class='error', link_class='danger')