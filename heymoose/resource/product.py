from backend import BackendResource
from heymoose.data.models import YmlCatalog


class ProductResource(BackendResource):
	base_path = '/products'

	def feed(self, aff_id, **kwargs):
		return self.path('feed').get(aff_id=aff_id, **kwargs).as_obj(YmlCatalog)