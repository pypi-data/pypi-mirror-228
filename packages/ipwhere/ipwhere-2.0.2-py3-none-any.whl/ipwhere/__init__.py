

__VERSION__ = "2.0.2"


# +++ implementation +++

from urllib.request import HTTPError

import json
import os
import socket
import sys
import urllib.parse
import urllib.request


# *** Symbolic constants ***

IPWHERE_API_KEY = os.getenv('IPWHERE_API_KEY')
IPWHERE_HTTP_OK = 200       # HTTP OK
IPWHERE_INVALID = 999       # Something wrong with the URI request

IPWHERE_VERSION = '1.2'
IPWHERE_UA      = 'ipwhere/'+IPWHERE_VERSION+' ('+sys.platform+')'

# IPInfoDB API URI:
IPINFODB_URI='http://ip-api.com/json'


# *** Implementation ***

def helpUser(unitTest = False):
   if not unitTest:
    print('Invalid arguments list - syntax:')
    print('ipwhere ip.add.re.ss\n')
    print('ip.add.re.ss is an octet-format IPv4 address.  It may also be a host name.')

    if IPWHERE_API_KEY is None:
        print('\nThe required IPWHERE_API_KEY environment variable is not defined.')
        print('Get a free API key from http://www.ipinfodb.com/ip_location_api_json.php')

    exit(1)


def die(message, exitCode, unitTest = False):
  if not unitTest:
    print(message)
    sys.exit(exitCode)


def fetchLocationData(address = None):
    request = urllib.request.Request(
        '/'.join([ IPINFODB_URI, address, ]),
        headers = {
            'Content-Type': 'application/json',
            # 'User-Agent': '	Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
            'User-Agent': IPWHERE_UA,
        },
        method = 'GET',
    )
    payload = None

    try:
        input   = urllib.request.urlopen(request)
        payload = input.read()
        status  = input.code
        input.close()
    except HTTPError as e:
        status  = e.code
        print("request = %s" % request)
        # TODO: Implement better handling here for v2.1
        die(e.headers, 1)
    except Exception as e:
        status = IPWHERE_INVALID
        print("request = %s" % request)
        # TODO: Implement better handling here for v2.1
        die(e, 2)

    return status, json.loads(payload)


def reverseDNSOf(location):
    try:
        hostInfo = socket.gethostbyaddr(location)
    except Exception as e:
        hostInfo = (('rDNS failed = %s' % e), None, None)

    return hostInfo[0]


def displayResultsIn(locationData, unitTest = False):
    output = '%s - %s (%s) is in %s, %s, %s' % (
        locationData['query'] if unitTest else sys.argv[1],
        locationData['query'],
        reverseDNSOf(locationData['query']),
        locationData['city'],
        locationData['regionName'],
        locationData['countryCode'] )

    if not unitTest:
        print(output)

    return output


def displayErrorIn(locationData, status):
    if locationData is not None:
        print('error processing your request - HTTP response = %d, %s' % (status, locationData['statusMessage']))
    else:
        print('error processing your request - HTTP response = %d' % status)


def _main():
    if len(sys.argv) < 2 or IPWHERE_API_KEY is None:
      helpUser()

    status, locationData = fetchLocationData(sys.argv[1])

    if status is IPWHERE_HTTP_OK:
        displayResultsIn(locationData)
    else:
        displayErrorIn(locationData, status)
        if status == IPWHERE_INVALID:
            helpUser()


# *** main ***

if __name__ == '__main__':
  try:
    _main()
  except KeyboardInterrupt:
    pass


