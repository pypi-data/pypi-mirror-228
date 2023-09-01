# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['preserve_podcasts', 'preserve_podcasts.utils']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.10,<7.0.0',
 'internetarchive>=3.5.0,<4.0.0',
 'pyrfc6266>=1.0.2,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'rich>=13.3.3,<14.0.0']

entry_points = \
{'console_scripts': ['podcastsPreserve = preserve_podcasts:main',
                     'podcastsUpload = preserve_podcasts.uploadPodcasts:main']}

setup_kwargs = {
    'name': 'preservethosepod',
    'version': '1.0.7',
    'description': 'Preserve those podcasts!',
    'long_description': '# preserve-those-podcasts\n\nPodcast archiving tool!\n\n## Why "preserve-those-podcasts"\n\nInspired by <http://preservethispodcast.org>\n\n## Requirements\n\n* Py>=3.8\n* requests\n* feedparser\n* rich\n* internetarchive\n* pyrfc6266\n\n* ffmpeg (`ffprobe`)\n\n## Installation\n\n```bash\npip install PreserveThosePod\n```\n\n## Usage\n\n### Quickstart\n\nTo archive a podcast, run:\n\n```bash\npodcastsPreserve --add <rss_feed_url> # download all episodes\npodcastsPreserve --update # download new episodes\npodcastsUpload # upload to archive.org\n```\n',
    'author': 'yzqzss',
    'author_email': 'yzqzss@yandex.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
