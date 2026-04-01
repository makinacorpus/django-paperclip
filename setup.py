import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
    'coverage',
]

setup(
    name='paperclip',
    version='2.7.4',
    author='Makina Corpus',
    author_email='geobi@makina-corpus.com',
    url='https://github.com/makinacorpus/django-paperclip',
    download_url="https://pypi.python.org/pypi/paperclip/",
    description="Attach files to Django models",
    long_description=open(os.path.join(here, 'README.rst')).read() + '\n\n' +
                     open(os.path.join(here, 'CHANGES')).read(),
    license='LPGL, see LICENSE file.',
    python_requires='>=3.10',
    install_requires=[
        'Django',
        'pillow',
        'easy-thumbnails',
        'django-embed-video',
        'python-magic'
    ],
    tests_require=tests_require,
    extras_require={
        'dev': tests_require + [
            'flake8',
        ]
    },
    packages=find_packages(include=('paperclip', )),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Topic :: Utilities',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',

    ]
)
