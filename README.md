# Small Hours — a personal creative home

A complete, responsive static site for poems, essays, stories, photographs, and videos. No browser JavaScript, database, or paid service is needed. Write files; GitHub Actions builds the homepage and individual entry pages on each push.

## Quick start: publish on GitHub Pages

1. Create a GitHub repository with a `main` branch. A public repository is the simplest starting point for free Pages hosting.
2. Add **the contents of this folder** at the repository root, including `.github/workflows/pages.yml`. Do not upload the ZIP itself. If using the GitHub upload interface, check that the hidden `.github` folder was included; otherwise create `.github/workflows/pages.yml` with the GitHub file editor and paste its contents.
3. Open repository **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Commit a change on `main`, or open **Actions → Publish creative home → Run workflow**.
5. Wait for the workflow to finish. The deployment link is shown in the workflow and Pages settings. Repository sites such as `https://USERNAME.github.io/REPOSITORY/` and user sites both work without changing URL settings.

If your default branch is different, update `branches: [main]` in the workflow. Organization policies or account plans may affect Pages availability. Deployment uses the documented GitHub Pages custom-workflow pattern: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Make it yours

Edit `site.json` to change the name, author, introduction, and about text. Edit `assets/style.css` for colors, spacing, and typography, and `templates/page.html` for the shared HTML shell. Sample content and the original SVG artwork are included for you to use or replace.

## Add a post

Create `posts/YYYY-MM-DD-your-title.md` or `.txt`. Filenames must use a valid date and a lowercase slug with letters, numbers, and hyphens. Every published file needs a unique filename; changing it changes the page URL. Posts sort newest first by filename date, with slug as a tie-breaker.

Optional metadata goes at the very top. It uses simple `key: value` lines, not full YAML. Do not quote values. Omitted titles come from the filename.

```markdown
---
title: A walk beside the water
category: Photo essay
excerpt: A small collection from a morning by the sea.
---
Today I took the long way home.

![Sunlight over the water](../assets/my-photo.jpg)

## Something I noticed

Words can be **bold**, *italic*, or [linked](https://example.com).
```

Put pictures in `assets/` and use `../assets/filename.jpg` inside posts. Include meaningful alt text. Use lowercase filenames without spaces for simplicity. All post pages live one level below the homepage, so this relative path works locally and under a GitHub repository URL.

For poetry in Markdown, end a line with two spaces to keep a deliberate line break. Blank lines create stanzas. In `.txt`, spacing and line breaks are preserved and HTML is displayed literally; use `.md` for embedded graphics, formatting, or video.

Set `draft: true` in metadata to omit a draft. Future dates are published immediately: this template does not schedule releases. Commit a new file, edit, or deletion on `main` and GitHub rebuilds the entire collection automatically.

## Photographs and video

A photo entry is simply Markdown with one or more images and optional captions. A video entry can use an HTML embed supplied by your video host; replace the placeholder ID below with your own. YouTube embeds load an external service when someone opens the post.

```html
<iframe src="https://www.youtube-nocookie.com/embed/YOUR_VIDEO_ID"
  title="Describe your film" loading="lazy" allowfullscreen></iframe>
```

For a small self-hosted clip, add the files to `assets/`:

```html
<video controls preload="metadata" poster="../assets/film-poster.jpg">
  <source src="../assets/film.mp4" type="video/mp4">
  <track kind="captions" src="../assets/film-en.vtt" srclang="en" label="English" default>
  Your browser cannot play this video.
</video>
```

Supply captions or a text transcript for videos. Large media is better kept on a video host; GitHub repositories and Pages have storage/bandwidth limits. Authored Markdown allows raw HTML for creative flexibility: publish only content you trust. This is a personal authoring system, not a public file-upload service.

## Preview on your computer

Python 3.10+ is required. From this folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python build.py
python test_site.py
python -m http.server 8000 --directory dist
```

On Windows, activate with `.venv\Scripts\activate` instead. Open http://localhost:8000 and stop the server with Ctrl+C. Rebuild after editing; the server itself does not rebuild files. You can also open the included `dist/index.html` directly for an immediate preview. The generated `dist/` is a replaceable preview, never the source for your writing.

## Folder structure

```text
.github/workflows/pages.yml   Automatic build and Pages deployment
posts/                       Your .md and .txt entries
assets/                      Images, video, captions, and stylesheet
site.json                    Site name and personal introduction
templates/page.html          Shared HTML layout
build.py                     Generates homepage, post pages, navigation
requirements.txt             Pinned Markdown dependency
test_site.py                 Local link, asset, anchor, navigation checks
dist/                        Complete ready-to-browse generated website
```

There is no browser folder enumeration: the Python build reads `posts/` and emits complete HTML pages. No manual post index is needed. The homepage displays categories as labels, not interactive filters. Comments, newsletters, and subscriptions are not included; you can add an external service later. This template has no tracking or external fonts.

## Troubleshooting

- **Workflow missing:** ensure `.github/workflows/pages.yml` is in the repository root, not inside a wrapper folder.
- **Deployment permission error:** select GitHub Actions in Pages settings and check repository/organization Actions permissions.
- **Build error:** the log names invalid filenames, dates, or malformed metadata. Correct the file and commit again.
- **Image missing:** check capitalization and use `../assets/...` from post content.
- **Updates absent:** check the workflow ran on `main` and completed successfully.

## Reuse

Template code and original sample writing/artwork are released under the MIT license in LICENSE. Replace the sample author and content before presenting the site as your personal work.
