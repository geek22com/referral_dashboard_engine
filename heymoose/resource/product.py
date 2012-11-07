from backend import BackendResource
from heymoose.data.models import YmlCatalog, Shop


class ProductResource(BackendResource):
	base_path = '/products'

	def feed(self, key, **kwargs):
		return self.path('feed').get(key=key, **kwargs).as_obj(YmlCatalog)

	def feed_size(self, key, **kwargs):
		return self.path('feed').path('size').get(key=key, **kwargs).as_int()

	def categories(self, aff_id):
		return self.path('categories').get(aff_id=aff_id).as_objlist(Shop)
