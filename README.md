# empiricalco.com

The marketing site for Empirical Co Pty Ltd. It is a single static page: plain HTML, CSS and a little JavaScript, with no build step and no dependencies.

```
index.html        All page copy and structure (edit words here)
styles.css        Colours, type and layout (tokens at the top)
main.js           Nav behaviour, section rules, enquiry form
404.html          Not-found page
favicon.svg       Browser icon
assets/           PNG icons and the social share image (og.png)
CNAME             Custom domain for GitHub Pages (empiricalco.com)
tools/            Scripts that regenerate the logo curve and image assets
```

## Editing copy

All the words on the site are in `index.html`. Each section starts with a banner comment such as `<!-- ===== HOW WE ENGAGE ===== -->`, so search for the section name and edit the text between the tags.

The quickest way, with no tools needed:

1. Open `index.html` on GitHub and click the pencil icon.
2. Change the text. Leave the `<tags>` alone.
3. Click **Commit changes**. The live site updates in about a minute.

Some things to keep in mind:

- **Client names.** "Selected experience" lists work by sector only. Add a client's name only after they agree to it in writing.
- **Email address.** `hello@empiricalco.com` appears in four places. To change it, search and replace across `index.html` and `main.js`.
- **Page title and description** (what Google shows) are the `<title>` and `<meta name="description">` near the top of `index.html`.
- **Ampersands** in copy are written `&amp;`, and curly apostrophes as `’`.

## Enquiry form

The form posts to Formspree (form ID `mqayrlvp`), which emails each enquiry. To change the recipient, change it in the Formspree dashboard. To use a different form service, change the form's `action` URL in `index.html`. If the request fails, the form shows an error with the plain email address, so no enquiry is lost silently.

## Look and feel

Colours, fonts and spacing are CSS variables at the top of `styles.css`. The bell curve in the hero is drawn from `tools/curve.py`, a Gaussian matched to the original logo. To regenerate the favicons and share image after a brand change:

```
python3 tools/make_assets.py     # needs Pillow and Google Chrome
```

## Preview locally

```
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Deployment

- Hosting: GitHub Pages, published from the `main` branch root of this repository.
- Domain: `CNAME` contains `empiricalco.com`. DNS is on Cloudflare (proxied) and points at GitHub Pages.
- Every push to `main` deploys automatically. Check progress under the repository's **Actions** tab.
