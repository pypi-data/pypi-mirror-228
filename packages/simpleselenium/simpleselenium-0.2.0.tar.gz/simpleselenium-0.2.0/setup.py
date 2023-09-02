# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpleselenium']

package_data = \
{'': ['*']}

install_requires = \
['PyAutoGUI>=0.9.54,<0.10.0',
 'PyYAML>=6.0.1,<7.0.0',
 'django-environ>=0.11.1,<0.12.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'selenium>=4.12.0,<5.0.0']

setup_kwargs = {
    'name': 'simpleselenium',
    'version': '0.2.0',
    'description': 'Python package to easily work with Selenium.',
    'long_description': '### Simple Selenium\n\nSelenium with Tab Management\n\n<small> With all the already available flexibility and features of Selenium </small>\n\n### Installation\n\nInstall from PyPI\n\n```bash\npip install simpleselenium\n```\n\n### Core Idea\n\nA `browser` has many `tabs`.\n\nAction/activity on `Tab` object\n- Check if the tab is alive (i.e. it has not been closed)\n- Switch to a tab\n- See/obtain page source, title and headings\n- work on a specific tab (click elements, scroll and so on.)\n- ... many more\n\nAction/activity on `Browser` object\n- Open a new tab with url\n- Get a list of open tabs\n- Get active tab\n- Switch to a tab of the browser (first, last or any one).\n- close a tab\n- Close the browser\n\n### Working with driver objects\n\n`driver` object available on any `Tab` object.\n\n### Features\n\nSome basic features are being listed below (also see the `Usage` section below):\n\n- easy management of different tabs\n- switching to a tab is super easy\n- know if a tab is active (current tab) or alive\n- closing a tab is easy as `browser.close_tab(tab_object)`\n- Several (built-in) functions\n    - `tab.infinite_scroll()`\n    - `tab.scroll()`\n    - `tab.scroll_to_bottom()`\n    - `tab.click(element_on_page)`\n    - `tab.switch()` to focus on tab i.e. make it the active tab\n- Can\'t find a way to use usual selenium methods? Use `tab.driver` object to access the browser/driver object and use\n  accordingly\n\n### Usage\n\nThe best way to getting started with the package is to use the `Browser` object to start a browser and call `open`\nmethod off it which returns a Tab object.\n\n#### Browser\n\n```python\n\nfrom simpleselenium import Browser, Tab\n\n# name is one of "Chrome" or "FireFox"\n# driver path is not required in most cases\n\nwith Browser(name="Chrome", driver_path=None, implicit_wait=10) as browser:\n        google: Tab = browser.open("https://google.com") # a `Tab` object\n        yahoo = browser.open("https://yahoo.com")\n        bing = browser.open("https://bing.com")\n        duck_duck = browser.open("https://duckduckgo.com/")\n\n        yahoo.scroll_up(times=5)\n        yahoo.scroll_down(times=10)\n\n        print(browser.tabs)\n        print(browser.current_tab)\n        print(browser.first_tab)\n        print(browser.last_tab)\n\n        print(browser.last_tab.switch())\n\n        print(google.page_source)\n        print(google.title)\n        print(google.url)\n        print(google.is_active)\n        print(google.is_alive)\n\n        browser.close_tab(bing)\n        print(browser.tabs)\n\n        print(browser.current_tab)\n\n        yahoo.switch()\n        print(browser.current_tab)\n        google.switch()\n\n        print(browser.current_tab)\n\n        browser.close_tab(yahoo)\n\n        print(yahoo.is_alive)\n        print(yahoo.is_active)\n\n        print(google.driver.title, google.title)\n        print(google.driver.title == google.title)\n```\n\n### TODO\n\n- Complete documentation\n',
    'author': 'Vishal Kumar Mishra',
    'author_email': 'vishal.k.mishra2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TheConfused/simpleselenium',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
