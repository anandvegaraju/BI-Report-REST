# Developed by Anand Vegaraju
# This web service only supports reports with CSV output. Please ensure the user account used has the right credentials
# Tested on Windows 10
# Requires 2 mandatory parameters - csvDelimiter and instanceURL

from flask import Flask, jsonify, request
import requests
import json
from json import dumps
from requests import Session
from zeep import Client, Settings
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import base64
import csv
import os

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


app = Flask(__name__)
session = requests.Session()
session.trust_env = False


#User Inputs (Instance specific)
userName = 'USERNAME' #Instance user account Name
password = 'PASSWORD' #User account password. Basic Auth only

@app.route('/getReport', methods=['GET'])
def getReport():
    headerArr = {}
    settings = Settings(strict=False, xml_huge_tree=True,extra_http_headers=headerArr,raw_response=True)
    session = Session()
    session.auth = HTTPBasicAuth(userName, password)
    transport_with_basic_auth = Transport(session=session)
    client = Client(request.args['instanceURL'] + '/xmlpserver/services/ExternalReportWSSService?WSDL',settings=settings, transport=transport_with_basic_auth)
    requestData = {
        'reportRequest': {
                    'flattenXML':'True',
                    'byPassCache':'True',
                    'reportAbsolutePath': request.args['reportXDOpath'],
                    'sizeOfDataChunkDownload':'-1',
        },
        'appParams': ''
        ,
    }

    soapresult = client.service.runReport(**requestData)
    reportResultB64 = find_between(soapresult.text, '<ns2:reportBytes>', '</ns2:reportBytes>')
    reportResult = base64.b64decode(reportResultB64)
    f = open('reportData.csv',"wb")
    f.write(reportResult)
    f.close()
    with open('reportData.csv', 'r') as f:
        reader = csv.reader(f, delimiter=request.args['csvDelimiter'])
        data_list = list()
        for row in reader:
            data_list.append(row)
    data = [dict(zip(data_list[0],row)) for row in data_list]
    data.pop(0)
    #s = json.dumps(data)
    res = {'empdata':{'emp': []}}
    for i in range(len(data)):
        res['empdata']['emp'].append(data[i])
    return jsonify(res)

if __name__ == '__main__':
   app.run(debug=True, use_reloader=True)
