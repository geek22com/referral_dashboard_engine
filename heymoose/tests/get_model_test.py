# -*- coding: utf-8 -*-
import sys
sys.path.append("/home/kshilov/Prg/tuta/apache_configuration/frontend")

import heymoose.db.cursor as cursor
import heymoose.db.models as models
from heymoose import app


connection = cursor.HConnection()
lst = models.User.get(connection, id=1)
for i in lst:
	user = i 
user.username = 12
print user
