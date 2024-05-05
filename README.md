### Установка

1. Клонируйте репозиторий на свой локальный компьютер:

```shell
git clone https://github.com/LeoLay7/PizzaDelivery
```

2. Перейдите в каталог с проектом:

```shell
cd pizza
```

3. Создайте и активируйте виртуальное окружение (необязательно, но рекомендуется):

```shell
python -m venv venv
```

4. Запуск виртуального окружения

- На Windows:

```shell
venv\Scripts\activate
```

- На macOS и Linux:

```shell
source venv/bin/activate
```

5. Установите зависимости из файла requirements.txt:

```shell
pip install -r requirements.txt
```

### Настройка

1. Переименуйте файл template.env в .env и при необходимости 
вставьте свой ключ django в переменную DJANGO_SECRET_KEY.

2. Примените миграции:

```shell
python manage.py migrate
```


3. Создайте суперпользователя(c его помощью вы потом сможете
заходить в админку(url: 127.0.0.1/admin/):

```shell
python manage.py shell

>>> from user.models import *
>>> User.objects.create_superuser(email=<email>, password=<password>)
```

### Запуск

Теперь вы можете запустить сервер разработки Django:

```shell
python manage.py runserver
```

### Примечание для проверяющих

Визуал для страницы профиля будет добавлен позже