import pdb
import json
import subprocess

def read_json(filepath, filename):
    fullname = filepath + '/' + filename
    with open(fullname) as handle:
        dictdump = json.loads(handle.read())
    return dictdump

def check_liveness(ip):
    try:
        ping_cmd = f"ping {ip} -c 3"
        subprocess.check_output(ping_cmd, shell=True, stderr=subprocess.PIPE).decode()
    except subprocess.CalledProcessError as err:
        ip = ip + " is not alive"
    return ip

def fqdn_alias(domainname):
    if domainname == "sample.com":
        return check_liveness('10.145.69.216')
    if domainname == "foo.com":
        return check_liveness('10.144.75.221')
    if domainname == 'bar.com':
        return check_liveness('10.145.251.1')


def list_of_bigips(fqdns):
    bigips = []
    if type(fqdns) is list:
        for fqdn in fqdns:
            bigips.append(fqdn_alias(fqdn))
    else:
        bigips.append(fqdn_alias(fqdns))
    return bigips

def get_bigipPartition(allAs3):
    get_bigipPartition = sorted(set(allAs3.keys()))
    if allAs3['class'] == 'ADC':
        list_of_known_objects = ['class', 'controls', 'id', 'label', 'remark', 'schemaVersion', 'updateMode']
        for known_object in list_of_known_objects:
            get_bigipPartition.remove(known_object)
        bigipActualPartition = sorted(set(allAs3[get_bigipPartition[0]].keys()))
        list_of_known_objects = ['class', 'defaultRouteDomain']
        for known_object in list_of_known_objects:
            bigipActualPartition.remove(known_object)
        return get_bigipPartition[0], bigipActualPartition[0]

    bigipActualPartition = [None]
    if allAs3['class'] == 'Tenant':
        bigipActualPartition = sorted(set(allAs3[get_bigipPartition[0]].keys()))
        list_of_known_objects = ['class', 'defaultRouteDomain']
        for known_object in list_of_known_objects:
            bigipActualPartition.remove(known_object)
    return  None,bigipActualPartition[0]

def get_virtualserver(allvs):
    keys = sorted(set(allvs.keys()))
    keys.remove('class')
    keys.remove('template')
    names_dict = dict()
    for ind in keys:
        if allvs[ind]['class'] in ['Service_HTTP', 'Service_HTTPS']:
            names_dict['virtualServer'] = ind
        if allvs[ind]['class'] in ['Pool']:
            names_dict['pool'] = ind
        if allvs[ind]['class'] in ['Monitor']:
            names_dict['monitor'] = ind
    return names_dict

def parse_request(request):
    fqdn = request['request_body']['fqdn']
    parsed_data = dict()
    parsed_data['list_of_bigips'] = list_of_bigips(fqdn)

    if "poolMembers" in request['request_body'].keys():
        parsed_data['poolMembers'] = request['request_body']['poolMembers']
    if "vsPort" in request['request_body'].keys():
        parsed_data['vsPort'] = request['request_body']['vsPort']
    return parsed_data

def fetchReplaceAs3(bigip,parsed_data):
    curl_cmd = f"curl -ku admin:admin -X GET https://{bigip}/mgmt/shared/appsvcs/declare/"
    output = subprocess.check_output(curl_cmd, shell=True, stderr=subprocess.PIPE).decode()
    allAs3 = json.loads(output)
    bigip_partition, shared_bigip_partition = get_bigipPartition(allAs3)
    if bigip_partition is not None:
        namesdict = get_virtualserver(allAs3[bigip_partition][shared_bigip_partition])
        vsObjects = allAs3[bigip_partition][shared_bigip_partition]
    else:
        namesdict = get_virtualserver(allAs3[shared_bigip_partition])
        vsObjects = allAs3[shared_bigip_partition]
    if parsed_data['vsPort']:
        vsObjects[namesdict['virtualServer']]['virtualPort'] = int(parsed_data['vsPort'])
    for poolMember in parsed_data['poolMembers']:
        allVals = poolMember.split(':')
        newMember = {
            'addressDiscovery': 'static',
            'serverAddresses': allVals[0],
            'servicePort': int(allVals[1])
        }
        # Check for existence of the member
        is_poolmember_exists = False
        for member in vsObjects[namesdict['pool']]['members']:
            if newMember['serverAddresses'] in member['serverAddresses']:
                is_poolmember_exists = True

        if not is_poolmember_exists:
            vsObjects[namesdict['pool']]['members'][0]['serverAddresses'].append(allVals[0])
    allAs3 = json.dumps(allAs3)
    return allAs3

def post_as3(bigip,formedAs3):
    post_cmd = f"curl -ks -u admin:admin -H 'Content-Type: application/json' https://{bigip}/mgmt/shared/appsvcs/declare/ -X POST -d '" + formedAs3 + "'"
    post_result = subprocess.check_output(post_cmd, shell=True, stderr=subprocess.PIPE).decode()
    post_result = json.loads(post_result)
    #print(post_result)
    if "results" in post_result.keys():
        if post_result['results'][0]['code'] in [200, 202]:
            print(f"Pushed successfully to BIGIP: {bigip}")
    else:
        print(f"Post Failed to BIGIP: {bigip}, Revoked to the previous configuration")

def process_request(bigip,parsed_data):
    if "not alive" in bigip:
        print("\n\nProcessing request")
        print(f"BIGIP {bigip}")
        return
    print(f"\n\nProcessing request of BIGIP:{bigip}")
    # Get AS3 declaration and Replace with request
    formedAs3 = fetchReplaceAs3(bigip, parsed_data)
    # Send Declaration back to BIGIP
    post_as3(bigip, formedAs3)







