import base64, re, pathlib

src = pathlib.Path('/home/user/Project-Manzil/index.html').read_text(encoding='utf-8')
lines = src.split('\n')

# 1-indexed slices confirmed by inspection
style_block = '\n'.join(lines[28:425])   # <style> ... </style>
body_block  = '\n'.join(lines[593:1775]) # inside <body> ... </body>

# --- asset: the only image the site uses, inlined so the preview is self-contained
mark = base64.b64encode(
    pathlib.Path('/home/user/Project-Manzil/manzil-mark.png').read_bytes()
).decode()
mark_uri = f'data:image/png;base64,{mark}'
body_block = body_block.replace('src="manzil-mark.png"', f'src="{mark_uri}"')
assert mark_uri in body_block

# --- three.js: vendored locally on the real site, from the allowed CDN here
body_block = body_block.replace(
    "lib.src = 'three.min.js';",
    "lib.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';")
assert 'cdnjs.cloudflare.com/ajax/libs/three.js' in body_block

# --- the other pages are single files on the live site; point at the live copies
for page in ('privacy.html', 'terms.html'):
    body_block = body_block.replace(
        f'href="{page}"',
        f'href="https://projectmanzil.netlify.app/{page}" target="_blank" rel="noopener"')

# --- the form cannot submit here; say so plainly rather than let it look broken
body_block = body_block.replace(
    '<p>Takes under a minute. No documents needed at this stage.</p>',
    '<p>Takes under a minute. No documents needed at this stage.</p>\n'
    '          <p class="preview-formnote">Preview only — this form does not send. '
    'Enquiries on the live site reach you as normal.</p>')

title = 'Manzil Properties'

banner_css = """
<style>
  .preview-ribbon{
    background:var(--navy-950);color:rgba(255,255,255,.82);
    font-family:'Times New Roman',Times,serif;font-size:14px;line-height:1.5;
    padding:10px 24px;text-align:center;border-bottom:1px solid rgba(217,178,92,.35);
  }
  .preview-ribbon b{color:var(--gold-400);font-weight:700;}
  .preview-formnote{
    margin:10px 0 0;padding:9px 12px;border-radius:8px;
    background:#fff8ea;border:1px solid #f0dfb4;color:#7a5c17;
    font-size:13.5px;line-height:1.5;
  }
</style>"""

banner_html = ('<div class="preview-ribbon"><b>Preview</b> — working copy of the '
               'Manzil Properties site. Your live site is unaffected.</div>')

out = (f'<title>{title}</title>\n{style_block}\n{banner_css}\n{banner_html}\n{body_block}\n')
dest = pathlib.Path('/tmp/claude-0/-home-user-Project-Manzil/969ce45f-fb09-5f81-a8f6-b5a4eb94b9ff/scratchpad/manzil-preview.html')
dest.write_text(out, encoding='utf-8')

# sanity checks
for bad in ('<!DOCTYPE', '<html', '<head>', '<body>', 'manzil-mark.png', "'three.min.js'"):
    assert bad not in out, f'leaked: {bad}'
print('written:', dest, f'{dest.stat().st_size/1024:.0f} KB')
print('calculator present:', 'BUYER_RULES' in out)
print('skyline present:   ', 'initSkyline' in out or 'skylineCanvas' in out)
print('faq present:       ', out.count('faq-q'))
