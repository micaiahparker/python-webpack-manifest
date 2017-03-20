python-webpack-manifest
=======================

Manifest loader that allows you to include references to files built by webpack. Handles manifests generated by the [webpack-yam-plugin](https://github.com/markfinger/webpack-yam-plugin).

- Load references to webpack assets
- Uses relative paths to ensure that manifests+assets can be pre-built and deployed across environments
- Caches file reads to reduce overhead in production environments
- Provides an opt-in debug mode which disables caching and blocks the python process as webpack completes re-builds
- Designed to be optionally packaged with redistributable apps+libraries that need to avoid dependency-hell.

If you are using webpack with Django, you might also want to check out Owais' [django-webpack-loader](https://github.com/owais/django-webpack-loader/) project. He has some great docs and the project has a lot of use. This project originated as a re-implementation of django-webpack-loader as I needed support for some of the above features. Personally, I continue to use this project in Django projects by exposing the manifest to templates via a call to `webpack_manifest.load(...)` in a context processor.


Documentation
-------------

- [Installation](#installation)
- [Usage](#usage)
- [How to run the tests](#how-to-run-the-tests)


Installation
------------

If you're using this in a project, use `pip`

```
pip install webpack-manifest
```

If you're using this in an redistributable app or library, just copy the [loader's file](webpack_manifest/webpack_manifest.py)
in so that you can avoid causing any dependency pains downstream.


Usage
-----

```python
import webpack_manifest
```

Once you've imported the manifest loader...

```python
manifest = webpack_manifest.load(
    # An absolute path to a manifest file
    path='/abs/path/to/manifest.json',

    # The root url that your static assets are served from
    static_url='/static/',

    # optional args...
    # ----------------

    # Ensures that the manifest is flushed every time you call `load(...)`
    # If webpack is currently building, it will also delay until it's ready.
    # You'll want to set this to True in your development environment
    debug=False,

    # Max timeout (in seconds) that the loader will wait while webpack is building.
    # This setting is only used when the `debug` argument is True
    timeout=60,

    # If a manifest read fails during deserialization, a second attempt will be
    # made after a small delay. By default, if `read_retry` is `None` and `debug`
    # is `True`, it well be set to `1`
    read_retry=None,

    # If you want to access the actual file content, provide the build directory root
    static_root='/var/www/static/',
)

# `load` returns a manifest object with properties that match the names of
# the entries in your webpack config. The properties matching your entries
# have `js` and `css` properties that are pre-rendered strings that point
# to all your JS and CSS assets. Additionally, access internal entry data with:
# `js.rel_urls` and `css.rel_urls` - relative urls
# `js.content` and `css.content` - raw string content
# `js.inline` and `css.inline` - pre-rendered inline asset elements

# A string containing pre-rendered script elements for the "main" entry
manifest.main.js  # '<script src="/static/path/to/file.js"></script><script ... >'

# A string containing pre-rendered link elements for the "main" entry
manifest.main.css  # '<link rel="stylesheet" href="/static/path/to/file.css"><link ... >'

# A string containing pre-rendered link elements for the "vendor" entry
manifest.vendor.css  # '<link rel="stylesheet" href="/static/path/to/file.css"><link ... >'

# A list containing relative urls (without the static url) to the "vender" entry
manifest.vendor.css.rel_urls  # ['path/to/file.css', 'path/to/another.css', ...]

# A string containing concatenated script elements for the "main" entry
manifest.main.js.content  # '/* content of file1.js, files2.js, ...*/'

# A string containing pre-rendered inline script elements for the "main" entry
manifest.main.js.inline  # '<script>/* content of file1.js, files2.js, ...*/</script>'

# A string containing pre-rendered inline style elements for the "main" entry
manifest.main.css.inline  # '<style>/* content of file1.css, files2.css, ...*/</style>'

# Note: If you don't name your entry, webpack will automatically name it "main".
```


How to run the tests
--------------------

```
pip install -r requirements.txt
nosetests
```
