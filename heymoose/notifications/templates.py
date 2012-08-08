# -*- coding: utf-8 -*-

OFFER_BLOCKED = u'''
	Рекламная кампания
	<a href="{{ url_for('cabinetcpa.offers_info', id=offer.id, _external=true) }}">&laquo;{{ offer.name }}&raquo;</a>
	была заблокирована администрацией.
	{% if reason %}Причина блокировки: <i>{{ reason }}</i>{% endif %}
'''

OFFER_UNBLOCKED = u'''
	Рекламная кампания
	<a href="{{ url_for('cabinetcpa.offers_info', id=offer.id, _external=true) }}">&laquo;{{ offer.name }}&raquo;</a>
	активна.
'''

GRANT_APPROVED = u'''
	Ваша заявка на сотрудничество с рекламной кампанией
	<a href="{{ url_for('cabinetcpa.offers_info', id=grant.offer.id, _external=true) }}">&laquo;{{ grant.offer.name }}&raquo;</a>
	подтверждена.
'''

GRANT_REJECTED = u'''
	Ваша заявка на сотрудничество с рекламной кампанией
	<a href="{{ url_for('cabinetcpa.offers_info', id=grant.offer.id, _external=true) }}">&laquo;{{ grant.offer.name }}&raquo;</a>
	отклонена рекламодателем.
	{% if reason %}Причина: <i>{{ reason }}</i>{% endif %}
'''

GRANT_BLOCKED = u'''
	Ваша заявка на сотрудничество с рекламной кампанией
	<a href="{{ url_for('cabinetcpa.offers_info', id=grant.offer.id, _external=true) }}">&laquo;{{ grant.offer.name }}&raquo;</a>
	заблокирована администрацией.
	{% if reason %}Причина: <i>{{ reason }}</i>{% endif %}
'''