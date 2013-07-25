from distutils.core import setup
setup(name='json2line',
      description='Convert json to java.properties or tsv',
      long_description="""
      more convenience for cli tools such as grep , awk, ..""",
      url='https://github.com/nazoking/json2line',
      version='0.0.1',
      author='nazoking',
      author_email='nazoking@gmail.com',
      py_modules=[
          'json2line'
          ],
      scripts=[
          'scripts/json2line'
          ]
      )
