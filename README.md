# Delete unused media files from Django project

[![build-status-image]][travis]

This package provides management command `cleanup_unused_media` for Django applications. With help of this management command you can remove all media files which are no longer used (files without references from any Django model with `FileField` or `ImageField` fields or their inheritances).

# Installation

1.  Install ``django-unused-media``:
    ```
    pip install django-unused-media
    ```

    Python 2.7, 3.5, 3.6, PyPy are tested with tox.
    
    Django 1.6, 1.7, 1.8, 1.9, 1.10, 1.11 are tested with tox.

2.  Add ``django-unused-media`` to ``INSTALLED_APPS``:
    ```python
    INSTALLED_APPS = (
        ...
        'django_unused_media',
        ...
    )
    ```

# Usage

To cleanup all unused media files, run management command:
```
./manage.py cleanup_unused_media
```
By default command is running in interactive mode. List of files which are going to be removed will be displayed for confirmation. User have to confirm the action.

### Options

`--noinput`, `--no-input`

Non interactive mode. Command will remove files without any confirmation from user. Useful for scripts.
```
./manage.py cleanup_unused_media --noinput
```

`-e`, `--exclude` 

To avoid operating on particular files you can use exclude option. 
- *`*` as any symbol is supported.*
- *Can use multiple options in one command.*

For example, to keep `.gitignore` and `*.png` files you can use:
```
./manage.py cleanup_unused_media -e *.gitignore -e *.png
```

Also you can exclude entire folder or some files in that folder (path should be relative to `settings.MEDIA_ROOT`):
```
./manage.py cleanup_unused_media -e path/to/dir/* -e path/to/dir/my*.doc
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

[build-status-image]: https://api.travis-ci.org/akolpakov/django-unused-media.svg?branch=master
[travis]: http://travis-ci.org/akolpakov/django-unused-media?branch=master