# Testowanie-TDD
Aplikacja na drugi projekt z testowania - TDD

# Instrukcja uruchomienia
Python >= 3.6

Pobieramy repo
```git pull https://github.com/KamilKwapisz/Testowanie-TDD.git```

Tworzymy srodowisko wirtualne
```python3 -m venv env```
lub
```python -m venv env```

Uruchamiamy srodowisko (windows)
``` ./env/Scripts/activate ```
dla systemow UNIX:
```source ./env/bin/activate ```

Instalujemy pakiety:
```pip install -r requirements.txt```

Migracje:
``` python manage.py makemigrations```
```python manage.py migrate```

Uruchamiamy serwer:
```python manage.py runserver```

Uruchamianie testow:
```python manage.py test```

