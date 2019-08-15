

**System obsługi biblioteki stworzony w ramach pracy inżynierskiej pod tytułem:**

**"Projekt i implementacja systemu obsługi biblioteki w oparciu o technologie Django, Bootstrap, HTML, CSS, JavaScript, SQL."**

**Autor: Wojciech Kłusek**


**Instalacja Linux**
**Wymagania wstępne:**
- Zainstalowany pakiet python3 w wersji >= 3.5.3,
- Zainstalowany pakiet pip3 w wersji >= 9.0.1

- Uruchomić konsolę i przejść do katalogu praca_inz.
- Zainstalować niezbędne pakiety poleceniem: pip3 install -r requirements.txt
- Będąc w konsoli należy przejść do folderu library_project: cd library_project/
- Ostatnim krokiem jest uruchomienie lokalnego serwera poleceniem: python3 manage.py runserver
- Po prawidłowym starcie serwera przejść na adres: http://127.0.0.1:8000/


**Instalacja Windows**
-  Należy pobrać najnowszą wersje Python 3 ze strony: https://www.python.org/downloads/ oraz zainstalować ją.
- Uruchomić konsole cmd.
- Sprawdzić czy zainstalowana wersja Pythona >= 3.6 komendą: python -V
- Sprawdzić wersje narzędzia pip komendą: pip -V, jeśli wersja < 18.0 należy zaktualizować narzędzie pip ( **python -m pip install --upgrade pip** )
-  Będąc w konsoli należy przejść do folderu praca_inż: **cd praca_inz**
-  Zainstalować niezbędne pakiety poleceniem: **pip install -r requirements.txt**
- Ostatnim krokiem jest uruchomienie lokalnego serwera poleceniem: **python manage.py runserver**
- Po prawidłowym starcie serwera przejść na adres: http://127.0.0.1:8000/


**Uwaga:** W aplikacji zastosowano funkcjonalność oznaczania wypożyczeń jako nieodnane w terminie. W środowisku produkcyjnym byłby on wywoływany przez cron, Możliwe jest jednak uruchomienie go ręcznie poleceniem: python manage.py check_borrows z poziomu katalogu: praca_inz/library_project/. 

Skrypt ten wykryje wypożyczenia z przekroczoną datą zwrotu, odpowiednio je oznaczy, a także zablokuje użytkownikowi którego dotyczyło wypożyczenie, możliwość dalszego wypożyczania przez bibliotekarza.




