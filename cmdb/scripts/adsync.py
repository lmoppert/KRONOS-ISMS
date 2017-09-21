import sys
import ldap
from binascii import hexlify
from ldap.controls import SimplePagedResultsControl
from isms.settings import AD_URI, AD_USER, AD_PASS, AD_BASE
from cmdb.models import ComputerCategory, Person, Software, Workstation

PAGE_SIZE = 1000
SUB = ldap.SCOPE_SUBTREE


def decode_SID(raw):
    revision = int(ord(raw[0]))
    sub_auth_count = int(ord(raw[1]))
    ident_auth = int(hexlify(raw[2:8]), 16)
    if ident_auth >= 4294967296:
        ident_auth = hex(ident_auth)
    sub_auth = ''
    i = 0
    while i < sub_auth_count:
        sub_auth += '-' + str(int(hexlify(raw[11+(i*4):7+(i*4):-1]), 16))
        i += 1
    return 'S-' + str(revision) + '-' + str(ident_auth) + sub_auth


def process_person(dn, attrs):
    """Process a single result value"""
    person, c = Person.objects.get_or_create(userid=attrs['sAMAccountName'][0])
    person.path = attrs['distinguishedName'][0]
    person.name = attrs['cn'][0]
    person.sid = decode_SID(attrs['objectSid'][0])
    if 'title' in attrs:
        person.title = attrs['title'][0]
    if 'employeeNumber' in attrs:
        person.employee = attrs['employeeNumber'][0]
    if 'c' in attrs:
        person.countrycode = attrs['c'][0]
    if 'co' in attrs:
        person.country = attrs['co'][0]
    if 'l' in attrs:
        person.location = attrs['l'][0]
    if 'department' in attrs:
        person.department = attrs['department'][0]
    if 'postalCode' in attrs:
        person.zipcode = attrs['postalCode'][0]
    if 'streetAddress' in attrs:
        person.address = attrs['streetAddress'][0]
    if 'facsimileTelephoneNumber' in attrs:
        person.fax = attrs['facsimileTelephoneNumber'][0]
    if 'mobile' in attrs:
        person.mobile = attrs['mobile'][0]
    if 'telephoneNumber' in attrs:
        person.phone = attrs['telephoneNumber'][0]
    if 'mail' in attrs:
        person.mail = attrs['mail'][0]
    flags = int(attrs['userAccountControl'][0])
    person.active = not(flags & 0b10)
    person.unlocked = not(flags & 0b10000)
    person.pwex = not(flags & 0b10000000000000000)
    person.pwsv = not(flags & 0b100000000000000000000000)
    person.save()


def process_computer(dn, attrs):
    """Process a single result value"""
    name = attrs['name'][0]
    comp, c = Workstation.objects.get_or_create(name=name)
    comp.path = attrs['distinguishedName'][0]
    comp.sid = decode_SID(attrs['objectSid'][0])
    if 'dNSHostName' in attrs:
        comp.dnsname = attrs['dNSHostName'][0]
    if 'description' in attrs:
        comp.description = attrs['description'][0]
    if 'operatingSystem' in attrs:
        comp.os = attrs['operatingSystem'][0]
    if 'operatingSystemVersion' in attrs:
        comp.os_ver = attrs['operatingSystemVersion'][0]
    if 'operatingSystemServicePack' in attrs:
        comp.os_sp = attrs['operatingSystemServicePack'][0]
    parts = name.split("-")
    if len(name) == 15 and len(parts) == 4:
        comp.category, c = ComputerCategory.objects.get_or_create(token=parts[2])
    elif len(name) == 11 and len(parts) == 3:
        comp.category, c = ComputerCategory.objects.get_or_create(token=parts[1])
    comp.save()


def process_group(dn, attrs):
    """Process a single result value"""
    name = attrs['name'][0]
    if 'description' in attrs:
        description = attrs['description'][0]
    else:
        description = ''
    if name[0:3] == "SW-":
        sw, c = Software.objects.get_or_create(name=name)
        sw.description = description
        if 'member' in attrs:
            for member in attrs['member']:
                try:
                    ws = Workstation.objects.get(path=member)
                    sw.workstations.add(ws)
                except:
                    pass
        sw.save()


def set_cookie(lc_object, pctrls, pagesize):
    """Push lateset cookie back into the page control."""
    cookie = pctrls[0].cookie
    lc_object.cookie = cookie
    return cookie


def search_objects(ldap, ldapcontrol, filterstring, callback):
    print "Searching for {}".format(filterstring)
    cookie = True
    while cookie:
        print "Fetcing results"
        msgid = ldap.search_ext(AD_BASE, SUB, filterstring,
                                serverctrls=[ldapcontrol])
        rtype, rdata, rmsgid, serverctrls = ldap.result3(msgid)
        for dn, attrs in rdata:
            callback(dn, attrs)
        pctrls = [c for c in serverctrls
                if c.controlType == SimplePagedResultsControl.controlType]
        cookie = set_cookie(lc, pctrls, PAGE_SIZE)
    print "Finished searching for {}".format(filterstring)


def init():
    ldap.set_option(ldap.OPT_REFERRALS, 0)
    l = ldap.initialize(AD_URI)
    l.protocol_version = 3
    try:
        l.simple_bind_s(AD_USER, AD_PASS)
    except ldap.LDAPError as error:
        exit('LDAP bind failed: {}'.format(error))
    lc = SimplePagedResultsControl(True, PAGE_SIZE, '')
    return l, lc


# Main processing
l, lc = init()
search_objects(l, lc, '(objectCategory=person)', process_person)
search_objects(l, lc, '(objectCategory=computer)', process_computer)
search_objects(l, lc, '(objectCategory=group)', process_group)
l.unbind()
sys.exit(0)
