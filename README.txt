Usage: json2line.py [options]
  change json to line separated text.
    {a:[8,"b"]} 
  is converted
    a.0=8
    a.1="b"

Example:
  curl -s https://api.github.com/gists/public | json2line.py | grep "aaa.bbb" 

Options:
  -s SEP, --sep=SEP  separator of key hierarchy. default '.'
  -e EQ, --eq=EQ     separator of key and value. default '='
  --tsv              format as tsv. ex json{a:{b:1,c:2}} is "a.b\t1\na.c\t2"
  --listkey=LISTKEY  define callback lambda that format list key. lambda has
                     argument name is 'key'. ex: --listkey "'*'"
  -l                 do not print list key. if option defined then
                     json{a:[8,"b"]} is 'a=8 a="b"'. This option is same as
                     set listkey to 'None'
  --format=FORMAT    define callback lambda that format value. lambda has
                     argument name is 'val'. default format is
                     'json.dumps(val)'. ex: --format "'['+str(val)+']'"
  -h, --help         show this help message and exit
