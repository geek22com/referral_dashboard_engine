from mappers import order_from_xml, count_from_xml
from heymoose.core.rest import post, put, get, delete
from heymoose.core.data import OrderTypes
from heymoose.utils import convert

resource_path = "/orders"


def add_order(user_id, title, url, balance, cpa, type, auto_approve=True,
			  allow_negative_balance=True, reentrant=False,
			  male=None, min_age=None, max_age=None,
			  city_filter_type=None, city=[],
			  app_filter_type=None, app=[],
			  min_hour=None, max_hour=None,
			  **kwargs):
	params_dict = dict(
		userId=user_id,
		title=title,
		url=url,
        balance=balance,
		cpa=cpa,
		autoApprove=auto_approve,
		allowNegativeBalance=allow_negative_balance,
		reentrant=reentrant,
		type=type,
		**kwargs)
	
	if min_age is not None and min_age > 0: params_dict.update(minAge=min_age)
	if max_age is not None and max_age > 0: params_dict.update(maxAge=max_age)
	male = convert.to_bool(male)
	if male is not None: params_dict.update(male=male)
	if city_filter_type: params_dict.update(cityFilterType=city_filter_type, city=city)
	if app_filter_type: params_dict.update(appFilterType=app_filter_type, app=app)
	if min_hour is not None and 0 <= min_hour <= 23: params_dict.update(minHour=min_hour)
	if max_hour is not None and 0 <= max_hour <= 23: params_dict.update(maxHour=max_hour)
	
	id = post(path=resource_path, params_dict=params_dict)
	return int(id)


def add_regular_order(user_id, title, url, balance, cpa, description, image, auto_approve=True,
					allow_negative_balance=True, reentrant=False,
					male=None, min_age=None, max_age=None,
					city_filter_type=None, city=[],
					app_filter_type=None, app=[],
			  		min_hour=None, max_hour=None):
	return add_order(user_id=user_id,
				title=title,
				url=url,
				balance=balance,
				cpa=cpa,
				auto_approve=auto_approve,
				allow_negative_balance=allow_negative_balance,
				reentrant=reentrant,
				male=male,
				min_age=min_age,
				max_age=max_age,
				city_filter_type=city_filter_type,
				city=city,
				app_filter_type=app_filter_type,
				app=app,
				min_hour=min_hour,
				max_hour=max_hour,
				type=OrderTypes.REGULAR,
				description=description,
				image=image)
	
	
def add_banner_order(user_id, title, url, balance, cpa, image, banner_size, banner_mime_type,
					auto_approve=True,
					allow_negative_balance=True, reentrant=False,
					male=None, min_age=None, max_age=None,
					city_filter_type=None, city=[],
					app_filter_type=None, app=[],
			  		min_hour=None, max_hour=None):
	return add_order(user_id=user_id,
				title=title,
				url=url,
				balance=balance,
				cpa=cpa,
				auto_approve=auto_approve,
				allow_negative_balance=allow_negative_balance,
				reentrant=reentrant,
				male=male,
				min_age=min_age,
				max_age=max_age,
				city_filter_type=city_filter_type,
				city=city,
				app_filter_type=app_filter_type,
				app=app,
				min_hour=min_hour,
				max_hour=max_hour,
				type=OrderTypes.BANNER,
				image=image,
				bannerMimeType=banner_mime_type,
				bannerSize=banner_size)


def add_video_order(user_id, title, url, balance, cpa, video_url, auto_approve=True,
					allow_negative_balance=True, reentrant=False,
					male=None, min_age=None, max_age=None,
					city_filter_type=None, city=[],
					app_filter_type=None, app=[],
			  		min_hour=None, max_hour=None):
	return add_order(user_id=user_id,
				title=title,
				url=url,
				balance=balance,
				cpa=cpa,
				auto_approve=auto_approve,
				allow_negative_balance=allow_negative_balance,
				reentrant=reentrant,
				male=male,
				min_age=min_age,
				max_age=max_age,
				city_filter_type=city_filter_type,
				city=city,
				app_filter_type=app_filter_type,
				app=app,
				min_hour=min_hour,
				max_hour=max_hour,
				type=OrderTypes.VIDEO,
				videoUrl=video_url)


def update_order(order_id, **kwargs):
	path = '{0}/{1}'.format(resource_path, order_id)
	params = dict([(convert.to_camel_case(key), value) for key, value in kwargs.iteritems()])
	put(path=path, params_dict=params)


def get_order(order_id, **kwargs):
	path = "{0}/{1}".format(resource_path, order_id)
	return order_from_xml(get(path=path, params_dict=kwargs))

def approve_order(order_id):
	'''Deprecated, use enable_order instead.'''
	enable_order(order_id)
	
	
def enable_order(order_id):
	path = "{0}/{1}/enabled".format(resource_path, order_id)
	put(path=path)
	
def disable_order(order_id):
	path = "{0}/{1}/enabled".format(resource_path, order_id)
	delete(path=path)
	
	
def pause_order(order_id):
	path = "{0}/{1}/paused".format(resource_path, order_id)
	put(path=path)
	
def play_order(order_id):
	path = "{0}/{1}/paused".format(resource_path, order_id)
	delete(path=path)
	
def set_order_playing(order_id, play=True):
	if play:
		play_order(order_id)
	else:
		pause_order(order_id)


def get_orders(user_id=None, **kwargs):
	if user_id: kwargs.update(userId=user_id)
	return map(order_from_xml, get(path=resource_path, params_dict=kwargs))

def get_orders_count(user_id=None):
	path = "{0}/{1}".format(resource_path, "count")
	params = dict()
	if user_id: params.update(userId=user_id)
	return count_from_xml(get(path=path, params_dict=params))


def get_price_off_orders():
	path = "{0}/price-off".format(resource_path)
	return map(order_from_xml, get(path=path))


def add_order_banner(order_id, banner_size, mime_type, image):
	path = "{0}/{1}/banners".format(resource_path, order_id)
	params = dict(bannerSize=banner_size, mimeType=mime_type, image=image)
	post(path=path, params_dict=params)

def delete_order_banner(order_id, banner_id):
	path = "{0}/{1}/banners/{2}".format(resource_path, order_id, banner_id)
	delete(path=path)



