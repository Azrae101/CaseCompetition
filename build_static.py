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
        # Fix links that reference templates/ so built site uses root-relative filenames
        # If templates contain links like "templates/todaystasks.html" (for direct preview)
        # convert them to "todaystasks.html" in the built `site/` output.
        rendered = (rendered
                    .replace('href="templates/', 'href="')
                    .replace("href='templates/", "href='")
                    .replace('href="/templates/', 'href="')
                    .replace("href='/templates/", "href='"))

        out_name = ENDPOINT_MAP.get(os.path.splitext(tpl_name)[0], tpl_name)
        out_path = os.path.join(OUT_DIR, out_name)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print('Wrote', out_path)

        # Also write a preview-style copy under site/templates/ so the deployed
        # GitHub Pages URL can serve the same path as the preview (e.g.
        # /<repo>/templates/home.html).
        preview_dir = os.path.join(OUT_DIR, 'templates')
        os.makedirs(preview_dir, exist_ok=True)
        preview_content = rendered
        # Adjust asset paths for files placed inside site/templates/
        # - /static/...  -> ../static/...
        preview_content = preview_content.replace('href="/static/', 'href="../static/')
        preview_content = preview_content.replace("href='/static/", "href='../static/")
        preview_content = preview_content.replace('src="/static/', 'src="../static/')
        preview_content = preview_content.replace("src='/static/", "src='../static/")

        # Adjust links that point to templates/ so they are local to the templates/ folder
        preview_content = preview_content.replace('href="/templates/', 'href="')
        preview_content = preview_content.replace("href='/templates/", "href='")
        preview_content = preview_content.replace('href="templates/', 'href="')
        preview_content = preview_content.replace("href='templates/", "href='")

        # Make sure links to the site's index point to the parent folder
        preview_content = preview_content.replace('href="index.html"', 'href="../index.html"')
        preview_content = preview_content.replace("href='index.html'", "href='../index.html'")

        preview_path = os.path.join(preview_dir, out_name)
        with open(preview_path, 'w', encoding='utf-8') as pf:
            pf.write(preview_content)
        print('Wrote preview copy', preview_path)

    # Copy static assets
    dest_static = os.path.join(OUT_DIR, 'static')
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, dest_static)
        print('Copied static assets to', dest_static)
    else:
        print('No static/ directory found; skipping copy')

    # Overwrite the root index with a redirect to the preview-style page under /templates/
    # This ensures the project Pages root (https://<user>.github.io/<repo>/)
    # redirects to https://<user>.github.io/<repo>/templates/home.html instead of
    # an absolute /templates/... path which would point to the user site root.
    redirect_target = 'templates/home.html'
    redirect_html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url={redirect_target}">
  <meta name="robots" content="noindex">
  <title>Redirecting...</title>
</head>
<body>
  <p>Redirecting to <a href="{redirect_target}">{redirect_target}</a></p>
  <script>location.replace('{redirect_target}')</script>
</body>
</html>'''

    index_path = os.path.join(OUT_DIR, 'index.html')
    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(redirect_html)
        print('Wrote redirect index at', index_path)
    except Exception as e:
        print('Failed to write redirect index:', e)


if __name__ == '__main__':
    build()
