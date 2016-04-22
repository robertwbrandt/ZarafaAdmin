#!/usr/bin/env python
"""
Python wrapper for analyzing at zarafa logs
"""
import argparse, textwrap, fnmatch, datetime
import xml.etree.cElementTree as ElementTree
import subprocess
from multiprocessing import Process, Queue

# Import Brandt Common Utilities
import sys, os
sys.path.append( os.path.realpath( os.path.join( os.path.dirname(__file__), "/opt/brandt/common" ) ) )
import brandt
sys.path.pop()

args = {}
args['output'] = 'text'
args['log'] = 'system'
args['filter'] = ''

version = 0.3
encoding = 'utf-8'

# Logs have roughly 135 (89-165) Bytes per line.
logSizeLimit = 20000 * 135
logDefaults = {'system':{"logfile":"/var/log/syslog","oldlogfile":"/var/log/syslog.1"},
               'zarafa':{"logfile":"/var/log/zarafa/server.log","oldlogfile":"/var/log/zarafa/server.log.1"},
               'mysql':{"logfile":"/var/log/mysql/mysql.log","oldlogfile":"/var/log/mysql/mysql.log.1"},
               'mysql-error':{"logfile":"/var/log/mysql/error.log","oldlogfile":"/var/log/mysql/error.log.1"},
               'z-push':{"logfile":"/var/log/z-push/z-push.log","oldlogfile":"/var/log/z-push/z-push.log.1"},
               'z-push-error':{"logfile":"/var/log/z-push/z-push-error.log","oldlogfile":"/var/log/z-push/z-push-error.log.1"}}

class customUsageVersion(argparse.Action):
  def __init__(self, option_strings, dest, **kwargs):
    self.__version = str(kwargs.get('version', ''))
    self.__prog = str(kwargs.get('prog', os.path.basename(__file__)))
    self.__row = min(int(kwargs.get('max', 80)), brandt.getTerminalSize()[0])
    self.__exit = int(kwargs.get('exit', 0))
    super(customUsageVersion, self).__init__(option_strings, dest, nargs=0)
  def __call__(self, parser, namespace, values, option_string=None):
    # print('%r %r %r' % (namespace, values, option_string))
    if self.__version:
      print self.__prog + " " + self.__version
      print "Copyright (C) 2013 Free Software Foundation, Inc."
      print "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>."
      version  = "This program is free software: you can redistribute it and/or modify "
      version += "it under the terms of the GNU General Public License as published by "
      version += "the Free Software Foundation, either version 3 of the License, or "
      version += "(at your option) any later version."
      print textwrap.fill(version, self.__row)
      version  = "This program is distributed in the hope that it will be useful, "
      version += "but WITHOUT ANY WARRANTY; without even the implied warranty of "
      version += "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the "
      version += "GNU General Public License for more details."
      print textwrap.fill(version, self.__row)
      print "\nWritten by Bob Brandt <projects@brandt.ie>."
    else:
      print "Usage: " + self.__prog + " [options] [filter]"
      print "Script used to find details about Zarafa groups.\n"
      print "Options:"
      options = []
      options.append(("-h, --help",              "Show this help message and exit"))
      options.append(("-v, --version",           "Show program's version number and exit"))
      options.append(("-o, --output OUTPUT",     "Type of output {text | xml}"))
      options.append(("-l, --log LOG",           "Log to analyse {" + " | ".join(sorted(logDefaults.keys())) + "}"))
      options.append(("filter",                  "Filter to apply to log."))
      length = max( [ len(option[0]) for option in options ] )
      for option in options:
        description = textwrap.wrap(option[1], (self.__row - length - 5))
        print "  " + option[0].ljust(length) + "   " + description[0]
      for n in range(1,len(description)): print " " * (length + 5) + description[n]
    exit(self.__exit)
def command_line_args():
  global args, version
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument('-v', '--version', action=customUsageVersion, version=version, max=80)
  parser.add_argument('-h', '--help', action=customUsageVersion)
  parser.add_argument('-o', '--output',
          required=False,
          default=args['output'],
          choices=['text', 'xml'],
          help="Display output type.")
  parser.add_argument('-l', '--log',
          required=False,
          default=args['log'],
          choices=sorted(logDefaults.keys()),
          help="Log to analyse.")
  parser.add_argument('filter',
          nargs='?',
          default= args['filter'],
          action='store',
          help="Filter to apply to log.")
  args.update(vars(parser.parse_args()))

def get_data():
  global args

  size = os.stat(logDefaults[args['log']][logfile]).st_size
  print logDefaults[args['log']][logfile], size

  data = []
  if size < logSizeLimit:
    if os.path.isfile(logDefaults[args['log']][oldlogfile])
    f = open(logDefaults[args['log']][oldlogfile], 'r')
    data = f.read().split('\n')
    f.close()

  f = open(logDefaults[args['log']][logfile], 'r')
  data += f.read().split('\n')
  f.close()

  return data

def zarafa_groups(groups):
  global args

  if args['output'] == 'text':
    print "Zarafa Groups (" + str(len(groups)) + ")"
    print "-" * max([len(x) for x in groups] + [13])
    print "\n".join( groups )
  elif args['output'] == 'csv':
    print "Zarafa Groups"
    print "\n".join( groups )
  else:
    xml = ElementTree.Element('groups')
    for group in groups:
      xmluser = ElementTree.SubElement(xml, "group", groupname = group)
    return xml


# Start program
if __name__ == "__main__":
    command_line_args()

    exitcode = 0
  # try:
    logdata = get_data()
    print logdata




    # if len(groups) == 1:
    #   xmldata = zarafa_group(groups[0])
    # else:
    #   xmldata = zarafa_groups(groups)

    # if args['output'] == 'xml': 
    #   xml = ElementTree.Element('zarafaadmin')
    #   xml.append(xmldata)
    #   print '<?xml version="1.0" encoding="' + encoding + '"?>\n' + ElementTree.tostring(xml, encoding=encoding, method="xml")

  # except ( Exception, SystemExit ) as err:
  #   try:
  #     exitcode = int(err[0])
  #     errmsg = str(" ".join(err[1:]))
  #   except:
  #     exitcode = -1
  #     errmsg = str(" ".join(err))

  #   if args['output'] != 'xml': 
  #     if exitcode != 0: sys.stderr.write( str(err) +'\n' )
  #   else:
  #     xml = ElementTree.Element('zarafaadmin')      
  #     xmldata = ElementTree.SubElement(xml, 'error', errorcode = str(exitcode) )
  #     xmldata.text = errmsg
  #     print '<?xml version="1.0" encoding="' + encoding + '"?>\n' + ElementTree.tostring(xml, encoding=encoding, method="xml")

  # sys.exit(exitcode)