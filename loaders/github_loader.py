import github

def _process_event(e, result_list):
    if not e.type in ('CreateEvent', 'PushEvent'):
        return

    result = {
        "type": "github",
        "stamp": e.created_at.timestamp(),
        "repo": e.repo.name,
        "timestamp": e.created_at,
    }

    if e.type == 'CreateEvent':
        result.update({
            "icon": "create",
            "content": e.payload['description'],
        })
        result_list.append(result)
    elif e.type == 'PushEvent':
        result.update({
            "icon": "push",
            "content": "pushed {} commit{} to {}".format(e.payload['distinct_size'],
                's' if e.payload['distinct_size'] > 1 else '',
                e.payload['ref'].split('/')[-1]),
        })
        result_list.append(result)

def load_content(config):
    g = github.MainClass.Github()
    u = g.get_user(config['username'])
    ret = []
    for e in u.get_events():
        _process_event(e, ret)

    return ret
