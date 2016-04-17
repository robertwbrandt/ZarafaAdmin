#!/usr/bin/env python
"""
Python wrapper for zarafa-admin --type group --details group
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
args['cache'] = 15
args['output'] = 'text'
args['group'] = ''
args['delimiter'] = ""

version = 0.3
encoding = 'utf-8'


ldapmapping = (("pr_ec_enabled_features","0x67b3101e"),("pr_ec_disabled_features","0x67b4101e"),
               ("pr_ec_archive_servers","0x67c4101e"),("pr_ec_archive_couplings","0x67c5101e"),
               ("pr_ec_exchange_dn","0x678001e"),("pr_business_telephone_number","0x3a08001e"),
               ("pr_business2_telephone_number","0x3a1b101e"),("pr_business_fax_number","0x3a24001e"),
               ("pr_mobile_telephone_number","0x3a1c001e"),("pr_home_telephone_number","0x3a09001e"),
               ("pr_home2_telephone_number","0x3a2f101e"),("pr_primary_fax_number","0x3a23001e"),
               ("pr_pager_telephone_number","0x3a21001e"),("pr_comment","0x3004001e"),
               ("pr_department_name","0x3a18001e"),("pr_office_location","0x3a19001e"),
               ("pr_given_name","0x3a06001e"),("pr_surname","0x3a11001e"),
               ("pr_childrens_names","0x3a58101e"),("pr_business_ddress_city","0x3a27001e"),
               ("pr_title","0x3a17001e"),("pr_user_certificate","0x3a220102"),("pr_initials","0x3a0a001e"),
               ("pr_language","0x3a0c001e"),("pr_organizational_id_number","0x3a10001e"),
               ("pr_postal_address","0x3a15001e"),("pr_company_name","0x3a16001e"),
               ("pr_country","0x3a26001e"),("pr_state_or_province","0x3a28001e"),("pr_street_address","0x3a29001e"),
               ("pr_postal_code","0x3a2a001e"),("pr_post_office_box","0x3a2b001e"),
               ("pr_assistant","0x3a30001e"),("pr_ems_ab_www_home_page","0x8175101e"),
               ("pr_business_home_page","0x3a51001e"),("pr_ems_ab_is_member_of_dl","0x80081102"),
               ("pr_ems_ab_reports","0x800e1102"),("pr_manager_name","0x8005001e"),("pr_ems_ab_owner","0x800c001e"))

fieldmappings = (("username","Username"),("fullname","Fullname"),("emailaddress","Email Address"),
                 ("active","Active"),("administrator","Administrator"),("addressbook","Address Book"),
                 ("autoacceptmeetingreq","Auto-Accept Meeting Req"),("lastlogon","Last Logon"),("lastlogoff","Last Logoff"))

ldapfieldmappings = (("pr_given_name","Given Name"),("pr_initials","Initials"),("pr_surname","Surname"),
                     ("pr_company_name","Company Name"),("pr_title","Title"),("pr_department_name","Department Name"),
                     ("pr_office_location","Office Location"),("pr_business_telephone_number","Business Telephone Number"),
                     ("pr_business2_telephone_number","Business 2 Telephone Number"),("pr_home_telephone_number","Home Telephone Number"),
                     ("pr_home2_telephone_number","Home 2 Telephone Number"),("pr_pager_telephone_number","Pager Telephone Number"),
                     ("pr_primary_fax_number","Primary Fax Number"),("pr_business_fax_number","Business Fax Number"),
                     ("pr_country","Country"),("pr_state_or_province","State or Province"),
                     ("pr_ems_ab_is_member_of_dl","Distribution Lists"),("pr_ec_enabled_features","Enabled Features"),
                     ("pr_ec_disabled_features","Disabled Features"),("pr_assistant","Assistant"),
                     ("pr_business_address_city","Business Address City"),("pr_business_home_page","Business Homepage"),
                     ("pr_childrens_names","Children's Names"),("pr_comment","Comment"),("pr_ec_exchange_dn","Exchange DN"),
                     ("pr_ems_ab_owner","Distribution List Owner"),("pr_ems_ab_reports","Reports"),
                     ("pr_ems_ab_www_home_page","Homepage"),("pr_language","Language"),
                     ("pr_manager_name","Manager"),("pr_mobile_telephone_number","Mobile Telephone Number"),
                     ("pr_organizational_id_number","Organizational ID Number"),("pr_post_office_box","Post Office Box"),
                     ("pr_postal_address","Postal Address"),("pr_postal_code","Postal Code"),
                     ("pr_street_address","Street Address"),("pr_user_certificate","User Certificate"))

quotafieldmappings = (("quotaoverrides"," Quota overrides"),("warninglevel"," Warning level (MB)"),
                      ("softlevel"," Soft level (MB)"),("hardlevel"," Hard level (MB)"),
                      ("currentstoresize","Current store size (MB)"))

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
      print "Usage: " + self.__prog + " [options] [groupname]"
      print "Script used to find details about Zarafa groups.\n"
      print "Options:"
      options = []
      options.append(("-h, --help",              "Show this help message and exit"))
      options.append(("-v, --version",           "Show program's version number and exit"))
      options.append(("-o, --output OUTPUT",     "Type of output {text | csv | xml}"))
      options.append(("-c, --cache MINUTES",     "Cache time. (in minutes)"))
      options.append(("-d, --delimiter DELIM",   "Character to use instead of TAB for field delimiter"))
      options.append(("groupname",               "Filter to apply to groupnames."))
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
  parser.add_argument('-c', '--cache',
          required=False,
          default=args['cache'],
          type=int,
          help="Cache time. (in minutes)")
  parser.add_argument('-d', '--delimiter',
          required=False,
          default=args['delimiter'],
          type=str,
          help="Character to use instead of TAB for field delimiter")
  parser.add_argument('-o', '--output',
          required=False,
          default=args['output'],
          choices=['text', 'csv', 'xml'],
          help="Display output type.")
  parser.add_argument('group',
          nargs='?',
          default= args['group'],
          action='store',
          help="Group to retrieve details about.")
  args.update(vars(parser.parse_args()))
  if args['delimiter']: args['delimiter'] = args['delimiter'][0]
  if not args['delimiter'] and args['output'] == "csv": args['delimiter'] = ","

def get_data():
  global args
  command = '/usr/sbin/zarafa-admin -L'
  cachefile = '/tmp/zarafa-groups.cache'    

  args['cache'] *= 60
  age = args['cache'] + 1
  try:
    age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.stat(cachefile).st_mtime)).seconds
  except:
    pass

  if age > args['cache']:
    p = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err: raise IOError(err)

    out = out.strip().split('\n')[3:]
    for c in reversed(range(len(out))):
      if out[c]:
        out[c] = out[c].strip()
        if out[c] != "Everyone": continue
      out.pop(c)
    out = sorted(out, key=lambda s: s.lower())

    f = open(cachefile, 'w')
    f.write("\n".join(out))
    f.close()
  else:
    f = open(cachefile, 'r')
    out = f.read().split('\n')
    f.close()

  # Apply groupname filter
  for c in reversed(range(len(out))):
    if out[c]:
      if args['group']:
        if not fnmatch.fnmatch(out[c].lower(), args['group'].lower()): continue
    out.pop(c)

  return out


def zarafa_groups(groups):
  global args

  if args['output'] != 'xml':
    print "Zarafa Groups"
    if args['output'] == 'text': print "-" * 25
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
    groups = get_data()
    if len(groups) == 1:
      xmldata = zarafa_group(groups[0])
    else:
      xmldata = zarafa_groups(groups)

    if args['output'] == 'xml': 
      xml = ElementTree.Element('zarafaadmin')
      xml.append(xmldata)
      print '<?xml version="1.0" encoding="' + encoding + '"?>\n' + ElementTree.tostring(xml, encoding=encoding, method="xml")

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