import re
from urllib.parse import urlencode
from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user  # noqa F401

logger = init_logger(app_type='confluence')


# @run_as_specific_user(username='admin', password='admin')  # run as specific user
@confluence_measure("locust-instantsearch:call-search-action-with-complex-params")
def app_specific_action(locust):
    params = {
        'decorator': 'none',
        'queryString': 'page',
        'showSpaceKey': 'true',
        'showDateCreated': 'true',
        'showDateLastModified': 'true',
        'limit': '200',
        'showLabels': 'true',
        'showBreadCrumbs': 'true',
        'likesFilter': '>-1',
        'showLikes': 'true',
        'track': 'true',
    }
    r = locust.get('/plugins/instantsearch/instantsearch.action?' + urlencode(params), catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content
    print(content)

    assert 'plugin_instantsearch_returnedSearchResult' in content
    if ('plugin_instantsearch_row' in content):
        #if we have matching result, then there must be like, last modified, created date, etc due to query params above
        assert 'Created:&nbsp;' in content
        assert 'Last&nbsp;Modified:' in content
        assert 'thumbs_up.png' in content