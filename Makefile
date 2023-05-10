# <<<<<<< leonard
LOGIN="Типичный программист"
PASSWORD=testpass
ID=2
LOGIN_DONATOR=leonard
PASSWORD_DONATOR=leoleo
ID_DONATOR=9

all:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) ID=$(ID) LOGIN_DONATOR=$(LOGIN_DONATOR) PASSWORD_DONATOR=$(PASSWORD_DONATOR) ID_DONATOR=$(ID_DONATOR) pytest-3 -q hw/code  --vnc

about:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) ID=$(ID) LOGIN_DONATOR=$(LOGIN_DONATOR) PASSWORD_DONATOR=$(PASSWORD_DONATOR) ID_DONATOR=$(ID_DONATOR) pytest-3 -q -k "TestAbout" hw/code  --vnc

post/create:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) ID=$(ID) LOGIN_DONATOR=$(LOGIN_DONATOR) PASSWORD_DONATOR=$(PASSWORD_DONATOR) ID_DONATOR=$(ID_DONATOR) pytest-3 -q -k "TestCreationPost" hw/code  --vnc
# =======
# LOGIN=george_test_acc
# PASSWORD=12345678

local:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) pytest hw/code/ --browser chrome

selenoid:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) pytest hw/code/ --browser chrome --selenoid

vnc:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) pytest hw/code/ --browser chrome --selenoid --vnc
	
# >>>>>>> vdonate
