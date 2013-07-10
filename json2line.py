#!/usr/bin/python26
import json
import sys
import textwrap
from optparse import OptionParser, make_option

class Dumper:
  def as_dict(self, v, prefix=[]):
    for k in v.keys():
      for a in self.apply(v[k], self.append_key(k, prefix)):
        yield a

  def as_list(self, val, key=[]):
    for (i, v) in enumerate(val):
      for a,b in self.apply(v, self.append_key(i, key)):
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

  def format_list_key(self, key):
    return key

  def format_key(self, key):
    if isinstance(key, int):
      k=self.format_list_key(key)
      if k == None:
        return k
      else:
        return str(k)
    return key

  def format_keys(self, key):
    return self.sep.join([ks for ks in [self.format_key(k) for k in key] if not( ks == None )])

  def format_val(self, val):
    return json.dumps(val)

  def format(self, key, val):
    return self.format_keys(key) + self.eq + str(self.format_val(val))

class FormatterOption:
  def __init__(self, target):
    self.target=target

  def list(self):
    return [
      make_option("-s", "--sep", action="store", dest="sep", help="separator of key hierarchy. default '.'",default="."),
      make_option("-e", "--eq", action="store", dest="eq", help="separator of key and value. default '=' ",default="="),
      make_option("--tsv", action="store_true", dest="as_tsv", help="format as tsv. ex json{a:{b:1,c:2}} is \"a.b\\t1\\na.c\\t2\""),
      make_option("--listkey",dest="listkey", help="define callback lambda that format list key. lambda has argument name is 'key'. ex: --listkey \"'*'\""),
      make_option("-l", action="store_true", dest="listkey_erase", help="do not print list key. if option defined then json{a:[8,\"b\"]} is 'a=8\na=\"b\"'. This option is same as set listkey to 'None'") ,
      make_option("--format",dest="format",help="define callback lambda that format value. lambda has argument name is 'val'. default format is 'json.dumps(val)'. ex: --format \"'['+str(val)+']'\"") ]

  def apply(self, options):
    if options.as_tsv:
      options.eq = "\t"
      options.format = lambda val: val

    self.target.sep = options.sep
    self.target.eq = options.eq
    if options.listkey_erase:
      options.listkey = lambda key: None

    if options.listkey:
      if not(hasattr(options.listkey,'__call__')):
        lf = options.listkey
        options.listkey = lambda key: eval(lf)
      self.target.format_list_key = options.listkey

    if options.format:
      if not(hasattr(options.format,'__call__')):
        f = options.format
        options.format = lambda val: eval(f)
      self.target.format_val = options.format

USAGE=textwrap.dedent("""\
  Usage: %prog [options]
    change json to line separated text.
      {a:[8,"b"]} 
    is converted
      a.0=8
      a.1="b"
  
  Example:
    curl -s https://api.github.com/gists/public | %prog | grep "aaa.bbb" """)

def execute(data, options=None):
  dumper = Dumper()
  formatter = Formatter()
  formatter_option = FormatterOption(formatter)

  option_parser = OptionParser(usage=USAGE, option_list=formatter_option.list())

  (options, args) = option_parser.parse_args(options)
  formatter_option.apply(options)

  for k,v in dumper.apply(data):
    yield formatter.format(k,v)

def to_str(data, options=None):
  """
  >>> from json2line import to_str
  >>> print to_str({"hoge":"huge"})
  hoge="huge"
  >>> print to_str({"a":2})
  a=2
  >>> print to_str({"a":[2,1]}, ["-l"])
  a=2
  a=1
  >>> print to_str({"a":{"b":[2,"1"]}})
  a.b.0=2
  a.b.1="1"
  >>> print to_str({"a":{"b":[2,"1"]}}, ["-l"])
  a.b=2
  a.b="1"
  >>> print to_str({"a":{"b":[2,"1"]}}, ["-l","--format","val"])
  a.b=2
  a.b=1
  >>> print to_str({"a":{"b":[2,"1"]}}, ["-l","--format","'['+str(val)+']'"])
  a.b=[2]
  a.b=[1]
  >>> print to_str({"a":{"b":[2,"1"]}}, ["--listkey","'['+str(key)+']'"])
  a.b.[0]=2
  a.b.[1]="1"
  >>> print to_str({"a":{"b":[2,"1"]}}, ["--sep","-"])
  a-b-0=2
  a-b-1="1"
  >>> print to_str({"a":{"b":[2,"1"]}}, ["--eq","-"])
  a.b.0-2
  a.b.1-"1"
  """
  return "\n".join([i for i in execute(data,options)])

if __name__ == '__main__':
  import select
  rlist, wlist, xlist = select.select([sys.stdin],[],[],0)
  if not rlist:
    data = None
    options = ["--help"]
  else:
    data = json.load(sys.stdin)
    options = None

  for l in execute(data,options):
    print l

