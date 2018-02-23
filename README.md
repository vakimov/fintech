
# Development

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