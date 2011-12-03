from heymoose.db.models import Category

def load_category(c_id):
	return Category.query.filter(Category.mongo_id == c_id).first()

def load_categories(page=1, per_page=20):
	return Category.query.paginate(page=page, per_page=per_page).items