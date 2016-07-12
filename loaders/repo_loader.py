# This expects a repository with a blog directory and a series of .md files in that
# directory that are blog posts.  Also expects the files to start like this:
# blog-entry
# 2016-05-01
# Post Title
# Post Subtitle
# -----
import os
import shutil
import markdown
from urllib.parse import quote
from datetime import datetime

def _update_repo(path):
    result = os.system('git --git-dir={0}/.git --work-tree={0} pull'.format(path))
    if not result:
        print("updating repo failed: {}".format(result))

def _copy_images(path):
    if not os.path.isdir('output/img'):
        os.mkdir('output/img')
    if os.path.isdir("{}/img".format(path)):
        for f in os.listdir("{}/img".format(path)):
            if os.path.isfile("{}/img/{}".format(path, f)):
                shutil.copy("{}/img/{}".format(path, f), 'output/img/{}'.format(f))

def _load_file(f):
    try:
        sanity = next(f).rstrip()
        if not sanity == 'blog-entry':
            return None # don't know what we're reading
        publish = next(f).rstrip()
        title = next(f).rstrip()
        subtitle = next(f).rstrip()
        sanity = next(f).rstrip()
        if not sanity == '-----':
            return None # again, we're malformed
    except TypeError as e:
        # malformed file - bail
        return None

    publish_date = datetime.strptime(publish, "%Y-%m-%d")

    raw_md = f.read()
    parsed_md = markdown.markdown(raw_md)

    page_title = title.replace(' ','-')
    return {
        "type": "post",
        "stamp": publish_date.timestamp(),
        "posted": publish_date,
        "content": parsed_md,
        "post_url": '{}.html'.format(page_title),
        "title": title,
        "subtitle": subtitle,
        "page-title": page_title,
        "page": True,
    }

def _load_files(path):
    files = [ "{}/{}".format(path, f) for f in os.listdir(path) if f.endswith('.md') ]
    ret = []
    
    for f in files:
        with open(f) as fl:
            ret.append(_load_file(fl))

    rettt= [ r for r in ret if r ]
    return rettt

def load_content(config):
    path = os.path.expanduser(config['repo_dir'])
    if os.path.isdir(path) and os.path.isdir('{}/entries'.format(path)):
        _update_repo(path)
        _copy_images(path)
        return _load_files('{}/entries'.format(path))
    return []
