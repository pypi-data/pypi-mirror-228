from distutils.core import setup
setup(
  name = 'llmmodelsapi',
  packages = ['llmmodelsapi'],
  version = '0.3',
  license='MIT',
  description = 'SDK for interfacing with core models hosted by LLM Solutions',
  long_description_content_type="text/markdown",
  author = 'Matthieu Moullec',
  author_email = 'matthieu.moullec.perso@gmail.com',
  url = 'https://github.com/llm-solutions/LLM-API-Express-SDK-Python',
  download_url = 'https://github.com/llm-solutions/LLM-API-Express-SDK-Python/archive/refs/tags/v0.2.tar.gz',
  keywords = ['Large Language Model', 'LLM', 'API'],
  install_requires=[
          'requests',
          'json',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)