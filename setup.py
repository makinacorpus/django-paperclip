import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


setup(
    name='paperclip',
    version='2.1.0',
    author='Makina Corpus',
    author_email='geobi@makina-corpus.com',
    url='https://github.com/makinacorpus/paperclip',
    download_url="http://pypi.python.org/pypi/paperclip/",
    description="Attach files to Django models",
    long_description=open(os.path.join(here, 'README.rst')).read() + '\n\n' +
                     open(os.path.join(here, 'CHANGES')).read(),
    license='LPGL, see LICENSE file.',
    install_requires=[
        'Django',
        'easy-thumbnails',
        'django-embed-video',
    ],
    packages=find_packages(include=('paperclip', )),
    include_package_data=True,
    zip_safe=False,
    classifiers=['Topic :: Utilities',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Development Status :: 5 - Production/Stable',
                 'Programming Language :: Python :: 2.7'],
)
