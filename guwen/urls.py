from django.conf.urls import patterns, url

urlpatterns = patterns('guwen.views',
	url(r'^$', 'home', name='home'),
    url(r'^frame/(\w+)/(\d+)', 'hanzi_show', name='hanzi_show'),
    url(r'^hanzi_list', 'hanzi_list', name='hanzi_list'),
    url(r'^cedict_update', 'cedict_update', name='cedict_update'),
    url(r'^update_lexical_data', 'lexical_data_update', name='lexical_data_update'),
    url(r'^convert_pinyin_all', 'convert_pinyin_all'),
    url(r'^search', 'search', name='search'),
    url(r'^hanzi_edit/(\d+)', 'hanzi_edit', name='hanzi_edit'),
    url(r'^hanzi_add', 'hanzi_add', name='hanzi_add'),
    url(r'^guestbook', 'guestbook', name='guestbook'),
	)
