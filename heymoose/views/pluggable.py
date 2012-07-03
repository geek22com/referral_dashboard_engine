from flask import render_template, redirect, request
from flask.views import View
from math import ceil


class ContextViewMixin(object):
	def __init__(self):
		super(ContextViewMixin, self).__init__()
		self.args = []
	
	def context(self, *args):
		pass


class SecurityViewMixin(object):
	allow_all = False
	
	def __init__(self):
		super(SecurityViewMixin, self).__init__()
		self.perms = dict()
	
	def permissions(self):
		return dict()
	
	def can(self, permission):
		return self.allow_all or self.perms.get(permission, False)


class TemplateViewMixin(object):
	template = None
	
	def __init__(self, template=None, **kwargs):
		super(TemplateViewMixin, self).__init__()
		self.template = template or self.template

	def render_template(self):
		return render_template(self.template, view=self)


class ListViewMixin(object):
	context_list_name = 'items'
	
	def __init__(self):
		super(ListViewMixin, self).__init__()
		self.query_args = dict()
		
	def query(self, **kwargs):
		return []
	
	def perform_query(self):
		self.items = self.query(**self.query_args)
		setattr(self, self.context_list_name, self.items)


class ListPageViewMixin(ListViewMixin):
	page_param_name = 'page'
	pages_name = 'pages'
	items_per_page = 20
	page_zone = 7
	
	def current_page(self):
		try:
			return int(request.args.get(self.page_param_name))
		except:
			return 1
	
	def page_limits(self, page):
		return self.items_per_page * (page - 1), self.items_per_page
	
	def paginate(self, page, count):
		pcount = int(ceil(float(count) / self.items_per_page)) if self.items_per_page > 0 else 0
		if pcount == 0: pcount = 1
		
		# Calculate pages range
		pfirst = page - self.page_zone
		plast = page + self.page_zone
		
		if pfirst < 1 and plast > pcount:
			pfirst = 1
			plast = pcount
		elif pfirst < 1:
			pfirst = 1
			plast = min(pfirst + 2 * self.page_zone, pcount)
		elif plast > pcount:
			plast = pcount
			pfirst = max(1, plast - 2 * self.page_zone)
		
		return dict(current=page, count=pcount, range=range(pfirst, plast+1))
		

class SortedListMixin(object):
	default_order = None
	default_direction = None
	
	def sorting(self):
		order = request.args.get('ord', self.default_order)
		direction = request.args.get('dir', self.default_direction) if order else None
		return order, direction


class TemplateView(View, ContextViewMixin, SecurityViewMixin, TemplateViewMixin):
	def permissions(self):
		return dict(view=True)
	
	def dispatch_request(self, *args):
		self.context(*args)
		self.perms.update(self.permissions())
		if not self.can('view'):
			return redirect(403)
		return self.render_template()


class ListView(View, ContextViewMixin, SecurityViewMixin, TemplateViewMixin, ListViewMixin):
	def permissions(self):
		return dict(view=True)
	
	def dispatch_request(self, *args):
		self.context(*args)
		self.perms.update(self.permissions())
		if not self.can('view'):
			return redirect(403)
		self.items = self.query(**self.query_args)
		return self.render_template()


class ListPageView(View, ContextViewMixin, SecurityViewMixin, TemplateViewMixin, ListPageViewMixin):
	def permissions(self):
		return dict(view=True)
	
	def dispatch_request(self, *args):
		self.context(*args)
		self.perms.update(self.permissions())
		if not self.can('view'):
			return redirect(403)
		page = self.current_page()
		offset, limit = self.page_limits(page)
		self.query_args.update(offset=offset, limit=limit)
		self.items, count = self.query(**self.query_args)
		self.pages = self.paginate(page, count)
		return self.render_template()


class SortedListPageView(View, ContextViewMixin, SecurityViewMixin, TemplateViewMixin, ListPageViewMixin, SortedListMixin):
	def permissions(self):
		return dict(view=True)
	
	def dispatch_request(self, *args):
		self.context(*args)
		self.perms.update(self.permissions())
		if not self.can('view'):
			return redirect(403)
		self.order, self.direction = self.sorting()
		self.query_args.update(ord=self.order, dir=self.direction)
		page = self.current_page()
		offset, limit = self.page_limits(page)
		self.query_args.update(offset=offset, limit=limit)
		self.items, count = self.query(**self.query_args)
		self.pages = self.paginate(page, count)
		return self.render_template()
