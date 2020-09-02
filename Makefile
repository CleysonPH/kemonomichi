SHELL := /bin/fish

test:
	coverage run manage.py test
	coverage html
