import codecs
import json
import os

from collections import defaultdict
from functools import partial
from itertools import count

import pytest

import logging
logger = logging.getLogger(__name__)


counters = defaultdict(dict)


def get_count(kind='png', name='screenshot'):

    # ensure good registry
    counters[kind] = counters.get(kind, {})
    counters[kind][name] = counters[kind].get(name, count())

    return counters[kind][name].next()


def get_filename(kind='png', name='screenshot'):
    return '{0}-{1}.{2}'.format(name, get_count(kind=kind, name=name), kind)


def screenshot(browser, name='screenshot', dir_='/tmp'):

    # shortcuts
    path = os.path.join(dir_, get_filename(kind='png', name=name))

    # succeed ?
    if browser.driver.get_screenshot_as_file(path):
        logger.debug('path: {0}'.format(path))
        return path


def dumphtml(browser, name='dump', dir_='/tmp'):

    # shortcuts
    path = os.path.join(dir_, get_filename(kind='html', name=name))

    with codecs.open(path, 'wb', encoding='utf-8') as dump:
        dump.write(browser.html)

    logger.debug('path: {0}'.format(path))
    return path


def get_by_id(browser, id_):
    """Returns just first element found or None.
    """
    if browser.is_element_present_by_id(id_):
        return browser.driver.find_element_by_id(id_)


def get_by_css(browser, selector):
    """Returns just first element found or None.
    """
    if browser.is_element_present_by_css(selector):
        return browser.driver.find_element_by_css_selector(selector)


def get_by_xpath(browser, path):
    """Returns just first element found or None.
    """
    if browser.is_element_present_by_xpath(path):
        return browser.driver.find_element_by_xpath(path)


def get_by_name(browser, name):
    """Returns just first element found or None.
    """
    if browser.is_element_present_by_name(name):
        return browser.driver.find_element_by_name(name)


SCRIPT_DOWNLOAD_TMPL = """
jQuery.get('{0}', function(data) {{
    var _str = JSON.stringify(data);
    var el = jQuery('body');
    el.append('<div id="{1}">' + _str + '</div>');
}})
"""


SCRIPT_REMOVE_TMPL = """
jQuery('{0}').remove()
"""


def get_ajax(browser, url, uri, name='ajax'):
    """Returns dowloaded content through very ugly ajax way.
    """
    # id_ of the element to populate
    id_ = '__{0}_{1}_id'.format(name, get_count(kind='id', name=name))

    # retrieve data
    browser.execute_script(SCRIPT_DOWNLOAD_TMPL.format(url(uri), id_))

    # get populated element
    el = browser.get_by_id(id_)

    # parse data
    data = json.loads(el.text)

    # remove element after all
    browser.execute_script(SCRIPT_REMOVE_TMPL.format('#%s' % id_))

    return data


SCRIPT_SET_VALUE = """
jQuery('%s').val('%s')
"""


def set_value(browser, selector, value):
    browser.execute_script(SCRIPT_SET_VALUE % (selector, value))


def form(browser, **kwargs):

    # fill the form
    for k, v in kwargs.items():
        input_field = browser.get_by_name(k)
        if not input_field:
            raise Exception('field `{0}` not found: {1} {2}'.format(
                k,
                browser.screenshot(),
                browser.dumphtml(),
            ))
        input_field.clear()
        input_field.send_keys(v)

    # submit
    browser.get_by_css('form button').submit()


@pytest.fixture(scope='session')
def settings(request):
    return request.config.option


@pytest.fixture
def url(settings):
    return partial('{0}://{1}{2}'.format, settings.scheme, settings.host)


@pytest.fixture
def path(settings):
    return partial(os.path.join, settings.data)


@pytest.fixture
def bro(browser, settings, url):

    browser.settings = settings

    browser.screenshot = partial(screenshot, browser)
    browser.dumphtml = partial(dumphtml, browser)

    browser.get_ajax = partial(get_ajax, browser, url)
    browser.set_value = partial(set_value, browser)

    browser.get_by_id = partial(get_by_id, browser)
    browser.get_by_css = partial(get_by_css, browser)
    browser.get_by_name = partial(get_by_name, browser)
    browser.get_by_xpath = partial(get_by_xpath, browser)

    browser.form = partial(form, browser)

    return browser


def pytest_addoption(parser):

    parser.addoption('--scheme', dest='scheme', default='http')
    parser.addoption('--host', dest='host',
                     default='www.github.com')
    parser.addoption('--data', dest='data', default='./data')
