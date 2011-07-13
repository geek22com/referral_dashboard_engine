# -*- coding: utf-8 -*-
# Обертка над connection pool из psycopg2.
# Ипользуем модуль как синглтон.
import sys
from psycopg2.pool import ThreadedConnectionPool
import psycopg2.extensions 
import psycopg2.extras
from heymoose.utils.workers import app_logger

class HConnection(object):
	connection = None
	def __init__(self, minconn, maxconn, *args, **kwargs):
		if HConnection.connection:
			return

		try:
			self.pool = ThreadedConnectionPool(minconn, maxconn, *args, **kwargs)
		except:
			app_logger.error(sys.exc_info())
			sys.exit(1)
		HConnection.connection = self
		app_logger.debug('HConnection instance created')

	def execute_query(self, query, args):
		try:
			conn = self.pool.getconn()
			cursor = conn.cursor()
			cursor.execute(query, args)
		except psycopg2.ProgrammingError, err:
			app_logger.error(err)
			app_logger.error(sys.exc_info())
			conn.rollback()
			self.pool.putconn(conn)
			return False

		conn.commit()
		self.pool.putconn(conn)
		return True

	def select_query(self, query, args, one=False):
		try:
			conn = self.pool.getconn()
			conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
			cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
			cursor.execute(query, args)
			if one:
				res = cursor.fetchone()
			else:
				res = cursor.fetchall()
			self.pool.putconn(conn)
		except psycopg2.ProgrammingError, err:
			app_logger.error(err)
			app_logger.error(sys.exc_info())
			return []
		
		return res

connection = HConnection(5, 20, database="social_sampler", host="127.0.0.1", user="qa", password="appatit")
