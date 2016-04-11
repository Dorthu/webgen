from dateutil.parser import parse as parse_date
from apiclient.discovery import build

def _get_post(post):
   post_date = parse_date(post['published'])

   parts = post['title'].split('--')
   if len(parts) > 1:
       ptitle = ''.join(parts[:-1])
       psubtitle = parts[-1]
   else:
       ptitle = parts[0]
       psubtitle = None

   return {
        "type": "post",
        "stamp": post_date.timestamp(),
        "posted": post_date,
        "content": post['content'],
        "post_url": post['url'],
        "title": ptitle,
        "subtitle": psubtitle,
    }

def load_content(config):

    api = build('blogger', 'v3', developerKey=config['api_key'])
    posts = api.posts().list(blogId=config['blog_id']).execute()
    ret = []

    if not 'items' in posts or not len(posts['items']):
        return ret

    for p in posts['items']:
        ret.append(_get_post(p))

    return ret
