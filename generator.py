from jinja2 import Environment, FileSystemLoader
from importlib.machinery import SourceFileLoader
import sass
import os

modules = []
posts = []

for f in os.listdir('./loaders'):
    if f[-3:] == '.py':
        s = SourceFileLoader(f[:-3], './loaders/{}'.format(f)).load_module()
        modules.append(s)
        posts += s.load_content()

posts.sort(key=lambda s: s['stamp'])
posts.reverse()

env = Environment(loader=FileSystemLoader('./templates'))
t = env.get_template('index.html')

with open('output/index.html', 'w') as f:
    f.write(t.render(features=posts))

compiled_sass = ""

for f in os.listdir('./sass'):
    if f[-5:] == '.scss':
        with open("sass/{}".format(f)) as fh:
            compiled_sass += sass.compile(string=fh.read())

with open('output/style.css', 'w') as f:
    f.write(compiled_sass)

print("done")
