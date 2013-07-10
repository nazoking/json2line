import json
import sys
from optparse import OptionParser

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

def option_parser():
  parser = OptionParser()
  parser.add_option("-s", "--sep", action="store", dest="sep", help="separator of key hierarchy. default '.'",default=".")
  parser.add_option("-e", "--eq", action="store", dest="eq", help="separator of key and value. default '=' ",default="=")
  parser.add_option("--br", action="store", dest="br", help="separator of records. default \"\\n\"",default="\n")
  parser.add_option("-l", action="store_true", dest="list_is_map", help="list is map. if true then json{a:[8,9]} is 'a.0=8\na.1=9', else 'a=8\na=9'. default false",default="\n")
  parser.add_option("--tsv", action="store_true", dest="as_tsv", help="format as tsv. ex json{a:{b:1,c:2}} is \"a.b\\t1\\na.c\\t2\"")
  parser.add_option("--format",dest="format",help="define callback function of value format argument name is val. ex: --format \"'['+val+']'")
  return parser

def options_apply(dumper,formatter,options):
  if options.as_tsv:
    formatter.eq = "\t"
    def format_val(val):
      return val
    formatter.format_val = format_val

  formatter.sep = options.sep
  formatter.eq = options.eq
  formatter.br = options.br
  dumper.list_is_map = options.list_is_map
  if options.format:
    def format_val(val):
      return eval(options.format)
    formatter.format_val = format_val
  
dumper = Json2Line.Dumper()
formatter = Json2Line.Formatter()
(options, args) = option_parser().parse_args()
options_apply(dumper,formatter,options)

for k,v in dumper.apply(json.load(sys.stdin)):
  print formatter.format(k,v)

