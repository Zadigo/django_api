from selenium.webdriver import Chrome, Edge
from selenium.webdriver.common.keys import Keys


PATH = 'C:\\Users\\Pende\\Downloads\\edgedriver_win64'

def driver(path=None):
    """Returns a driver for selenium"""
    # chrome = Chrome(executable_path=None)
    edge = Edge(executable_path=PATH)
    return edge

s = driver()
s.get('https://example.com')

e = s.find_element_by_id('test')
e.send_keys(Keys.ENTER)
s.quit()