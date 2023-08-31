#!/usr/bin/env python3

# -*- coding: utf-8 -*-

name = 'mastodon_2_album'

from telegram_util import AlbumResult as Result
from telegram_util import isInt
from bs4 import BeautifulSoup
import re

def getReblogsCount(status):
    try:
        return status.reblogs_count + status.reblog.reblogs_count
    except:
        return status.reblogs_count

def getReblogsCountRaw(status):
    try:
        if status.reblogs_count == 0:
            return '%d' % status.reblog.reblogs_count
        return '%d %d' % status.reblog.reblogs_count, status.reblogs_count
    except:
        return '%d' % status.reblogs_count

def getContentText(status):
    content = status.content
    soup = BeautifulSoup(content, 'html.parser')
    content = str(soup).replace('<br/>', '\n')
    soup = BeautifulSoup(content, 'html.parser')
    result = []
    for paragraph in soup.find_all('p'):
        text = paragraph.text
        if len(text.split()) == 1 and text.startswith('@'):
            continue
        result.append(text)
    result = '\n\n'.join(result)
    if status.spoiler_text:
        result = status.spoiler_text + '\n\n' + result
    return result

def getMediaAttachments(status):
    media_attachments = status.media_attachments
    try:
        media_attachments += status.reblog.media_attachments
    except:
        ...
    deduped_media_attachments = []
    media_ids = set()
    for media in media_attachments:
    	if media.id in media_ids:
    		continue
    	deduped_media_attachments.append(media)
    	media_ids.add(media.id)
    return deduped_media_attachments

def getImages(status):
    media_attachments = getMediaAttachments(status)
    # if not [media for media in media_attachments if media.type == 'image']:
    #     return []
    return [media.remote_url or media.url for media in media_attachments]

def getVideo(status):
    return
    # media_attachments = getMediaAttachments(status)
    # if [media for media in media_attachments if media.type == 'image']:
    #     return
    # for media in media_attachments:
    #     if media.type != 'image':
    #         return media.remote_url or media.url

def getOriginCap(status):
    try:
        return getContentText(status.reblog)
    except:
        return ''

def getCap(status):
    cap = getContentText(status)
    origin_cap = getOriginCap(status)
    if not origin_cap:
        return cap
    if not cap:
        return origin_cap
    return origin_cap + '\n\n【网评】' + cap

def getUrl(status):
    if status.url and not status.url.endswith('/activity'):
        return status.url
    return status.reblog.url

def getOrigin(mastodon, status):
    if status.in_reply_to_id:
        try:
            origin_status = mastodon.status(status.in_reply_to_id)
            return ' <a href="%s">origin</a>' % origin_status.url
        except:
            ...
    return ''

def get(mastodon, status):
    r = Result()
    r.imgs = getImages(status)
    r.video = getVideo(status)
    r.cap_html_v2 = getCap(status) + getOrigin(mastodon, status)
    r.url = getUrl(status)
    return r

def getFromUrl(mastodon, url):
    for status in mastodon.search_v2(url)['statuses']:
        if getUrl(status) == url:
            return get(mastodon, status)
    return Result()

def getHash(status):
    cap = getContentText(status)
    origin_cap = getOriginCap(status)
    raw_content = origin_cap + cap
    raw_content += ''.join(getImages(status))
    raw_content += str(getVideo(status))
    result = []
    for x in raw_content:
        if re.search(u'[\u4e00-\u9fff]', x):
            result.append(x)
            if len(result) > 10:
                break
    return ''.join(result)

def getAuthor(status):
    try:
        return status.reblog.account
    except:
        return status.account

def getCommenter(status):
    if getAuthor(status).id != status.account.id:
        return status.account

def getUserInfo(account, key):
    if not account:
        return ''
    return '[%s](%s): %s %d' % (key, account.url, account.display_name or account.username, account.id)

def yieldUsersRawInfo(status):
    users = [getCommenter(status), getAuthor(status)]
    users = [user for user in users if user]
    for user in users:
        yield user.id, user.url + ' ' + user.display_name

def getLog(status):
    return 'count: %s ' % getReblogsCountRaw(status) + '%s' + '%s %s' % (
        getUserInfo(getAuthor(status), 'author'), getUserInfo(getCommenter(status), 'commenter'))

def getCoreContent(status):
    result = []
    for user_id, user_info in yieldUsersRawInfo(status):
        result.append('%d %s' % (user_id, user_info))
    result += [getContentText(status), getOriginCap(status)]
    return '=' + ' '.join(result)

def findAccount(mastodon, text):
    if isInt(text):
        return mastodon.account(int(text))
    if '/' in text:
        text = text.strip('/')
        pieces = text.split('/')
        text = pieces[-1].strip('@') + '@' + pieces[2]
    account = mastodon.account_lookup(text)
    print('account_lookup', account)
    if account:
        return account
    return mastodon.account_search(text)[0]

def getTwitterReplace(item):
    if item.startswith('https://bird.makeup/@'):
        user = item.split('/')[3][1:]
        status_id = item.split('/')[4]
        return 'https://twitter.com/%s/status/%s' % (user, status_id)
    if item.startswith('https://bird.makeup/users/'):
        user = item.split('/')[4]
        status_id = item.split('/')[6]
        return 'https://twitter.com/%s/status/%s' % (user, status_id)
    if item.startswith('https://twitter.com/i/web/status'):
        return ''

def toTwitterContent(content):
    for item in re.split('\"|\n|\s', content):
        replace = getTwitterReplace(item)
        if replace != None:
            content = content.replace(item, replace)
    return content.strip()
    
def toTwitter(album):
    album.url = getTwitterReplace(album.url)
    album.cap_html_v2 = toTwitterContent(album.cap_html_v2)
    return album