#  api-excercise



Przykładowe api, korzystające z mongodb

***Dane potrzebne do połączenia się należy uzupełnić w pliku *.env****

Posiada 8 prostych endpointów:
- get/user
- post/user
- post/item
- delete/item
- get/itemIndex *(przy użyciu indexu)*
- get/itemMessage *(przy użyciu zawratości)*
- put/itemID

**pipenv**

Za pomocą Pipfile/Pipfile.lock i PipEnv z łatwością można
zainstalować wszystkie zależności projektu

<code>pipenv install --version </code> - aby sprawdzić wersję/czy jest zainstalowany

<code>pip install pipenv</code> - Instalacja *pipenv* za pomocą *pip*

**Uruchamianie**

*Przed rozpoczeciem uruchamiania uzupełniamy dane do połączenia się z MongoDB w pliku .env*

<code>pipenv install</code> - instalujemy wszystkie moduły

<code>uvicorn api:app</code> - uruchamiamy webserver

Gotowe, teraz api działa na socketcie 127.0.0.1:8000

Można go używać przy pomocy *curl* lub przeglądarki

<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>

