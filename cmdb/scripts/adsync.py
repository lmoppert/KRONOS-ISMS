import sys
import ldap
from binascii import hexlify
from ldap.controls import SimplePagedResultsControl
from isms.settings import AD_URI, AD_USER, AD_PASS, AD_BASE
from cmdb.models import (ComputerCategory, Person, Software, Workstation,
                         Location, Country)

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


def process_office(attrs):
    """Search for an office, create it if nothing is found and return the
    coresponding object."""
    loc, c = Location.objects.get_or_create(
        token=attrs['physicalDeliveryOfficeName'][0])
    if 'l' in attrs and not loc.name:
        loc.name = attrs['l'][0]
    if 'postalCode' in attrs and not loc.zipcode:
        loc.zipcode = attrs['postalCode'][0]
    if 'streetAddress' in attrs and not loc.address:
        loc.address = attrs['streetAddress'][0]
    if 'c' in attrs and not loc.country:
        co, c = Country.objects.get_or_create(token=attrs['c'][0])
        if 'co' in attrs and c:
            co.name = attrs['co'][0]
            co.save()
        loc.country = co
    loc.save()
    return loc


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
    if 'physicalDeliveryOfficeName' in attrs:
        person.office = process_office(attrs)
    if 'department' in attrs:
        person.department = attrs['department'][0]
    if 'facsimileTelephoneNumber' in attrs:
        person.fax = attrs['facsimileTelephoneNumber'][0]
    if 'mobile' in attrs:
        person.mobile = attrs['mobile'][0]
    if 'telephoneNumber' in attrs:
        person.phone = attrs['telephoneNumber'][0]
    if 'mail' in attrs:
        person.mail = attrs['mail'][0]
    # Replace by ForeignKey
    if 'c' in attrs and 'co' in attrs:
        person.countrycode = attrs['c'][0]
        person.country = attrs['co'][0]
    # Examine User Account Control Flags and set coresponding values
    flags = int(attrs['userAccountControl'][0])
    person.active = not(flags & 0b10)
    person.unlocked = not(flags & 0b10000)
    person.pwex = not(flags & 0b10000000000000000)
    person.pwsv = not(flags & 0b100000000000000000000000)
    person.save()


def process_computer(dn, attrs):
    """Process a single result value"""
    name = attrs['name'][0]
    cp, c = Workstation.objects.get_or_create(name=name)
    cp.path = attrs['distinguishedName'][0]
    cp.sid = decode_SID(attrs['objectSid'][0])
    if 'dNSHostName' in attrs:
        cp.dnsname = attrs['dNSHostName'][0]
    if 'description' in attrs:
        cp.description = attrs['description'][0]
    if 'operatingSystem' in attrs:
        cp.os = attrs['operatingSystem'][0]
    if 'operatingSystemVersion' in attrs:
        cp.os_ver = attrs['operatingSystemVersion'][0]
    if 'operatingSystemServicePack' in attrs:
        cp.os_sp = attrs['operatingSystemServicePack'][0]
    parts = name.split("-")
    if len(name) == 15 and len(parts) == 4:
        cp.category, c = ComputerCategory.objects.get_or_create(token=parts[2])
        cp.location, c = Location.objects.get_or_create(token=parts[1])
    elif len(name) == 11 and len(parts) == 3:
        cp.category, c = ComputerCategory.objects.get_or_create(token=parts[1])
        cp.location, c = Location.objects.get_or_create(token=parts[0])
    cp.save()


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
    print("Searching for {}".format(filterstring))
    cookie = True
    while cookie:
        print("Fetcing results")
        msgid = ldap.search_ext(AD_BASE, SUB, filterstring,
                                serverctrls=[ldapcontrol])
        rtype, rdata, rmsgid, serverctrls = ldap.result3(msgid)
        for dn, attrs in rdata:
            callback(dn, attrs)
        pctrls = [c for c in serverctrls
                  if c.controlType == SimplePagedResultsControl.controlType]
        cookie = set_cookie(lc, pctrls, PAGE_SIZE)
    print("Finished searching for {}".format(filterstring))


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
# search_objects(l, lc, '(objectCategory=person)', process_person)
search_objects(l, lc, '(objectCategory=computer)', process_computer)
# search_objects(l, lc, '(objectCategory=group)', process_group)
l.unbind()
sys.exit(0)
