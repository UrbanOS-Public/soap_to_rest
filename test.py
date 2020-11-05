import logging
import json
from zeep.helpers import serialize_object
from xml.etree.ElementTree import fromstring

from xmljson import parker
#from suds.client import Client
#from suds.xsd.doctor import ImportDoctor, Import

# logging.basicConfig(level=logging.DEBUG)

#imp = Import('http://www.tmdd.org/303/messages', location='https://scos-third-party-repository.s3.us-east-2.amazonaws.com/wsdl/TMDD.xsd')
#doctor = ImportDoctor(imp)
from zeep import Client, Settings
#settings = Settings(force_https=False, extra_http_headers={'soapaction': 'dlIntersectionSignalStatusRequest'}, strict=False, raw_response=True)
settings = Settings(force_https=False, strict=False, raw_response=True)
#client = Client("https://scos-third-party-repository.s3.us-east-2.amazonaws.com/wsdl/tmdd_http.wsdl", settings=settings)
client = Client("http://www.dneonline.com/calculator.asmx?WSDL", settings=settings)

# params = {
#         "organization-requesting": {
#             "organization-id": "COLB4321"
#         }
#     }

params = {
    "authentication": {
        "user-id": "user",
        "password": "password"
    },
    "organization-information": {
        "organization-id": "COLB4321"
    },
    "organization-requesting": {
        "organization-id": "COLB4321"
    },
    "device-type": 9,
    "device-information-type": 2
}

add_params = {
    "intA": 1,
    "intB": 2
        }


# client.service.dlCenterActiveVerificationRequest(**params)
# client.service.dlIntersectionSignalControlScheduleRequest(**params)
#serialized = serialize_object(client.service.dlIntersectionSignalStatusRequest(**params))
#print('ser', serialized)
#print('result', json.dumps(serialized))
#xml = client.service.dlIntersectionSignalStatusRequest(**params).content
xml = client.service.Add(**add_params).content
print(json.dumps(parker.data(fromstring(xml)), sort_keys=True, indent=4, separators=(',', ': ')))
