import re
import sys
import cgi as urlparse
import urllib2

import xbmcgui
import xbmcplugin
import xbmcaddon

class PixelTVAddon(object):
    def showCategories(self):
        u = urllib2.urlopen('http://www.pixel.tv/')
        html = u.read()
        u.close()

        for m in re.finditer('<a href="/programmer/([^/]+)/" onmouseout="UnTip\(\);" onmouseover="Tip\(\'([^\']+)\'\);"><img src="([^"]+)" alt="([^"]+)">', html):
            slug = m.group(1)
            description = m.group(2).replace('<strong>', '[B]').replace('</strong>', '[/B]').replace('<br>', '\n')
            icon = 'http://www.pixel.tv%s' % m.group(3)
            title = m.group(4)

            item = xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
            item.setInfo(type = 'video', infoLabels = {
                'title' : title,
                'plot' : description
            })
            url = PATH + '?slug=' + slug + '&page=1'
            xbmcplugin.addDirectoryItem(HANDLE, url, item, True)

        xbmcplugin.endOfDirectory(HANDLE)

    def showCategory(self, slug, page):
        if page == 1:
            url = 'http://www.pixel.tv/programmer/%s/' % slug
        else:
            url = 'http://www.pixel.tv/programmer/%s/%s' % (slug, page)

        u = urllib2.urlopen(url)
        html = u.read()
        u.close()

        for m in re.finditer('<small>([^<]+)</small></td><td>.*?<a href="([^"]+)"><small>.*?</small>([^<]+)</a>', html):
            #date = m.group(1)
            playlist = m.group(2)
            title = m.group(3)

            item = xbmcgui.ListItem(title)
            item.setProperty('IsPlayable', 'true')
            url = PATH + '?playlist=' + playlist
            xbmcplugin.addDirectoryItem(HANDLE, url, item)

        page += 1
        if re.search('/programmer/%s/%d' % (slug, page), html):
            item = xbmcgui.ListItem('XXXldre indslag...')
            url = PATH + '?slug=' + slug + '&page=' + str(page)
            xbmcplugin.addDirectoryItem(HANDLE, url, item, True)

        xbmcplugin.endOfDirectory(HANDLE)


    def playClip(self, playlist):
        u = urllib2.urlopen('http://www.pixel.tv%s' % playlist)
        html = u.read()
        u.close()

        m = re.search('/([0-9]+/pixelV2)', html)
        path = m.group(1)

        item = xbmcgui.ListItem(path = 'http://files.pixel.tv/video/' + path)
        xbmcplugin.setResolvedUrl(HANDLE, True, item)

if __name__ == '__main__':
    ADDON = xbmcaddon.Addon(id = 'plugin.video.pixel.tv')
    PATH = sys.argv[0]
    HANDLE = int(sys.argv[1])
    PARAMS = urlparse.parse_qs(sys.argv[2][1:])

    ptv = PixelTVAddon()
    if PARAMS.has_key('slug'):
        ptv.showCategory(PARAMS['slug'][0], int(PARAMS['page'][0]))
    elif PARAMS.has_key('playlist'):
        ptv.playClip(PARAMS['playlist'][0])
    else:
        ptv.showCategories()

