LOGIN=testleonard
PASSWORD=testtest
ID=45

all:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) ID=$(ID) pytest-3 -q hw/code  --vnc

about:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) ID=$(ID) pytest-3 -q -k "TestAbout" hw/code  --vnc

post/create:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) ID=$(ID) pytest-3 -q -k "TestCreationPost" hw/code  --vnc
