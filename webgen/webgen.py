from jinja2 import Environment, FileSystemLoader
from importlib.machinery import SourceFileLoader
import configparser
import sass
import os

def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config
    

def generate(config_path):
    modules = []
    posts = []
    config = load_config(config_path)
    pages = []

    for f in os.listdir(config['global']['loaders_dir']):
        if f[-3:] == '.py':
            s = SourceFileLoader(f[:-3], '{}/{}'.format(config['global']['loaders_dir'], f)).load_module()
            modules.append(s)
            if f[:-3] in config:
                posts += s.load_content(config[f[:-3]])

    posts.sort(key=lambda s: s['stamp'])
    posts.reverse()

    pages = [ p for p in posts if 'page' in p ]

    env = Environment(loader=FileSystemLoader(config['global']['templates_dir']))
    t = env.get_template('index.html')

    with open('output/index.html', 'w') as f:
        f.write(t.render(features=posts))

    pt = env.get_template('page.html')
    for p in pages:
        with open('output/entries/{}.html'.format(p['page-title']), 'w') as f:
            f.write(pt.render(data=p, features=posts))

    compiled_sass = ""

    for f in os.listdir('./sass'):
        if f[-5:] == '.scss':
            with open("sass/{}".format(f)) as fh:
                compiled_sass += sass.compile(string=fh.read())

    with open('output/style.css', 'w') as f:
        f.write(compiled_sass)

    print("done")
