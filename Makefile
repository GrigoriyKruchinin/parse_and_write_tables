lint:
	docformatter -r --in-place . && black .

start:
	python app/main.py