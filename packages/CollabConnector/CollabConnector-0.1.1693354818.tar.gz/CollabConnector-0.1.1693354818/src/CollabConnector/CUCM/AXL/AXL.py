import requests
from requests import Session
from requests.auth import HTTPBasicAuth
import sys
import os
import lxml
from zeep.transports import Transport
from zeep import Client, Settings
from zeep.helpers import serialize_object

requests.packages.urllib3.disable_warnings()


class Connect:
    def __init__(self, ipaddr, username, passwd, version="14.0", wsdl=None):
        # if type= cucm then set username/password for AXL connection
        if ipaddr is None or passwd is None or username is None:
            raise Exception(
                f'Usage: CollabConnector.AXL("ipaddr", "admin", "password", version="12.0", wsdl="./AXL/AXLAPI.wsdl")')
        else:
            self.username = username

            if wsdl:
                wsdl = wsdl
            elif version and int(version.split(".")[0]) < 10:
                wsdl = os.path.join(os.path.dirname(__file__), 'schema', '10.0', 'AXLAPI.wsdl')
            elif version:
                wsdl = os.path.join(os.path.dirname(__file__), 'schema', version, 'AXLAPI.wsdl')

            # create a SOAP client session
            session = Session()

            # avoid certificate verification by default and setup session
            session.verify = False
            session.auth = HTTPBasicAuth(username, passwd)
            transport = Transport(session=session, timeout=10)
            settings = Settings(strict=False, xml_huge_tree=True)

            # If WSDL file specified then create AXL SOAP connector
            if wsdl is not None:
                # Create the Zeep client with the specified settings
                client_axl = Client(wsdl, settings=settings, transport=transport)  # ,plugins = plugin )
                # Create the Zeep service binding to AXL at the specified CUCM
                try:
                    self.client = client_axl.create_service(
                        '{http://www.cisco.com/AXLAPIService/}AXLAPIBinding',
                        f'https://{ipaddr}:8443/axl/')

                except Exception as err:
                    print(f"SOAP/AXL Error could not create service: {err}", file=sys.stderr)
                    self.client = False

    def elements_to_dict(self, input):
        if input is None or isinstance(input, (str, int, float, complex, bool, tuple)):
            return input

        if isinstance(input, dict):
            for key, value in input.items():
                input[key] = self.elements_to_dict(value)
            return input

        elif isinstance(input, list):
            return_list = []
            for position in input:
                return_list.append(self.elements_to_dict(position))
            return return_list

        elif isinstance(input, lxml.etree._Element):
            element = {}  # {t.tag : map(etree_to_dict, t.iterchildren())}
            element.update(('@' + k, v) for k, v in input.attrib.iteritems())
            element[input.tag] = input.text
            return element

        else:
            return str(input)

    def getSipProfile(self, **args):
        try:
            resp = self.client.getSipProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipProfile`: ", str(err), file=sys.stderr)
            return []

    def listSipProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSipProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipProfile`: ", str(err), file=sys.stderr)
            return []

    def getSipProfileOptions(self, **args):
        try:
            resp = self.client.getSipProfileOptions(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipProfileOptions`: ", str(err), file=sys.stderr)
            return []

    def getSipTrunkSecurityProfile(self, **args):
        try:
            resp = self.client.getSipTrunkSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipTrunkSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def listSipTrunkSecurityProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSipTrunkSecurityProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipTrunkSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def getTimePeriod(self, **args):
        try:
            resp = self.client.getTimePeriod(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTimePeriod`: ", str(err), file=sys.stderr)
            return []

    def listTimePeriod(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listTimePeriod(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTimePeriod`: ", str(err), file=sys.stderr)
            return []

    def getTimeSchedule(self, **args):
        try:
            resp = self.client.getTimeSchedule(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTimeSchedule`: ", str(err), file=sys.stderr)
            return []

    def listTimeSchedule(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listTimeSchedule(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTimeSchedule`: ", str(err), file=sys.stderr)
            return []

    def getTodAccess(self, **args):
        try:
            resp = self.client.getTodAccess(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTodAccess`: ", str(err), file=sys.stderr)
            return []

    def listTodAccess(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listTodAccess(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTodAccess`: ", str(err), file=sys.stderr)
            return []

    def getVoiceMailPilot(self, **args):
        try:
            resp = self.client.getVoiceMailPilot(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVoiceMailPilot`: ", str(err), file=sys.stderr)
            return []

    def listVoiceMailPilot(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listVoiceMailPilot(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVoiceMailPilot`: ", str(err), file=sys.stderr)
            return []

    def getProcessNode(self, **args):
        try:
            resp = self.client.getProcessNode(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getProcessNode`: ", str(err), file=sys.stderr)
            return []

    def listProcessNode(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listProcessNode(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listProcessNode`: ", str(err), file=sys.stderr)
            return []

    def getCallerFilterList(self, **args):
        try:
            resp = self.client.getCallerFilterList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallerFilterList`: ", str(err), file=sys.stderr)
            return []

    def listCallerFilterList(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCallerFilterList(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallerFilterList`: ", str(err), file=sys.stderr)
            return []

    def getRoutePartition(self, **args):
        try:
            resp = self.client.getRoutePartition(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRoutePartition`: ", str(err), file=sys.stderr)
            return []

    def listRoutePartition(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRoutePartition(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRoutePartition`: ", str(err), file=sys.stderr)
            return []

    def getCss(self, **args):
        try:
            resp = self.client.getCss(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCss`: ", str(err), file=sys.stderr)
            return []

    def listCss(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCss(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCss`: ", str(err), file=sys.stderr)
            return []

    def getCallManager(self, **args):
        try:
            resp = self.client.getCallManager(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallManager`: ", str(err), file=sys.stderr)
            return []

    def listCallManager(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCallManager(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallManager`: ", str(err), file=sys.stderr)
            return []

    def getExpresswayCConfiguration(self, **args):
        try:
            resp = self.client.getExpresswayCConfiguration(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getExpresswayCConfiguration`: ", str(err), file=sys.stderr)
            return []

    def listExpresswayCConfiguration(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listExpresswayCConfiguration(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listExpresswayCConfiguration`: ", str(err), file=sys.stderr)
            return []

    def getMedia(self, **args):
        try:
            resp = self.client.getMedia(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMedia`: ", str(err), file=sys.stderr)
            return []

    def listMedia(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listMedia(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMedia`: ", str(err), file=sys.stderr)
            return []

    def getRegion(self, **args):
        try:
            resp = self.client.getRegion(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRegion`: ", str(err), file=sys.stderr)
            return []

    def listRegion(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRegion(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRegion`: ", str(err), file=sys.stderr)
            return []

    def getAarGroup(self, **args):
        try:
            resp = self.client.getAarGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAarGroup`: ", str(err), file=sys.stderr)
            return []

    def listAarGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listAarGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAarGroup`: ", str(err), file=sys.stderr)
            return []

    def getPhysicalLocation(self, **args):
        try:
            resp = self.client.getPhysicalLocation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhysicalLocation`: ", str(err), file=sys.stderr)
            return []

    def listPhysicalLocation(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listPhysicalLocation(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhysicalLocation`: ", str(err), file=sys.stderr)
            return []

    def getCustomer(self, **args):
        try:
            resp = self.client.getCustomer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCustomer`: ", str(err), file=sys.stderr)
            return []

    def listCustomer(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCustomer(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCustomer`: ", str(err), file=sys.stderr)
            return []

    def getRouteGroup(self, **args):
        try:
            resp = self.client.getRouteGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRouteGroup`: ", str(err), file=sys.stderr)
            return []

    def listRouteGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRouteGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRouteGroup`: ", str(err), file=sys.stderr)
            return []

    def getDevicePool(self, **args):
        try:
            resp = self.client.getDevicePool(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDevicePool`: ", str(err), file=sys.stderr)
            return []

    def listDevicePool(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDevicePool(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDevicePool`: ", str(err), file=sys.stderr)
            return []

    def getDeviceMobilityGroup(self, **args):
        try:
            resp = self.client.getDeviceMobilityGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDeviceMobilityGroup`: ", str(err), file=sys.stderr)
            return []

    def listDeviceMobilityGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDeviceMobilityGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDeviceMobilityGroup`: ", str(err), file=sys.stderr)
            return []

    def getLocation(self, **args):
        try:
            resp = self.client.getLocation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLocation`: ", str(err), file=sys.stderr)
            return []

    def listLocation(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLocation(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLocation`: ", str(err), file=sys.stderr)
            return []

    def getSoftKeyTemplate(self, **args):
        try:
            resp = self.client.getSoftKeyTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSoftKeyTemplate`: ", str(err), file=sys.stderr)
            return []

    def listSoftKeyTemplate(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSoftKeyTemplate(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSoftKeyTemplate`: ", str(err), file=sys.stderr)
            return []

    def getTranscoder(self, **args):
        try:
            resp = self.client.getTranscoder(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTranscoder`: ", str(err), file=sys.stderr)
            return []

    def listTranscoder(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listTranscoder(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTranscoder`: ", str(err), file=sys.stderr)
            return []

    def getCommonDeviceConfig(self, **args):
        try:
            resp = self.client.getCommonDeviceConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCommonDeviceConfig`: ", str(err), file=sys.stderr)
            return []

    def listCommonDeviceConfig(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCommonDeviceConfig(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCommonDeviceConfig`: ", str(err), file=sys.stderr)
            return []

    def getDeviceMobility(self, **args):
        try:
            resp = self.client.getDeviceMobility(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDeviceMobility`: ", str(err), file=sys.stderr)
            return []

    def listDeviceMobility(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDeviceMobility(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDeviceMobility`: ", str(err), file=sys.stderr)
            return []

    def getCmcInfo(self, **args):
        try:
            resp = self.client.getCmcInfo(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCmcInfo`: ", str(err), file=sys.stderr)
            return []

    def listCmcInfo(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCmcInfo(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCmcInfo`: ", str(err), file=sys.stderr)
            return []

    def getCredentialPolicy(self, **args):
        try:
            resp = self.client.getCredentialPolicy(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCredentialPolicy`: ", str(err), file=sys.stderr)
            return []

    def listCredentialPolicy(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCredentialPolicy(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCredentialPolicy`: ", str(err), file=sys.stderr)
            return []

    def getFacInfo(self, **args):
        try:
            resp = self.client.getFacInfo(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFacInfo`: ", str(err), file=sys.stderr)
            return []

    def listFacInfo(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listFacInfo(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listFacInfo`: ", str(err), file=sys.stderr)
            return []

    def getHuntList(self, **args):
        try:
            resp = self.client.getHuntList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getHuntList`: ", str(err), file=sys.stderr)
            return []

    def listHuntList(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listHuntList(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listHuntList`: ", str(err), file=sys.stderr)
            return []

    def getIvrUserLocale(self, **args):
        try:
            resp = self.client.getIvrUserLocale(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getIvrUserLocale`: ", str(err), file=sys.stderr)
            return []

    def listIvrUserLocale(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listIvrUserLocale(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listIvrUserLocale`: ", str(err), file=sys.stderr)
            return []

    def getLineGroup(self, **args):
        try:
            resp = self.client.getLineGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLineGroup`: ", str(err), file=sys.stderr)
            return []

    def listLineGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLineGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLineGroup`: ", str(err), file=sys.stderr)
            return []

    def getRecordingProfile(self, **args):
        try:
            resp = self.client.getRecordingProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRecordingProfile`: ", str(err), file=sys.stderr)
            return []

    def listRecordingProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRecordingProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRecordingProfile`: ", str(err), file=sys.stderr)
            return []

    def getRouteFilter(self, **args):
        try:
            resp = self.client.getRouteFilter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRouteFilter`: ", str(err), file=sys.stderr)
            return []

    def listRouteFilter(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRouteFilter(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRouteFilter`: ", str(err), file=sys.stderr)
            return []

    def getCallManagerGroup(self, **args):
        try:
            resp = self.client.getCallManagerGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallManagerGroup`: ", str(err), file=sys.stderr)
            return []

    def listCallManagerGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCallManagerGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallManagerGroup`: ", str(err), file=sys.stderr)
            return []

    def getUserGroup(self, **args):
        try:
            resp = self.client.getUserGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUserGroup`: ", str(err), file=sys.stderr)
            return []

    def listUserGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listUserGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUserGroup`: ", str(err), file=sys.stderr)
            return []

    def getDialPlan(self, **args):
        try:
            resp = self.client.getDialPlan(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDialPlan`: ", str(err), file=sys.stderr)
            return []

    def listDialPlan(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDialPlan(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDialPlan`: ", str(err), file=sys.stderr)
            return []

    def getDialPlanTag(self, **args):
        try:
            resp = self.client.getDialPlanTag(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDialPlanTag`: ", str(err), file=sys.stderr)
            return []

    def listDialPlanTag(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDialPlanTag(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDialPlanTag`: ", str(err), file=sys.stderr)
            return []

    def getDdi(self, **args):
        try:
            resp = self.client.getDdi(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDdi`: ", str(err), file=sys.stderr)
            return []

    def listDdi(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDdi(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDdi`: ", str(err), file=sys.stderr)
            return []

    def getMobileSmartClientProfile(self, **args):
        try:
            resp = self.client.getMobileSmartClientProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMobileSmartClientProfile`: ", str(err), file=sys.stderr)
            return []

    def listMobileSmartClientProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listMobileSmartClientProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMobileSmartClientProfile`: ", str(err), file=sys.stderr)
            return []

    def getProcessNodeService(self, **args):
        try:
            resp = self.client.getProcessNodeService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getProcessNodeService`: ", str(err), file=sys.stderr)
            return []

    def listProcessNodeService(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listProcessNodeService(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listProcessNodeService`: ", str(err), file=sys.stderr)
            return []

    def getMohAudioSource(self, **args):
        try:
            resp = self.client.getMohAudioSource(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMohAudioSource`: ", str(err), file=sys.stderr)
            return []

    def listMohAudioSource(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listMohAudioSource(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMohAudioSource`: ", str(err), file=sys.stderr)
            return []

    def getDhcpServer(self, **args):
        try:
            resp = self.client.getDhcpServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDhcpServer`: ", str(err), file=sys.stderr)
            return []

    def listDhcpServer(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDhcpServer(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDhcpServer`: ", str(err), file=sys.stderr)
            return []

    def getDhcpSubnet(self, **args):
        try:
            resp = self.client.getDhcpSubnet(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDhcpSubnet`: ", str(err), file=sys.stderr)
            return []

    def listDhcpSubnet(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDhcpSubnet(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDhcpSubnet`: ", str(err), file=sys.stderr)
            return []

    def getCallPark(self, **args):
        try:
            resp = self.client.getCallPark(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallPark`: ", str(err), file=sys.stderr)
            return []

    def listCallPark(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCallPark(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallPark`: ", str(err), file=sys.stderr)
            return []

    def getDirectedCallPark(self, **args):
        try:
            resp = self.client.getDirectedCallPark(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDirectedCallPark`: ", str(err), file=sys.stderr)
            return []

    def listDirectedCallPark(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDirectedCallPark(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDirectedCallPark`: ", str(err), file=sys.stderr)
            return []

    def getMeetMe(self, **args):
        try:
            resp = self.client.getMeetMe(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMeetMe`: ", str(err), file=sys.stderr)
            return []

    def listMeetMe(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listMeetMe(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMeetMe`: ", str(err), file=sys.stderr)
            return []

    def getConferenceNow(self, **args):
        try:
            resp = self.client.getConferenceNow(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getConferenceNow`: ", str(err), file=sys.stderr)
            return []

    def listConferenceNow(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listConferenceNow(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listConferenceNow`: ", str(err), file=sys.stderr)
            return []

    def getMobileVoiceAccess(self, **args):
        try:
            resp = self.client.getMobileVoiceAccess(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMobileVoiceAccess`: ", str(err), file=sys.stderr)
            return []

    def getRouteList(self, **args):
        try:
            resp = self.client.getRouteList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRouteList`: ", str(err), file=sys.stderr)
            return []

    def listRouteList(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRouteList(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRouteList`: ", str(err), file=sys.stderr)
            return []

    def getUser(self, **args):
        try:
            resp = self.client.getUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUser`: ", str(err), file=sys.stderr)
            return []

    def listUser(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listUser(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUser`: ", str(err), file=sys.stderr)
            return []

    def getAppUser(self, **args):
        try:
            resp = self.client.getAppUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAppUser`: ", str(err), file=sys.stderr)
            return []

    def listAppUser(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listAppUser(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAppUser`: ", str(err), file=sys.stderr)
            return []

    def getSipRealm(self, **args):
        try:
            resp = self.client.getSipRealm(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipRealm`: ", str(err), file=sys.stderr)
            return []

    def listSipRealm(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSipRealm(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipRealm`: ", str(err), file=sys.stderr)
            return []

    def getPhoneNtp(self, **args):
        try:
            resp = self.client.getPhoneNtp(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhoneNtp`: ", str(err), file=sys.stderr)
            return []

    def listPhoneNtp(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listPhoneNtp(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhoneNtp`: ", str(err), file=sys.stderr)
            return []

    def getDateTimeGroup(self, **args):
        try:
            resp = self.client.getDateTimeGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDateTimeGroup`: ", str(err), file=sys.stderr)
            return []

    def listDateTimeGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDateTimeGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDateTimeGroup`: ", str(err), file=sys.stderr)
            return []

    def getPresenceGroup(self, **args):
        try:
            resp = self.client.getPresenceGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPresenceGroup`: ", str(err), file=sys.stderr)
            return []

    def listPresenceGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listPresenceGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPresenceGroup`: ", str(err), file=sys.stderr)
            return []

    def getGeoLocation(self, **args):
        try:
            resp = self.client.getGeoLocation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGeoLocation`: ", str(err), file=sys.stderr)
            return []

    def listGeoLocation(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listGeoLocation(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listGeoLocation`: ", str(err), file=sys.stderr)
            return []

    def getSrst(self, **args):
        try:
            resp = self.client.getSrst(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSrst`: ", str(err), file=sys.stderr)
            return []

    def listSrst(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSrst(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSrst`: ", str(err), file=sys.stderr)
            return []

    def getMlppDomain(self, **args):
        try:
            resp = self.client.getMlppDomain(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMlppDomain`: ", str(err), file=sys.stderr)
            return []

    def listMlppDomain(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listMlppDomain(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMlppDomain`: ", str(err), file=sys.stderr)
            return []

    def getCumaServerSecurityProfile(self, **args):
        try:
            resp = self.client.getCumaServerSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCumaServerSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def listCumaServerSecurityProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCumaServerSecurityProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCumaServerSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def getApplicationServer(self, **args):
        try:
            resp = self.client.getApplicationServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getApplicationServer`: ", str(err), file=sys.stderr)
            return []

    def listApplicationServer(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listApplicationServer(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listApplicationServer`: ", str(err), file=sys.stderr)
            return []

    def getApplicationUserCapfProfile(self, **args):
        try:
            resp = self.client.getApplicationUserCapfProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getApplicationUserCapfProfile`: ", str(err), file=sys.stderr)
            return []

    def listApplicationUserCapfProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listApplicationUserCapfProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listApplicationUserCapfProfile`: ", str(err), file=sys.stderr)
            return []

    def getEndUserCapfProfile(self, **args):
        try:
            resp = self.client.getEndUserCapfProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getEndUserCapfProfile`: ", str(err), file=sys.stderr)
            return []

    def listEndUserCapfProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listEndUserCapfProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listEndUserCapfProfile`: ", str(err), file=sys.stderr)
            return []

    def getServiceParameter(self, **args):
        try:
            resp = self.client.getServiceParameter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getServiceParameter`: ", str(err), file=sys.stderr)
            return []

    def listServiceParameter(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listServiceParameter(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listServiceParameter`: ", str(err), file=sys.stderr)
            return []

    def getGeoLocationFilter(self, **args):
        try:
            resp = self.client.getGeoLocationFilter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGeoLocationFilter`: ", str(err), file=sys.stderr)
            return []

    def listGeoLocationFilter(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listGeoLocationFilter(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listGeoLocationFilter`: ", str(err), file=sys.stderr)
            return []

    def getVoiceMailProfile(self, **args):
        try:
            resp = self.client.getVoiceMailProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVoiceMailProfile`: ", str(err), file=sys.stderr)
            return []

    def listVoiceMailProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listVoiceMailProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVoiceMailProfile`: ", str(err), file=sys.stderr)
            return []

    def getVoiceMailPort(self, **args):
        try:
            resp = self.client.getVoiceMailPort(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVoiceMailPort`: ", str(err), file=sys.stderr)
            return []

    def listVoiceMailPort(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listVoiceMailPort(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVoiceMailPort`: ", str(err), file=sys.stderr)
            return []

    def getGatekeeper(self, **args):
        try:
            resp = self.client.getGatekeeper(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatekeeper`: ", str(err), file=sys.stderr)
            return []

    def listGatekeeper(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listGatekeeper(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listGatekeeper`: ", str(err), file=sys.stderr)
            return []

    def getPhoneButtonTemplate(self, **args):
        try:
            resp = self.client.getPhoneButtonTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhoneButtonTemplate`: ", str(err), file=sys.stderr)
            return []

    def listPhoneButtonTemplate(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listPhoneButtonTemplate(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhoneButtonTemplate`: ", str(err), file=sys.stderr)
            return []

    def getCommonPhoneConfig(self, **args):
        try:
            resp = self.client.getCommonPhoneConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCommonPhoneConfig`: ", str(err), file=sys.stderr)
            return []

    def listCommonPhoneConfig(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCommonPhoneConfig(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCommonPhoneConfig`: ", str(err), file=sys.stderr)
            return []

    def getMessageWaiting(self, **args):
        try:
            resp = self.client.getMessageWaiting(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMessageWaiting`: ", str(err), file=sys.stderr)
            return []

    def listMessageWaiting(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listMessageWaiting(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMessageWaiting`: ", str(err), file=sys.stderr)
            return []

    def getIpPhoneServices(self, **args):
        try:
            resp = self.client.getIpPhoneServices(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getIpPhoneServices`: ", str(err), file=sys.stderr)
            return []

    def listIpPhoneServices(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listIpPhoneServices(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listIpPhoneServices`: ", str(err), file=sys.stderr)
            return []

    def getCtiRoutePoint(self, **args):
        try:
            resp = self.client.getCtiRoutePoint(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCtiRoutePoint`: ", str(err), file=sys.stderr)
            return []

    def listCtiRoutePoint(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCtiRoutePoint(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCtiRoutePoint`: ", str(err), file=sys.stderr)
            return []

    def getTransPattern(self, **args):
        try:
            resp = self.client.getTransPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTransPattern`: ", str(err), file=sys.stderr)
            return []

    def listTransPattern(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listTransPattern(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTransPattern`: ", str(err), file=sys.stderr)
            return []

    def getTransPatternOptions(self, **args):
        try:
            resp = self.client.getTransPatternOptions(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTransPatternOptions`: ", str(err), file=sys.stderr)
            return []

    def getCallingPartyTransformationPattern(self, **args):
        try:
            resp = self.client.getCallingPartyTransformationPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallingPartyTransformationPattern`: ", str(err), file=sys.stderr)
            return []

    def listCallingPartyTransformationPattern(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCallingPartyTransformationPattern(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallingPartyTransformationPattern`: ", str(err), file=sys.stderr)
            return []

    def getSipRoutePattern(self, **args):
        try:
            resp = self.client.getSipRoutePattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipRoutePattern`: ", str(err), file=sys.stderr)
            return []

    def listSipRoutePattern(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSipRoutePattern(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipRoutePattern`: ", str(err), file=sys.stderr)
            return []

    def getHuntPilot(self, **args):
        try:
            resp = self.client.getHuntPilot(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getHuntPilot`: ", str(err), file=sys.stderr)
            return []

    def listHuntPilot(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listHuntPilot(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listHuntPilot`: ", str(err), file=sys.stderr)
            return []

    def getRoutePattern(self, **args):
        try:
            resp = self.client.getRoutePattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRoutePattern`: ", str(err), file=sys.stderr)
            return []

    def listRoutePattern(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRoutePattern(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRoutePattern`: ", str(err), file=sys.stderr)
            return []

    def getApplicationDialRules(self, **args):
        try:
            resp = self.client.getApplicationDialRules(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getApplicationDialRules`: ", str(err), file=sys.stderr)
            return []

    def listApplicationDialRules(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listApplicationDialRules(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listApplicationDialRules`: ", str(err), file=sys.stderr)
            return []

    def getDirectoryLookupDialRules(self, **args):
        try:
            resp = self.client.getDirectoryLookupDialRules(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDirectoryLookupDialRules`: ", str(err), file=sys.stderr)
            return []

    def listDirectoryLookupDialRules(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDirectoryLookupDialRules(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDirectoryLookupDialRules`: ", str(err), file=sys.stderr)
            return []

    def getPhoneSecurityProfile(self, **args):
        try:
            resp = self.client.getPhoneSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhoneSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def listPhoneSecurityProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listPhoneSecurityProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhoneSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def getSipDialRules(self, **args):
        try:
            resp = self.client.getSipDialRules(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipDialRules`: ", str(err), file=sys.stderr)
            return []

    def listSipDialRules(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSipDialRules(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipDialRules`: ", str(err), file=sys.stderr)
            return []

    def getConferenceBridge(self, **args):
        try:
            resp = self.client.getConferenceBridge(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getConferenceBridge`: ", str(err), file=sys.stderr)
            return []

    def listConferenceBridge(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listConferenceBridge(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listConferenceBridge`: ", str(err), file=sys.stderr)
            return []

    def getAnnunciator(self, **args):
        try:
            resp = self.client.getAnnunciator(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAnnunciator`: ", str(err), file=sys.stderr)
            return []

    def listAnnunciator(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listAnnunciator(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAnnunciator`: ", str(err), file=sys.stderr)
            return []

    def getInteractiveVoice(self, **args):
        try:
            resp = self.client.getInteractiveVoice(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getInteractiveVoice`: ", str(err), file=sys.stderr)
            return []

    def listInteractiveVoice(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listInteractiveVoice(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listInteractiveVoice`: ", str(err), file=sys.stderr)
            return []

    def getMtp(self, **args):
        try:
            resp = self.client.getMtp(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMtp`: ", str(err), file=sys.stderr)
            return []

    def listMtp(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listMtp(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMtp`: ", str(err), file=sys.stderr)
            return []

    def getFixedMohAudioSource(self, **args):
        try:
            resp = self.client.getFixedMohAudioSource(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFixedMohAudioSource`: ", str(err), file=sys.stderr)
            return []

    def getRemoteDestinationProfile(self, **args):
        try:
            resp = self.client.getRemoteDestinationProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRemoteDestinationProfile`: ", str(err), file=sys.stderr)
            return []

    def listRemoteDestinationProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRemoteDestinationProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRemoteDestinationProfile`: ", str(err), file=sys.stderr)
            return []

    def getLine(self, **args):
        try:
            resp = self.client.getLine(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLine`: ", str(err), file=sys.stderr)
            return []

    def listLine(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLine(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLine`: ", str(err), file=sys.stderr)
            return []

    def getLineOptions(self, **args):
        try:
            resp = self.client.getLineOptions(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLineOptions`: ", str(err), file=sys.stderr)
            return []

    def getDefaultDeviceProfile(self, **args):
        try:
            resp = self.client.getDefaultDeviceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDefaultDeviceProfile`: ", str(err), file=sys.stderr)
            return []

    def listDefaultDeviceProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDefaultDeviceProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDefaultDeviceProfile`: ", str(err), file=sys.stderr)
            return []

    def getH323Phone(self, **args):
        try:
            resp = self.client.getH323Phone(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getH323Phone`: ", str(err), file=sys.stderr)
            return []

    def listH323Phone(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listH323Phone(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listH323Phone`: ", str(err), file=sys.stderr)
            return []

    def getMohServer(self, **args):
        try:
            resp = self.client.getMohServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMohServer`: ", str(err), file=sys.stderr)
            return []

    def listMohServer(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listMohServer(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMohServer`: ", str(err), file=sys.stderr)
            return []

    def getH323Trunk(self, **args):
        try:
            resp = self.client.getH323Trunk(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getH323Trunk`: ", str(err), file=sys.stderr)
            return []

    def listH323Trunk(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listH323Trunk(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listH323Trunk`: ", str(err), file=sys.stderr)
            return []

    def getPhone(self, **args):
        try:
            resp = self.client.getPhone(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhone`: ", str(err), file=sys.stderr)
            return []

    def listPhone(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listPhone(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhone`: ", str(err), file=sys.stderr)
            return []

    def getPhoneOptions(self, **args):
        try:
            resp = self.client.getPhoneOptions(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhoneOptions`: ", str(err), file=sys.stderr)
            return []

    def getH323Gateway(self, **args):
        try:
            resp = self.client.getH323Gateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getH323Gateway`: ", str(err), file=sys.stderr)
            return []

    def listH323Gateway(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listH323Gateway(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listH323Gateway`: ", str(err), file=sys.stderr)
            return []

    def getDeviceProfile(self, **args):
        try:
            resp = self.client.getDeviceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDeviceProfile`: ", str(err), file=sys.stderr)
            return []

    def listDeviceProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDeviceProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDeviceProfile`: ", str(err), file=sys.stderr)
            return []

    def getDeviceProfileOptions(self, **args):
        try:
            resp = self.client.getDeviceProfileOptions(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDeviceProfileOptions`: ", str(err), file=sys.stderr)
            return []

    def getRemoteDestination(self, **args):
        try:
            resp = self.client.getRemoteDestination(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRemoteDestination`: ", str(err), file=sys.stderr)
            return []

    def listRemoteDestination(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRemoteDestination(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRemoteDestination`: ", str(err), file=sys.stderr)
            return []

    def getVg224(self, **args):
        try:
            resp = self.client.getVg224(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVg224`: ", str(err), file=sys.stderr)
            return []

    def getGateway(self, **args):
        try:
            resp = self.client.getGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGateway`: ", str(err), file=sys.stderr)
            return []

    def listGateway(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listGateway(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listGateway`: ", str(err), file=sys.stderr)
            return []

    def getGatewayEndpointAnalogAccess(self, **args):
        try:
            resp = self.client.getGatewayEndpointAnalogAccess(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatewayEndpointAnalogAccess`: ", str(err), file=sys.stderr)
            return []

    def getGatewayEndpointDigitalAccessPri(self, **args):
        try:
            resp = self.client.getGatewayEndpointDigitalAccessPri(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatewayEndpointDigitalAccessPri`: ", str(err), file=sys.stderr)
            return []

    def getGatewayEndpointDigitalAccessBri(self, **args):
        try:
            resp = self.client.getGatewayEndpointDigitalAccessBri(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatewayEndpointDigitalAccessBri`: ", str(err), file=sys.stderr)
            return []

    def getGatewayEndpointDigitalAccessT1(self, **args):
        try:
            resp = self.client.getGatewayEndpointDigitalAccessT1(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatewayEndpointDigitalAccessT1`: ", str(err), file=sys.stderr)
            return []

    def getCiscoCatalyst600024PortFXSGateway(self, **args):
        try:
            resp = self.client.getCiscoCatalyst600024PortFXSGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCiscoCatalyst600024PortFXSGateway`: ", str(err), file=sys.stderr)
            return []

    def listCiscoCatalyst600024PortFXSGateway(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCiscoCatalyst600024PortFXSGateway(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCiscoCatalyst600024PortFXSGateway`: ", str(err), file=sys.stderr)
            return []

    def getCiscoCatalyst6000E1VoIPGateway(self, **args):
        try:
            resp = self.client.getCiscoCatalyst6000E1VoIPGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCiscoCatalyst6000E1VoIPGateway`: ", str(err), file=sys.stderr)
            return []

    def listCiscoCatalyst6000E1VoIPGateway(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCiscoCatalyst6000E1VoIPGateway(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCiscoCatalyst6000E1VoIPGateway`: ", str(err), file=sys.stderr)
            return []

    def getCiscoCatalyst6000T1VoIPGatewayPri(self, **args):
        try:
            resp = self.client.getCiscoCatalyst6000T1VoIPGatewayPri(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCiscoCatalyst6000T1VoIPGatewayPri`: ", str(err), file=sys.stderr)
            return []

    def listCiscoCatalyst6000T1VoIPGatewayPri(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCiscoCatalyst6000T1VoIPGatewayPri(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCiscoCatalyst6000T1VoIPGatewayPri`: ", str(err), file=sys.stderr)
            return []

    def getCiscoCatalyst6000T1VoIPGatewayT1(self, **args):
        try:
            resp = self.client.getCiscoCatalyst6000T1VoIPGatewayT1(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCiscoCatalyst6000T1VoIPGatewayT1`: ", str(err), file=sys.stderr)
            return []

    def listCiscoCatalyst6000T1VoIPGatewayT1(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCiscoCatalyst6000T1VoIPGatewayT1(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCiscoCatalyst6000T1VoIPGatewayT1`: ", str(err), file=sys.stderr)
            return []

    def getCallPickupGroup(self, **args):
        try:
            resp = self.client.getCallPickupGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallPickupGroup`: ", str(err), file=sys.stderr)
            return []

    def listCallPickupGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCallPickupGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallPickupGroup`: ", str(err), file=sys.stderr)
            return []

    def listRoutePlan(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRoutePlan(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRoutePlan`: ", str(err), file=sys.stderr)
            return []

    def getGeoLocationPolicy(self, **args):
        try:
            resp = self.client.getGeoLocationPolicy(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGeoLocationPolicy`: ", str(err), file=sys.stderr)
            return []

    def listGeoLocationPolicy(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listGeoLocationPolicy(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listGeoLocationPolicy`: ", str(err), file=sys.stderr)
            return []

    def getSipTrunk(self, **args):
        try:
            resp = self.client.getSipTrunk(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipTrunk`: ", str(err), file=sys.stderr)
            return []

    def listSipTrunk(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSipTrunk(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipTrunk`: ", str(err), file=sys.stderr)
            return []

    def getCalledPartyTransformationPattern(self, **args):
        try:
            resp = self.client.getCalledPartyTransformationPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCalledPartyTransformationPattern`: ", str(err), file=sys.stderr)
            return []

    def listCalledPartyTransformationPattern(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCalledPartyTransformationPattern(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCalledPartyTransformationPattern`: ", str(err), file=sys.stderr)
            return []

    def getExternalCallControlProfile(self, **args):
        try:
            resp = self.client.getExternalCallControlProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getExternalCallControlProfile`: ", str(err), file=sys.stderr)
            return []

    def listExternalCallControlProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listExternalCallControlProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listExternalCallControlProfile`: ", str(err), file=sys.stderr)
            return []

    def getSafSecurityProfile(self, **args):
        try:
            resp = self.client.getSafSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSafSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def listSafSecurityProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSafSecurityProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSafSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def getSafForwarder(self, **args):
        try:
            resp = self.client.getSafForwarder(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSafForwarder`: ", str(err), file=sys.stderr)
            return []

    def listSafForwarder(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSafForwarder(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSafForwarder`: ", str(err), file=sys.stderr)
            return []

    def getCcdHostedDN(self, **args):
        try:
            resp = self.client.getCcdHostedDN(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCcdHostedDN`: ", str(err), file=sys.stderr)
            return []

    def listCcdHostedDN(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCcdHostedDN(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCcdHostedDN`: ", str(err), file=sys.stderr)
            return []

    def getCcdHostedDNGroup(self, **args):
        try:
            resp = self.client.getCcdHostedDNGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCcdHostedDNGroup`: ", str(err), file=sys.stderr)
            return []

    def listCcdHostedDNGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCcdHostedDNGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCcdHostedDNGroup`: ", str(err), file=sys.stderr)
            return []

    def getCcdRequestingService(self, **args):
        try:
            resp = self.client.getCcdRequestingService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCcdRequestingService`: ", str(err), file=sys.stderr)
            return []

    def getInterClusterServiceProfile(self, **args):
        try:
            resp = self.client.getInterClusterServiceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getInterClusterServiceProfile`: ", str(err), file=sys.stderr)
            return []

    def getRemoteCluster(self, **args):
        try:
            resp = self.client.getRemoteCluster(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRemoteCluster`: ", str(err), file=sys.stderr)
            return []

    def listRemoteCluster(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRemoteCluster(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRemoteCluster`: ", str(err), file=sys.stderr)
            return []

    def getCcdAdvertisingService(self, **args):
        try:
            resp = self.client.getCcdAdvertisingService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCcdAdvertisingService`: ", str(err), file=sys.stderr)
            return []

    def listCcdAdvertisingService(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCcdAdvertisingService(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCcdAdvertisingService`: ", str(err), file=sys.stderr)
            return []

    def getLdapDirectory(self, **args):
        try:
            resp = self.client.getLdapDirectory(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapDirectory`: ", str(err), file=sys.stderr)
            return []

    def listLdapDirectory(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLdapDirectory(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLdapDirectory`: ", str(err), file=sys.stderr)
            return []

    def getEmccFeatureConfig(self, **args):
        try:
            resp = self.client.getEmccFeatureConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getEmccFeatureConfig`: ", str(err), file=sys.stderr)
            return []

    def getSafCcdPurgeBlockLearnedRoutes(self, **args):
        try:
            resp = self.client.getSafCcdPurgeBlockLearnedRoutes(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSafCcdPurgeBlockLearnedRoutes`: ", str(err), file=sys.stderr)
            return []

    def listSafCcdPurgeBlockLearnedRoutes(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSafCcdPurgeBlockLearnedRoutes(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSafCcdPurgeBlockLearnedRoutes`: ", str(err), file=sys.stderr)
            return []

    def getVpnGateway(self, **args):
        try:
            resp = self.client.getVpnGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVpnGateway`: ", str(err), file=sys.stderr)
            return []

    def listVpnGateway(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listVpnGateway(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVpnGateway`: ", str(err), file=sys.stderr)
            return []

    def getVpnGroup(self, **args):
        try:
            resp = self.client.getVpnGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVpnGroup`: ", str(err), file=sys.stderr)
            return []

    def listVpnGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listVpnGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVpnGroup`: ", str(err), file=sys.stderr)
            return []

    def getVpnProfile(self, **args):
        try:
            resp = self.client.getVpnProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVpnProfile`: ", str(err), file=sys.stderr)
            return []

    def listVpnProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listVpnProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVpnProfile`: ", str(err), file=sys.stderr)
            return []

    def getImeServer(self, **args):
        try:
            resp = self.client.getImeServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeServer`: ", str(err), file=sys.stderr)
            return []

    def listImeServer(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImeServer(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeServer`: ", str(err), file=sys.stderr)
            return []

    def getImeRouteFilterGroup(self, **args):
        try:
            resp = self.client.getImeRouteFilterGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeRouteFilterGroup`: ", str(err), file=sys.stderr)
            return []

    def listImeRouteFilterGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImeRouteFilterGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeRouteFilterGroup`: ", str(err), file=sys.stderr)
            return []

    def getImeRouteFilterElement(self, **args):
        try:
            resp = self.client.getImeRouteFilterElement(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeRouteFilterElement`: ", str(err), file=sys.stderr)
            return []

    def listImeRouteFilterElement(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImeRouteFilterElement(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeRouteFilterElement`: ", str(err), file=sys.stderr)
            return []

    def getImeClient(self, **args):
        try:
            resp = self.client.getImeClient(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeClient`: ", str(err), file=sys.stderr)
            return []

    def listImeClient(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImeClient(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeClient`: ", str(err), file=sys.stderr)
            return []

    def getImeEnrolledPattern(self, **args):
        try:
            resp = self.client.getImeEnrolledPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeEnrolledPattern`: ", str(err), file=sys.stderr)
            return []

    def listImeEnrolledPattern(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImeEnrolledPattern(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeEnrolledPattern`: ", str(err), file=sys.stderr)
            return []

    def getImeEnrolledPatternGroup(self, **args):
        try:
            resp = self.client.getImeEnrolledPatternGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeEnrolledPatternGroup`: ", str(err), file=sys.stderr)
            return []

    def listImeEnrolledPatternGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImeEnrolledPatternGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeEnrolledPatternGroup`: ", str(err), file=sys.stderr)
            return []

    def getImeExclusionNumber(self, **args):
        try:
            resp = self.client.getImeExclusionNumber(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeExclusionNumber`: ", str(err), file=sys.stderr)
            return []

    def listImeExclusionNumber(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImeExclusionNumber(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeExclusionNumber`: ", str(err), file=sys.stderr)
            return []

    def getImeExclusionNumberGroup(self, **args):
        try:
            resp = self.client.getImeExclusionNumberGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeExclusionNumberGroup`: ", str(err), file=sys.stderr)
            return []

    def listImeExclusionNumberGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImeExclusionNumberGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeExclusionNumberGroup`: ", str(err), file=sys.stderr)
            return []

    def getImeFirewall(self, **args):
        try:
            resp = self.client.getImeFirewall(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeFirewall`: ", str(err), file=sys.stderr)
            return []

    def listImeFirewall(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImeFirewall(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeFirewall`: ", str(err), file=sys.stderr)
            return []

    def getImeE164Transformation(self, **args):
        try:
            resp = self.client.getImeE164Transformation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeE164Transformation`: ", str(err), file=sys.stderr)
            return []

    def listImeE164Transformation(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImeE164Transformation(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeE164Transformation`: ", str(err), file=sys.stderr)
            return []

    def getTransformationProfile(self, **args):
        try:
            resp = self.client.getTransformationProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTransformationProfile`: ", str(err), file=sys.stderr)
            return []

    def listTransformationProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listTransformationProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTransformationProfile`: ", str(err), file=sys.stderr)
            return []

    def getFallbackProfile(self, **args):
        try:
            resp = self.client.getFallbackProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFallbackProfile`: ", str(err), file=sys.stderr)
            return []

    def listFallbackProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listFallbackProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listFallbackProfile`: ", str(err), file=sys.stderr)
            return []

    def getLdapFilter(self, **args):
        try:
            resp = self.client.getLdapFilter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapFilter`: ", str(err), file=sys.stderr)
            return []

    def listLdapFilter(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLdapFilter(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLdapFilter`: ", str(err), file=sys.stderr)
            return []

    def getTvsCertificate(self, **args):
        try:
            resp = self.client.getTvsCertificate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTvsCertificate`: ", str(err), file=sys.stderr)
            return []

    def listTvsCertificate(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listTvsCertificate(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTvsCertificate`: ", str(err), file=sys.stderr)
            return []

    def getFeatureControlPolicy(self, **args):
        try:
            resp = self.client.getFeatureControlPolicy(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFeatureControlPolicy`: ", str(err), file=sys.stderr)
            return []

    def listFeatureControlPolicy(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listFeatureControlPolicy(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listFeatureControlPolicy`: ", str(err), file=sys.stderr)
            return []

    def getMobilityProfile(self, **args):
        try:
            resp = self.client.getMobilityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMobilityProfile`: ", str(err), file=sys.stderr)
            return []

    def listMobilityProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listMobilityProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMobilityProfile`: ", str(err), file=sys.stderr)
            return []

    def getEnterpriseFeatureAccessConfiguration(self, **args):
        try:
            resp = self.client.getEnterpriseFeatureAccessConfiguration(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getEnterpriseFeatureAccessConfiguration`: ", str(err), file=sys.stderr)
            return []

    def listEnterpriseFeatureAccessConfiguration(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listEnterpriseFeatureAccessConfiguration(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listEnterpriseFeatureAccessConfiguration`: ", str(err), file=sys.stderr)
            return []

    def getHandoffConfiguration(self, **args):
        try:
            resp = self.client.getHandoffConfiguration(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getHandoffConfiguration`: ", str(err), file=sys.stderr)
            return []

    def listCalledPartyTracing(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCalledPartyTracing(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCalledPartyTracing`: ", str(err), file=sys.stderr)
            return []

    def getSIPNormalizationScript(self, **args):
        try:
            resp = self.client.getSIPNormalizationScript(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSIPNormalizationScript`: ", str(err), file=sys.stderr)
            return []

    def listSIPNormalizationScript(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSIPNormalizationScript(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSIPNormalizationScript`: ", str(err), file=sys.stderr)
            return []

    def getCustomUserField(self, **args):
        try:
            resp = self.client.getCustomUserField(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCustomUserField`: ", str(err), file=sys.stderr)
            return []

    def listCustomUserField(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCustomUserField(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCustomUserField`: ", str(err), file=sys.stderr)
            return []

    def getGatewaySccpEndpoints(self, **args):
        try:
            resp = self.client.getGatewaySccpEndpoints(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatewaySccpEndpoints`: ", str(err), file=sys.stderr)
            return []

    def listBillingServer(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listBillingServer(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listBillingServer`: ", str(err), file=sys.stderr)
            return []

    def getLbmGroup(self, **args):
        try:
            resp = self.client.getLbmGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLbmGroup`: ", str(err), file=sys.stderr)
            return []

    def listLbmGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLbmGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLbmGroup`: ", str(err), file=sys.stderr)
            return []

    def getAnnouncement(self, **args):
        try:
            resp = self.client.getAnnouncement(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAnnouncement`: ", str(err), file=sys.stderr)
            return []

    def listAnnouncement(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listAnnouncement(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAnnouncement`: ", str(err), file=sys.stderr)
            return []

    def getServiceProfile(self, **args):
        try:
            resp = self.client.getServiceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getServiceProfile`: ", str(err), file=sys.stderr)
            return []

    def listServiceProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listServiceProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listServiceProfile`: ", str(err), file=sys.stderr)
            return []

    def getLdapSyncCustomField(self, **args):
        try:
            resp = self.client.getLdapSyncCustomField(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapSyncCustomField`: ", str(err), file=sys.stderr)
            return []

    def getAudioCodecPreferenceList(self, **args):
        try:
            resp = self.client.getAudioCodecPreferenceList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAudioCodecPreferenceList`: ", str(err), file=sys.stderr)
            return []

    def listAudioCodecPreferenceList(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listAudioCodecPreferenceList(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAudioCodecPreferenceList`: ", str(err), file=sys.stderr)
            return []

    def getUcService(self, **args):
        try:
            resp = self.client.getUcService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUcService`: ", str(err), file=sys.stderr)
            return []

    def listUcService(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listUcService(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUcService`: ", str(err), file=sys.stderr)
            return []

    def getLbmHubGroup(self, **args):
        try:
            resp = self.client.getLbmHubGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLbmHubGroup`: ", str(err), file=sys.stderr)
            return []

    def listLbmHubGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLbmHubGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLbmHubGroup`: ", str(err), file=sys.stderr)
            return []

    def getImportedDirectoryUriCatalogs(self, **args):
        try:
            resp = self.client.getImportedDirectoryUriCatalogs(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImportedDirectoryUriCatalogs`: ", str(err), file=sys.stderr)
            return []

    def listImportedDirectoryUriCatalogs(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listImportedDirectoryUriCatalogs(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImportedDirectoryUriCatalogs`: ", str(err), file=sys.stderr)
            return []

    def getVohServer(self, **args):
        try:
            resp = self.client.getVohServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVohServer`: ", str(err), file=sys.stderr)
            return []

    def listVohServer(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listVohServer(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVohServer`: ", str(err), file=sys.stderr)
            return []

    def getSdpTransparencyProfile(self, **args):
        try:
            resp = self.client.getSdpTransparencyProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSdpTransparencyProfile`: ", str(err), file=sys.stderr)
            return []

    def listSdpTransparencyProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listSdpTransparencyProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSdpTransparencyProfile`: ", str(err), file=sys.stderr)
            return []

    def getFeatureGroupTemplate(self, **args):
        try:
            resp = self.client.getFeatureGroupTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFeatureGroupTemplate`: ", str(err), file=sys.stderr)
            return []

    def listFeatureGroupTemplate(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listFeatureGroupTemplate(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listFeatureGroupTemplate`: ", str(err), file=sys.stderr)
            return []

    def getDirNumberAliasLookupandSync(self, **args):
        try:
            resp = self.client.getDirNumberAliasLookupandSync(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDirNumberAliasLookupandSync`: ", str(err), file=sys.stderr)
            return []

    def listDirNumberAliasLookupandSync(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDirNumberAliasLookupandSync(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDirNumberAliasLookupandSync`: ", str(err), file=sys.stderr)
            return []

    def getLocalRouteGroup(self, **args):
        try:
            resp = self.client.getLocalRouteGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLocalRouteGroup`: ", str(err), file=sys.stderr)
            return []

    def listLocalRouteGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLocalRouteGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLocalRouteGroup`: ", str(err), file=sys.stderr)
            return []

    def getAdvertisedPatterns(self, **args):
        try:
            resp = self.client.getAdvertisedPatterns(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAdvertisedPatterns`: ", str(err), file=sys.stderr)
            return []

    def listAdvertisedPatterns(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listAdvertisedPatterns(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAdvertisedPatterns`: ", str(err), file=sys.stderr)
            return []

    def getBlockedLearnedPatterns(self, **args):
        try:
            resp = self.client.getBlockedLearnedPatterns(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getBlockedLearnedPatterns`: ", str(err), file=sys.stderr)
            return []

    def listBlockedLearnedPatterns(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listBlockedLearnedPatterns(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listBlockedLearnedPatterns`: ", str(err), file=sys.stderr)
            return []

    def getCCAProfiles(self, **args):
        try:
            resp = self.client.getCCAProfiles(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCCAProfiles`: ", str(err), file=sys.stderr)
            return []

    def listCCAProfiles(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCCAProfiles(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCCAProfiles`: ", str(err), file=sys.stderr)
            return []

    def getUniversalDeviceTemplate(self, **args):
        try:
            resp = self.client.getUniversalDeviceTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUniversalDeviceTemplate`: ", str(err), file=sys.stderr)
            return []

    def listUniversalDeviceTemplate(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listUniversalDeviceTemplate(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUniversalDeviceTemplate`: ", str(err), file=sys.stderr)
            return []

    def getUserProfileProvision(self, **args):
        try:
            resp = self.client.getUserProfileProvision(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUserProfileProvision`: ", str(err), file=sys.stderr)
            return []

    def listUserProfileProvision(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listUserProfileProvision(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUserProfileProvision`: ", str(err), file=sys.stderr)
            return []

    def getPresenceRedundancyGroup(self, **args):
        try:
            resp = self.client.getPresenceRedundancyGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPresenceRedundancyGroup`: ", str(err), file=sys.stderr)
            return []

    def listPresenceRedundancyGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listPresenceRedundancyGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPresenceRedundancyGroup`: ", str(err), file=sys.stderr)
            return []

    def listAssignedPresenceServers(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listAssignedPresenceServers(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAssignedPresenceServers`: ", str(err), file=sys.stderr)
            return []

    def listUnassignedPresenceServers(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listUnassignedPresenceServers(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUnassignedPresenceServers`: ", str(err), file=sys.stderr)
            return []

    def listAssignedPresenceUsers(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listAssignedPresenceUsers(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAssignedPresenceUsers`: ", str(err), file=sys.stderr)
            return []

    def listUnassignedPresenceUsers(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listUnassignedPresenceUsers(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUnassignedPresenceUsers`: ", str(err), file=sys.stderr)
            return []

    def getWifiHotspot(self, **args):
        try:
            resp = self.client.getWifiHotspot(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getWifiHotspot`: ", str(err), file=sys.stderr)
            return []

    def listWifiHotspot(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listWifiHotspot(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listWifiHotspot`: ", str(err), file=sys.stderr)
            return []

    def getWlanProfileGroup(self, **args):
        try:
            resp = self.client.getWlanProfileGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getWlanProfileGroup`: ", str(err), file=sys.stderr)
            return []

    def listWlanProfileGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listWlanProfileGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listWlanProfileGroup`: ", str(err), file=sys.stderr)
            return []

    def getWLANProfile(self, **args):
        try:
            resp = self.client.getWLANProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getWLANProfile`: ", str(err), file=sys.stderr)
            return []

    def listWLANProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listWLANProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listWLANProfile`: ", str(err), file=sys.stderr)
            return []

    def getUniversalLineTemplate(self, **args):
        try:
            resp = self.client.getUniversalLineTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUniversalLineTemplate`: ", str(err), file=sys.stderr)
            return []

    def listUniversalLineTemplate(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listUniversalLineTemplate(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUniversalLineTemplate`: ", str(err), file=sys.stderr)
            return []

    def getNetworkAccessProfile(self, **args):
        try:
            resp = self.client.getNetworkAccessProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getNetworkAccessProfile`: ", str(err), file=sys.stderr)
            return []

    def listNetworkAccessProfile(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listNetworkAccessProfile(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listNetworkAccessProfile`: ", str(err), file=sys.stderr)
            return []

    def getLicensedUser(self, **args):
        try:
            resp = self.client.getLicensedUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLicensedUser`: ", str(err), file=sys.stderr)
            return []

    def listLicensedUser(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLicensedUser(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLicensedUser`: ", str(err), file=sys.stderr)
            return []

    def getHttpProfile(self, **args):
        try:
            resp = self.client.getHttpProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getHttpProfile`: ", str(err), file=sys.stderr)
            return []

    def getElinGroup(self, **args):
        try:
            resp = self.client.getElinGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getElinGroup`: ", str(err), file=sys.stderr)
            return []

    def listElinGroup(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listElinGroup(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listElinGroup`: ", str(err), file=sys.stderr)
            return []

    def getSecureConfig(self, **args):
        try:
            resp = self.client.getSecureConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSecureConfig`: ", str(err), file=sys.stderr)
            return []

    def listUnassignedDevice(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listUnassignedDevice(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUnassignedDevice`: ", str(err), file=sys.stderr)
            return []

    def getRegistrationDynamic(self, **args):
        try:
            resp = self.client.getRegistrationDynamic(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRegistrationDynamic`: ", str(err), file=sys.stderr)
            return []

    def listRegistrationDynamic(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listRegistrationDynamic(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRegistrationDynamic`: ", str(err), file=sys.stderr)
            return []

    def getInfrastructureDevice(self, **args):
        try:
            resp = self.client.getInfrastructureDevice(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getInfrastructureDevice`: ", str(err), file=sys.stderr)
            return []

    def listInfrastructureDevice(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listInfrastructureDevice(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listInfrastructureDevice`: ", str(err), file=sys.stderr)
            return []

    def getLdapSearch(self, **args):
        try:
            resp = self.client.getLdapSearch(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapSearch`: ", str(err), file=sys.stderr)
            return []

    def listLdapSearch(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLdapSearch(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLdapSearch`: ", str(err), file=sys.stderr)
            return []

    def getWirelessAccessPointControllers(self, **args):
        try:
            resp = self.client.getWirelessAccessPointControllers(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getWirelessAccessPointControllers`: ", str(err), file=sys.stderr)
            return []

    def listWirelessAccessPointControllers(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listWirelessAccessPointControllers(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listWirelessAccessPointControllers`: ", str(err), file=sys.stderr)
            return []

    def listPhoneActivationCode(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listPhoneActivationCode(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhoneActivationCode`: ", str(err), file=sys.stderr)
            return []

    def getDeviceDefaults(self, **args):
        try:
            resp = self.client.getDeviceDefaults(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDeviceDefaults`: ", str(err), file=sys.stderr)
            return []

    def listDeviceDefaults(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listDeviceDefaults(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDeviceDefaults`: ", str(err), file=sys.stderr)
            return []

    def getMraServiceDomain(self, **args):
        try:
            resp = self.client.getMraServiceDomain(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMraServiceDomain`: ", str(err), file=sys.stderr)
            return []

    def listMraServiceDomain(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listMraServiceDomain(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMraServiceDomain`: ", str(err), file=sys.stderr)
            return []

    def listCiscoCloudOnboarding(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listCiscoCloudOnboarding(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCiscoCloudOnboarding`: ", str(err), file=sys.stderr)
            return []

    def executeSQLQuery(self, **args):
        try:
            resp = self.client.executeSQLQuery(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `executeSQLQuery`: ", str(err), file=sys.stderr)
            return []

    def executeSQLQueryInactive(self, **args):
        try:
            resp = self.client.executeSQLQueryInactive(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `executeSQLQueryInactive`: ", str(err), file=sys.stderr)
            return []

    def executeSQLUpdate(self, **args):
        try:
            resp = self.client.executeSQLUpdate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `executeSQLUpdate`: ", str(err), file=sys.stderr)
            return []

    def doAuthenticateUser(self, **args):
        try:
            resp = self.client.doAuthenticateUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `doAuthenticateUser`: ", str(err), file=sys.stderr)
            return []

    def getOSVersion(self, **args):
        try:
            resp = self.client.getOSVersion(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getOSVersion`: ", str(err), file=sys.stderr)
            return []

    def getMobility(self, **args):
        try:
            resp = self.client.getMobility(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMobility`: ", str(err), file=sys.stderr)
            return []

    def getEnterprisePhoneConfig(self, **args):
        try:
            resp = self.client.getEnterprisePhoneConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getEnterprisePhoneConfig`: ", str(err), file=sys.stderr)
            return []

    def getLdapSystem(self, **args):
        try:
            resp = self.client.getLdapSystem(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapSystem`: ", str(err), file=sys.stderr)
            return []

    def getLdapAuthentication(self, **args):
        try:
            resp = self.client.getLdapAuthentication(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapAuthentication`: ", str(err), file=sys.stderr)
            return []

    def getCCMVersion(self, **args):
        try:
            resp = self.client.getCCMVersion(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCCMVersion`: ", str(err), file=sys.stderr)
            return []

    def getFallbackFeatureConfig(self, **args):
        try:
            resp = self.client.getFallbackFeatureConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFallbackFeatureConfig`: ", str(err), file=sys.stderr)
            return []

    def getImeLearnedRoutes(self, **args):
        try:
            resp = self.client.getImeLearnedRoutes(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeLearnedRoutes`: ", str(err), file=sys.stderr)
            return []

    def getImeFeatureConfig(self, **args):
        try:
            resp = self.client.getImeFeatureConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeFeatureConfig`: ", str(err), file=sys.stderr)
            return []

    def getAppServerInfo(self, **args):
        try:
            resp = self.client.getAppServerInfo(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAppServerInfo`: ", str(err), file=sys.stderr)
            return []

    def getSoftKeySet(self, **args):
        try:
            resp = self.client.getSoftKeySet(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSoftKeySet`: ", str(err), file=sys.stderr)
            return []

    def getSyslogConfiguration(self, **args):
        try:
            resp = self.client.getSyslogConfiguration(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSyslogConfiguration`: ", str(err), file=sys.stderr)
            return []

    def listLdapSyncCustomField(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listLdapSyncCustomField(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLdapSyncCustomField`: ", str(err), file=sys.stderr)
            return []

    def getIlsConfig(self, **args):
        try:
            resp = self.client.getIlsConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getIlsConfig`: ", str(err), file=sys.stderr)
            return []

    def getSNMPCommunityString(self, **args):
        try:
            resp = self.client.getSNMPCommunityString(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSNMPCommunityString`: ", str(err), file=sys.stderr)
            return []

    def getSNMPUser(self, **args):
        try:
            resp = self.client.getSNMPUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSNMPUser`: ", str(err), file=sys.stderr)
            return []

    def getSNMPMIB2List(self, **args):
        try:
            resp = self.client.getSNMPMIB2List(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSNMPMIB2List`: ", str(err), file=sys.stderr)
            return []

    def getBillingServer(self, **args):
        try:
            resp = self.client.getBillingServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getBillingServer`: ", str(err), file=sys.stderr)
            return []

    def getCcdFeatureConfig(self, **args):
        try:
            resp = self.client.getCcdFeatureConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCcdFeatureConfig`: ", str(err), file=sys.stderr)
            return []

    def getPageLayoutPreferences(self, **args):
        try:
            resp = self.client.getPageLayoutPreferences(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPageLayoutPreferences`: ", str(err), file=sys.stderr)
            return []

    def getCredentialPolicyDefault(self, **args):
        try:
            resp = self.client.getCredentialPolicyDefault(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCredentialPolicyDefault`: ", str(err), file=sys.stderr)
            return []

    def listChange(self, searchCriteria={}, returnedTags=[]):
        try:
            resp = self.client.listChange(searchCriteria=searchCriteria, returnedTags=returnedTags)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listChange`: ", str(err), file=sys.stderr)
            return []

    def getSmartLicenseStatus(self, **args):
        try:
            resp = self.client.getSmartLicenseStatus(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))

                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]

                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSmartLicenseStatus`: ", str(err), file=sys.stderr)
            return []
