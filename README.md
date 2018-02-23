
# Requirements

Python 3.6
Python 2.7


# Install for development

Install requirements

```bash
pip install -r requirements.txt
```

Create file fintech/settings/local.py with local settings.
 
For example:

```python
from fintech.settings.const import *

STATIC_ROOT = 'static'

SECRET_KEY = 'very-secret-key'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

Run

```bash
python manage.py migrate
python manage.py loaddata test.yaml
python manage.py run
```

Test user/password: admin/admin


# ТЗ

1. Партнерское API:
 * получение списка анкет (с сортировкой и фильтрами)
   `GET /credits/customer-profile/?surname=Петров&?ordering=birth_day`
 * просмотр анкеты по ID
   `GET /credits/customer-profile/1/`
 * создание анкеты
   `POST /credits/customer-profile/`
   ```json
      {
        "first_name": "Иван",
        "patronymic": "Иванович",
        "surname": "Иванов",
        "birth_day": "1930-01-01",
        "phone": "+74990000000",
        "passport_number": "0000000000",
        "score": null
      }
   ```
 * отправка заявки в кредитные организации
   `POST /credits/application/`
   ```json
      {
        "customer_profile": "1",
        "offer": "2"
      }
   ```
2. API кредитной организации:
 * получение списка заявок (с сортировкой и фильтрами)
   `GET /credits/application/?status=NEW&ordering=created_at`
 * просмотре заявки по ID
   `GET /credits/application/1/`