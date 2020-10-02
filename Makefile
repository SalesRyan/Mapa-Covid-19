run:
	python3 manage.py runserver 0.0.0.0:8000
	
migrate:
	python3 manage.py migrate
	
migrations:
	python3 manage.py makemigrations
	
shell:
	python3 manage.py shell

ishell:
	python3 manage.py shell -i ipython

jupyter:
	python3 manage.py shell_plus --notebook

cleanmigrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	
povoar:
	python3 manage.py runscript povoar

rotina:
	python3 manage.py runscript rotina
		
excluir:
	python3 manage.py runscript excluir

