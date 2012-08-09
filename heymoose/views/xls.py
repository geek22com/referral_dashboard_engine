# -*- coding: utf-8 -*-
import xlwt, cStringIO

bold_font = xlwt.Font(); bold_font.bold = True
bold_style = xlwt.XFStyle(); bold_style.font = bold_font
datetime_style = xlwt.XFStyle(); datetime_style.num_format_str = u'dd.mm.yyyy hh:mm:ss'
currency_style = xlwt.XFStyle(); currency_style.num_format_str = u'# ##0.00 [$руб.-419]'

def offer_actions_to_xls(actions):
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
		ws.write(row, 4, action.state.name)
	for i in range(5):
		ws.col(i).width = 5000
	f = cStringIO.StringIO()
	wb.save(f)
	f.seek(0)
	return f