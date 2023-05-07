LOGIN=leonard
PASSWORD=leoleo

all:
	LOGIN=$(LOGIN) PASSWORD=$(PASSWORD) pytest-3 -q hw/code  --vnc
