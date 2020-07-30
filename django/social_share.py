from urllib.parse import urlencode, urljoin

def facebook(url, image, title, quote, description, caption):
    """A definition that helps create links to be able to share
    content on facebook
    """
    base_url = 'https://www.facebook.com/sharer/sharer.php'

    items = {
        'u': url,
        'picture': image,
        'title': title,
        'quote': quote,
        'description': description,
        'caption': caption
    }

    return urljoin(base_url, '?' + urlencode(items))

def twitter(message, *hashtags):
    """A definition that helps create links to be able to share
    content on twitter
    """
    base_url = 'https://twitter.com/intent/tweet'

    items = {
        'text': message,
        'hashtags': ','.join(hashtags)
    }
    return urljoin(base_url, '?' + urlencode(items))

def reddit(url, title):
    base_url = 'http://www.reddit.com/submit'

    items = {
        'url': url,
        'title': title
    }
    return urljoin(base_url, '?' + urlencode(items))

def gmail(email, cc:list=None, bcc:list=None):
    """Creates a link that can be used to automatically use gmail to send emails"""

    base_url = 'https://mail.google.com/mail/u/0/'

    items = {
        'view': 'cm',
        'fs': 1,
        'tf': 1,
        'to': email,
    }
    if cc:
        items.update({'cc': ','.join(cc)})
    if bcc:
        items.update({'cc': ','.join(bcc)})
    return urljoin(base_url, '?' + urlencode(items))
