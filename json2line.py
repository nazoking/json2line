import json
import sys
from optparse import OptionParser, make_option

class Json2Line:
  class Dumper:
    def __init__(self, list_is_map=True):
      self.list_is_map = list_is_map

    def as_dict(self, v, prefix=[]):
      for k in v.keys():
        for a in self.apply(v[k], self.append_key(k, prefix)):
          yield a

    def as_list(self, val, key=[]):
      if self.list_is_map:
        for (i, v) in enumerate(val):
          for a,b in self.apply(v, self.append_key(str(i), key)):
            yield a,b
      else:
        for (i, v) in enumerate(val):
          for a,b in self.apply(v, key):
            yield a,b

    def append_key(self, key, prefix=[]):
      return prefix + [ key ]

    def as_value(self, key, vaule):
      yield key, value

    def apply(self, v, prefix=[]):
      if isinstance(v, dict):
        for a in self.as_dict(v, prefix):
          yield a
      elif isinstance(v, list):
        for a in self.as_list(v, prefix):
          yield a
      else:
        yield prefix,v

  class Formatter:
    def __init__(self, sep='.', eq='='):
      self.sep = sep
      self.eq = eq
    def format_key(self, key):
      return self.sep.join(key)
  
    def format_val(self, val):
      return json.dumps(val)
  
    def format(self, key, val):
      return self.format_key(key) + self.eq + self.format_val(val)

  class Option:
    def __init__(self, target):
      self.target=target
  
  class DumperOption(Option):
    def list(self):
      return [
        make_option("-l", action="store_true", dest="list_is_map", help="list is map. if true then json{a:[8,9]} is 'a.0=8\na.1=9', else 'a=8\na=9'. default false",default="\n") ]

    def apply(self, options):
      self.target.list_is_map = options.list_is_map

  class FormatterOption(Option):

    def list(self):
      return [
        make_option("-s", "--sep", action="store", dest="sep", help="separator of key hierarchy. default '.'",default="."),
        make_option("-e", "--eq", action="store", dest="eq", help="separator of key and value. default '=' ",default="="),
        make_option("--br", action="store", dest="br", help="separator of records. default \"\\n\"",default="\n"),
        make_option("--tsv", action="store_true", dest="as_tsv", help="format as tsv. ex json{a:{b:1,c:2}} is \"a.b\\t1\\na.c\\t2\""),
        make_option("--format",dest="format",help="define callback function of value format argument name is val. ex: --format \"'['+val+']'") ]

    def apply(self, options):
      if options.as_tsv:
        self.target.eq = "\t"
        def format_val(val):
          return val
        self.target.format_val = format_val

      self.target.sep = options.sep
      self.target.eq = options.eq
      self.target.br = options.br
      if options.format:
        def format_val(val):
          return eval(options.format)
        self.target.format_val = format_val

  @classmethod
  def execute(cls):
    dumper = cls.Dumper()
    formatter = cls.Formatter()
    formatter_option = cls.FormatterOption(formatter)
    dumper_option = cls.DumperOption(dumper)

    option_parser = OptionParser(option_list=formatter_option.list() + dumper_option.list())

    (options, args) = option_parser.parse_args()
    formatter_option.apply(options)
    dumper_option.apply(options)
    
    for k,v in dumper.apply(json.load(sys.stdin)):
      print formatter.format(k,v)

if __name__ == '__main__':
  Json2Line.execute()

