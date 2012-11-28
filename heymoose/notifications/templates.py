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
