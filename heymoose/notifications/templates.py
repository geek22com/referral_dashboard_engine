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

SITE_MODERATED = u'''
	{% set state_changed = site.is_dirty('admin_state') %}
	{% set approved = state_changed and site.is_approved %}
	{% set blocked = state_changed and (site.is_blocked or site.is_moderating) %}
	{% set site_url = url_for('cabinetcpa.sites_info', id=site.id, _external=true) %}

	{% if state_changed %}
		Ваша площадка <a href="{{ site_url }}">{{ site.name }}</a>
		{% if approved %}
			теперь активна.
		{% elif blocked %}
			была заблокирована. Все Ваши размещения на этой площадке теперь неактивны. Пожалуйста, проверьте свои партнерские ссылки.
		{% endif %}
	{% else %}
		Был обновлен комментарий администрации к вашей площадке <a href="{{ site_url }}">{{ site.name }}</a>.
	{% endif %}
'''

PLACEMENT_MODERATED = u'''
	{% set state_changed = placement.is_dirty('admin_state') %}
	{% set approved = state_changed and placement.is_approved %}
	{% set blocked = state_changed and (placement.is_blocked or placement.is_moderating) %}

	Размещение оффера <a href="{{ url_for('cabinetcpa.offers_info', id=placement.offer.id, _external=true) }}">{{ placement.offer.name }}</a>
	на площадке <a href="{{ url_for('cabinetcpa.sites_info', id=placement.site.id, _external=true) }}">{{ placement.site.name }}</a>
	{% if approved %}активно.{% elif blocked -%}заблокировано. Пожалуйста, проверьте свои партнерские ссылки.{% else -%}обновлено.{% endif %}
'''