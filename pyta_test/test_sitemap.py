
def test_dummy(bro, url):

    bro.visit(url('/'))
    print bro.screenshot()

    bro.visit('http://www.github.com/')
    print bro.screenshot(name='github')
