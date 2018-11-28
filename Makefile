serve: clean
	python manage.py runserver

clean:
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -f .coverage
	rm -f pylint.out

test: clean
	nosetests -s --rednose

coverage: clean
	nosetests --with-coverage --cover-package=ads