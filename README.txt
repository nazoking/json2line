Usage: json2line.py [options]

Options:
  -s SEP, --sep=SEP  separator of key hierarchy. default '.'
  -e EQ, --eq=EQ     separator of key and value. default '='
  --br=BR            separator of records. default "\n"
  --tsv              format as tsv. ex json{a:{b:1,c:2}} is "a.b\t1\na.c\t2"
  --format=FORMAT    define callback function of value format argument name is
                     val. ex: --format "'['+val+']'
  -l                 list is map. if true then json{a:[8,9]} is 'a.0=8 a.1=9',
                     else 'a=8 a=9'. default false
  -h, --help         show this help message and exit
