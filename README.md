# Delete unused media files from Django project

This package provides management command `cleanup_unused_media` for Django application. With help of this command you can remove all media files which are no longer used (files without references from any model with `FileField` or `ImageField` fields or their inheritances).

# Installation
1.  Install ``django-unused-media``:
    ```
    pip install django-unused-media
    ```
    Python 2.7, 3.3, 3.4, PyPy are supported<br/>
    Django 1.6, 1.7, 1.8 are supported

2.  Add ``django-unused-media`` to ``INSTALLED_APPS``:
    ```python
    INSTALLED_APPS = (
        ...
        'django_unused_media',
        ...
    )
    ```

# Usage

For cleanup all unused media, run:
```
./manage.py cleanup_unused_media
```

By default command runs in interactive mode. And before removing list of files will be displayed. User should confirm action.
If you would like to use this command in non interactive mode, please use option `--noinput`:
```
./manage.py cleanup_unused_media --noinput
```



# Tests
At first make sure that you are in virtualenv.

Install all dependencies:
```
make setup
```
To run tests:
```
make test
```

# License
[MIT licence](./LICENSE)