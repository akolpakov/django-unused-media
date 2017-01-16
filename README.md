# Delete unused media files from Django project

This package provides management command `cleanup_unused_media` for Django application. With help of this command you can remove all media files which are no longer used (files without references from any Django model with `FileField` or `ImageField` fields or their inheritances).

# Installation
1.  Install ``django-unused-media``:
    ```
    pip install django-unused-media
    ```
    Python 2.7, 3.5, PyPy are tested with tox.
    
    Django 1.6, 1.7, 1.8, 1.9, 1.10 are tested with tox.

2.  Add ``django-unused-media`` to ``INSTALLED_APPS``:
    ```python
    INSTALLED_APPS = (
        ...
        'django_unused_media',
        ...
    )
    ```

# Usage

For cleanup all unused media run management command:
```
./manage.py cleanup_unused_media
```
By default command runs in interactive mode. And before removing list of files will be displayed. User should confirm the action.

### Options

`--noinput`, `--no-input`

Non interactive mode. Command will remove files without confirmation from user. Useful for scripts.
```
./manage.py cleanup_unused_media --noinput
```

`-e`, `--exclude` 

To avoid operating on files whose names match a particular pattern. Pattern supports only `*` as any symbols. Can use multiple options in one command.

For example, to keep `.gitignore` and `*.png` files you can use:
```
./manage.py cleanup_unused_media -e *.gitignore -e *.png
```

Also you can exclude entire folder or files in that folder (path should be relative to `settings.MEDIA_ROOT`):
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