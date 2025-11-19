"""Render the Jinja templates to a static `site/` directory.

This script does a minimal emulation of Flask's `url_for`, `session`, `g`, and
`get_flashed_messages` so the existing templates render to static HTML.

Run: python build_static.py
Output: `site/` folder containing HTML files and copied `static/` assets.
"""
import os
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape


TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
OUT_DIR = os.path.join(os.path.dirname(__file__), 'site')

# Map Flask endpoint names to output filenames
ENDPOINT_MAP = {
    'home': 'index.html',
    'todaystasks': 'todaystasks.html',
    'leaderboards': 'leaderboards.html',
    'pointshop': 'pointshop.html',
    'login': 'login.html',
    'register': 'register.html',
    'profile_settings': 'profile_settings.html',
    'logout': 'index.html',
}


def url_for(endpoint, **kwargs):
    """Minimal url_for replacement used in templates.

    - url_for('static', filename='x') -> 'static/x'
    - url_for('<endpoint>') -> mapped filename or '#'
    """
    if endpoint == 'static':
        return os.path.join('static', kwargs.get('filename', ''))
    return ENDPOINT_MAP.get(endpoint, '#')


def get_flashed_messages():
    # Static site: no runtime flash messages
    return []


def build():
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(['html', 'xml'])
    )

    # Inject minimal globals used by the templates
    env.globals['url_for'] = url_for
    env.globals['get_flashed_messages'] = get_flashed_messages
    # session and g are used in templates; provide safe defaults
    env.globals['session'] = {'logged_in': False}
    env.globals['g'] = {'user': None}
    # Some templates expect a `user` variable passed in (Flask passed it explicitly)
    # Provide a safe, empty user dict so attribute access doesn't fail during rendering.
    env.globals['user'] = {
        'first_name': '',
        'last_name': '',
        'email': '',
        'account_name': '',
        'username': ''
    }

    # Ensure output directory exists
    if os.path.exists(OUT_DIR):
        print('Cleaning existing', OUT_DIR)
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR, exist_ok=True)

    # Templates we want to render to standalone pages (route-like)
    pages = [
        'home.html',
        'todaystasks.html',
        'leaderboards.html',
        'pointshop.html',
        'login.html',
        'register.html',
        'profile_settings.html',
    ]

    for tpl_name in pages:
        try:
            tpl = env.get_template(tpl_name)
        except Exception as e:
            print('Skipping', tpl_name, 'failed to load template:', e)
            continue

        rendered = tpl.render()

        out_name = ENDPOINT_MAP.get(os.path.splitext(tpl_name)[0], tpl_name)
        out_path = os.path.join(OUT_DIR, out_name)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print('Wrote', out_path)

    # Copy static assets
    dest_static = os.path.join(OUT_DIR, 'static')
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, dest_static)
        print('Copied static assets to', dest_static)
    else:
        print('No static/ directory found; skipping copy')


if __name__ == '__main__':
    build()
