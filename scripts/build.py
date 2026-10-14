"""Build the static site. pCloud share pages load their configured URLs directly."""
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent


def build():
    out = ROOT / '_site'
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    for path in ROOT.iterdir():
        if path.name == 'assets' and path.is_dir():
            shutil.copytree(path, out / path.name)
        elif path.is_file() and (path.suffix in ('.html', '.css', '.js') or path.name in ('.nojekyll', 'CNAME', 'site-config.json')):
            shutil.copy2(path, out / path.name)
    aliases = {'files': 'filer.html', 'videos': 'videos.html', 'images': 'images.html', 'links': 'links.html', 'upload': 'upload.html', 'help': 'hjaelp.html'}
    for slug, filename in aliases.items():
        folder = out / slug
        folder.mkdir()
        html = (ROOT / filename).read_text(encoding='utf-8')
        html = html.replace('<head>', '<head><base href="../">', 1)
        (folder / 'index.html').write_text(html, encoding='utf-8')
    print('Static site prepared. pCloud share and upload links are loaded directly from site-config.json.')


if __name__ == '__main__':
    build()
