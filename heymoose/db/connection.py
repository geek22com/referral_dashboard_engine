# -*- coding: utf-8 -*-
# Обертка над connection pool из psycopg2.
# Ипользуем модуль как синглтон.
import sys
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
import psycopg2.extensions
import psycopg2.extras
from heymoose.utils.workers import app_logger
import heymoose.settings.debug_config as config

#Thread safe variant
class HConnection(object):
	connection = None
	def __init__(self, minconn, maxconn, *args, **kwargs):
		if HConnection.connection:
			return

		try:
			self.pool = ThreadedConnectionPool(minconn, maxconn, *args, **kwargs)
		except Exception as inst:
			app_logger.error(inst)
			app_logger.error(sys.exc_info())
			return

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
		except psycopg2.ProgrammingError, err:
			self.pool.putconn(conn)
			app_logger.error(err)
			app_logger.error(sys.exc_info())
			return []
		self.pool.putconn(conn)
		return res

#Reentrant variant (suggests pgbouncer usage, or some other pool controling tool)
class HReentrantConnection(object):
	connection = None
	def __init__(self, **kwargs):
		if HReentrantConnection.connection:
			return
		try:
			self.database = kwargs['database']
			self.host = kwargs['host']
			self.port = kwargs['port']
			self.user = kwargs['user']
			self.password = kwargs['password']
		except Exception as inst:
			app_logger.error(inst)
			app_logger.error(sys.exc_info())
			return
		HReentrantConnection.connection = self
		app_logger.debug('HReentrantConnection instance created')

	def execute_query(self, query, args):
		try:
			conn = psycopg2.connect(database=self.database,
									host=self.host,
									port=self.port,
									user=self.user,
									password=self.password)
			cursor = conn.cursor()
			cursor.execute(query, args)
		except psycopg2.ProgrammingError, err:
			conn.rollback()
			conn.close()
			app_logger.error(err)
			app_logger.error(sys.exc_info())
			return False

		conn.commit()
		conn.close()
		return True

	def select_query(self, query, args, one=False):
		try:
			conn = psycopg2.connect(database=self.database,
									host=self.host,
									port=self.port,
									user=self.user,
									password=self.password)
			cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
			cursor.execute(query, args)
			if one:
				res = cursor.fetchone()
			else:
				res = cursor.fetchall()
		except psycopg2.ProgrammingError, err:
			conn.close()
			app_logger.error(err)
			app_logger.error(sys.exc_info())
			return []
		conn.close()
		return res

connection = HReentrantConnection(database=config.DATABASE,
								  host=config.HOST,
								  port=config.DB_PORT,
								  user=config.DB_USER,
								  password=config.DB_PASSWORD)
#connection = HConnection(config.MIN_POOL,
#						 config.MAX_POOL,
#						 database=config.DATABASE,
#						 host=config.HOST,
#						 port=config.DB_PORT,
#						 user=config.DB_USER,
#						 password=config.DB_PASSWORD)
