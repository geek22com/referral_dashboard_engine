# -*- coding: utf-8 -*-
from heymoose import resource
from heymoose.data import enums
from heymoose.data.models import Offer

from decimal import Decimal
import pprint
pp = pprint.PrettyPrinter(indent=4)
'''
advertiser = resource.users.get_by_email('ad1@ad.ru')
offer = Offer(
	advertiser=advertiser,
	pay_method=enums.PayMethods.CPC,
	cost=Decimal('2.23'),
	name=u'Мой первый оффер',
	url='http://ya.ru',
	title=u'Регистрация',
	regions=[]
)
resource.offers.add(offer, Decimal('100.50'))

offers, count = resource.offers.list(offset=0, limit=20, ord='ID', asc=True)
pp.pprint(offers[0].values())'''

print enums.Regions.tuples('name')