from heymoose.db.models import Blog

def load_blog_by_id(b_id):
	return Blog.query.filter(Blog.mongo_id == b_id).first()

def load_blogs(page=1, per_page=20):
	return Blog.query.paginate(page=page, per_page=per_page).items

def load_blogs_by_category(category_id, page=1, per_page=20):
	return Blog.query.filter(Blog.category_id == category_id).paginate(page=page, per_page=per_page).items