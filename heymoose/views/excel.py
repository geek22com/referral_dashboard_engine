# -*- coding: utf-8 -*-
import xlwt, cStringIO
from heymoose.data.enums import OfferActionStates

bold_font = xlwt.Font(); bold_font.bold = True
red_font = xlwt.Font(); red_font.colour_index = 2
green_font = xlwt.Font(); green_font.colour_index = 3

bold_style = xlwt.XFStyle(); bold_style.font = bold_font
red_style = xlwt.XFStyle(); red_style.font = red_font
green_style = xlwt.XFStyle(); green_style.font = green_font
datetime_style = xlwt.XFStyle(); datetime_style.num_format_str = u'dd.mm.yyyy hh:mm:ss'
currency_style = xlwt.XFStyle(); currency_style.num_format_str = u'# ##0.00 [$руб.-419]'


def offer_actions_to_xls(actions):
	state_styles = { OfferActionStates.APPROVED : green_style, OfferActionStates.CANCELED : red_style }
	wb = xlwt.Workbook()
	ws = wb.add_sheet(u'Действия')
	ws.write(0, 0, u'Время', bold_style)
	ws.write(0, 1, u'Транзакция', bold_style)
	ws.write(0, 2, u'Код', bold_style)
	ws.write(0, 3, u'Сумма', bold_style)
	ws.write(0, 4, u'Состояние', bold_style)
	for i, action in enumerate(actions):
		row = i + 1
		ws.write(row, 0, action.creation_time, datetime_style)
		ws.write(row, 1, action.transaction_id)
		ws.write(row, 2, action.offer.code)
		ws.write(row, 3, action.amount, currency_style)
		ws.write(row, 4, action.state.name, state_styles.get(action.state, xlwt.Style.default_style))
	for i in range(5):
		ws.col(i).width = 5000
	f = cStringIO.StringIO()
	wb.save(f)
	f.seek(0)
	return f