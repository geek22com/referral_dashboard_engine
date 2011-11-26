#!/bin/bash
data="allowNegativeBalance=False&minAge=12&description=dasfasdf&title=asdfasdf&url=http%3A%2F%2Fya.ru&cpa=2&image=asdas&userId=1&maxAge=23&autoApprove=True&male=True&balance=12&type=REGULAR"
echo $data
curl -X POST -i --data $data http://localhost:5468/orders
