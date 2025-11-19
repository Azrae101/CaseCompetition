# Static build of the CogCards site

This repo originally used Flask. This project includes a small static site generator
(`build_static.py`) that renders the Jinja templates into pure HTML files and copies
the `static/` assets into a `site/` directory.

How to build

1. Install Jinja2 if you don't have it:

   pip install jinja2

2. Run the builder from the project root (where `build_static.py` is):

   python build_static.py

This will create a `site/` folder with rendered HTML and a `site/static/` copy of
the static assets.

How to serve

You can serve the `site/` folder easily with Python's built-in HTTP server:

```powershell
cd site
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

Notes / assumptions

- The generator provides minimal stubs for Flask globals (e.g. `session`, `g`).
- Dynamic features (login, forms, database-driven content) will be rendered
  with default static placeholders. If you want client-side interactivity you
  can add JavaScript that talks to an API or embeds static data files.
- `app.py` and the `database/` remain untouched; this tool simply renders
  static HTML from your templates.

If you'd like, I can:

- Make the generator pull sample user / leaderboard data from JSON to make the
  leaderboards and profile pages look populated.
- Convert more templates or tweak relative links.
