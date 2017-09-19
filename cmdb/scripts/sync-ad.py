import sys
import ldap
from ldap.controls import SimplePagedResultsControl
from isms.settings import AD_URI, AD_USER, AD_PASS, AD_BASE
from cmdb.models import Person

PAGE_SIZE = 1000
SUB = ldap.SCOPE_SUBTREE


def process_person(dn, attrs):
    """Process a single result value"""
    person, c = Person.objects.get_or_create(userid=attrs['sAMAccountName'][0])
    person.path = dn[0]
    person.name = attrs['cn'][0]
    person.sid = attrs['objectSid']
    if 'title' in attrs:
        person.title = attrs['title']
    if 'employeenumber' in attrs:
        person.employee = attrs['employeenumber']
    if 'c' in attrs:
        person.countrycode = attrs['c'][0]
    if 'co' in attrs:
        person.country = attrs['co'][0]
    if 'l' in attrs:
        person.location = attrs['l']
    if 'department' in attrs:
        person.department = attrs['department'][0]
    if 'postalAddress' in attrs:
        person.address = attrs['postalAddress']
    if 'facsimileTelephoneNumber' in attrs:
        person.fax = attrs['facsimileTelephoneNumber']
    if 'mobile' in attrs:
        person.mobile = attrs['mobile']
    if 'telephoneNumber' in attrs:
        person.phone = attrs['telephoneNumber'][0]
    if 'mail' in attrs:
        person.mail = attrs['mail'][0]
    person.save()


def process_computer(dn, attrs):
    """Process a single result value"""
    pass


def set_cookie(lc_object, pctrls, pagesize):
    """Push lateset cookie back into the page control."""
    cookie = pctrls[0].cookie
    lc_object.cookie = cookie
    return cookie


ldap.set_option(ldap.OPT_REFERRALS, 0)
l = ldap.initialize(AD_URI)
l.protocol_version = 3

try:
    l.simple_bind_s(AD_USER, AD_PASS)
except ldap.LDAPError as error:
    exit('LDAP bind failed: {}'.format(error))

# create_controls
lc = SimplePagedResultsControl(True, PAGE_SIZE, '')

# Search person objects
cookie = True
while cookie:
    flt = '(objectCategory=person)'
    msgid = l.search_ext(AD_BASE, SUB, flt, serverctrls=[lc])
    rtype, rdata, rmsgid, serverctrls = l.result3(msgid)
    for dn, attrs in rdata:
        process_person(dn, attrs)
    pctrls = [c for c in serverctrls
              if c.controlType == SimplePagedResultsControl.controlType]
    cookie = set_cookie(lc, pctrls, PAGE_SIZE)

# # Search computer objects
# cookie = True
# while cookie:
#     flt = '(objectCategory=computer)'
#     msgid = l.search_ext(AD_BASE, SUB, flt, serverctrls=[lc])
#     rtype, rdata, rmsgid, serverctrls = l.result3(msgid)
#     for dn, attrs in rdata:
#         process_computer(dn, attrs)
#     pctrls = [c for c in serverctrls
#               if c.controlType == SimplePagedResultsControl.controlType]
#     cookie = set_cookie(lc, pctrls, PAGE_SIZE)

# Clean up and exit
l.unbind()
sys.exit(0)
