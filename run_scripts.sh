#skrypt dla crona pozwalajacy uruchamiać własne polecenia manage.py
#dodać do crontab

#aktywuj virtualenv
cd /home/wojtek9502/.virtualenvs/myproj/bin/
source activate

#uruchom polecenie manage.py
cd /home/wojtek9502/praca-inz/library_project/
python manage.py check_borrows


