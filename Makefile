LOGIN=george_test_acc
PASSWORD=12345678

local:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) pytest hw/code/ --browser chrome

selenoid:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) pytest hw/code/ --browser chrome --selenoid

vnc:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) pytest hw/code/ --browser chrome --selenoid --vnc
	