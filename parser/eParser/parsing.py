import xml.etree.ElementTree as ET
import os
from constants import test_description_file, test_results_file

def parse_result_file(path) -> dict:
    xml_file = os.path.join(path, test_results_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()

    results = dict()


    # STATUS
    status = root.find('status').text
    results['status'] = 'SUCCESS' if status == 'STATUS_SUCCESS' else 'ERROR'


    # CONCULSION
    report = dict()
    custom_root = root.find('custom')
    report['total'] = int(custom_root.find('num_total').text)
    report['losses'] = int(custom_root.find('num_loss').text)
    report['timer_misses'] = int(custom_root.find('num_misses').text)

    duration = custom_root.find('elapsed_time')
    if duration is not None:
        report['duration'] = float(duration.text)
    else:
        report['duration'] = -1   # no value present

    results['report'] = report


    # STATISTICS <ethtool_statistic>
    ethtool_statistic = {}
    ethtool_statistic_root = root.find('ethtool_statistic')
    if ethtool_statistic_root is not None:
        for child in ethtool_statistic_root:
            start = int(child.find('start').text)
            end = int(child.find('end').text)
            ethtool_statistic[child.tag] = end - start

        results['ethtool_statistic'] = ethtool_statistic


    # STATISTICS <ip_statistic>
    ip_statistic = {}
    ip_statistic_root = root.find('ip_statistic')
    if ip_statistic_root is not None:
        for child in root.find('ip_statistic'):
            start = int(child.find('start').text)
            end = int(child.find('end').text)
            
            if 'mtu' == child.tag:
                ip_statistic[child.tag] = end
            else:
                ip_statistic[child.tag] = end - start

        results['ip_statistic'] = ip_statistic


    # STATISTICS <netstat_statistic>
    netstat_statistic = {}
    netstat_root = root.find('netstat_statistic')
    if netstat_root is not None:
        for child in netstat_root:
            start = int(child.find('start').text)
            end = int(child.find('end').text)
            netstat_statistic[child.tag] = end - start

        results['netstat_statistic'] = netstat_statistic


    return results


def parse_query_messages(path) -> list:
    xml_file = os.path.join(path, test_results_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    query_root = root.find('custom').find('query')
    if query_root is None:
        return None
    
    reports = list()


    for report in query_root.findall('report'):
        # REPORT CONTENT (Total and misses are reversed in the XML file, this is a bug in TestSuite.)
        misses = int(report.find('total').text)
        total = int(report.find('misses').text)
        timestamp = report.find('timestamp')
        if timestamp is not None:
            timestamp = float(timestamp.text)
        else:
            timestamp = -1   # no value present

        # DIFFERENCE
        if reports:
            difference = misses - reports[-1]['misses']
        else:
            difference = 0
        
        reports.append({
            'misses': misses,
            'total': total,
            'timestamp': timestamp,
            'difference': difference
        })

    return reports
    

def parse_description_file(path) -> dict:
    xml_file = os.path.join(path, test_description_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()

    description = dict()


    # METADATA
    metadata = dict()
    metadata_root = root.find('metadata')
    metadata['method'] = metadata_root.find('method').text
    metadata['t_uid'] = metadata_root.find('t_uid').text
    metadata['path'] = metadata_root.find('path').text

    description['metadata'] = metadata


    # DURATION
    description['duration'] = int(root.find('duration').text)


    # CONNECTION
    connection = dict()
    if description['metadata']['method'] == 'CUSTOM':
        connection_root = root.find('connection').find('custom')
        connection['client_ip'] = connection_root.find('client_ip').text
        connection['server_ip'] = connection_root.find('server_ip').text
        connection['port'] = int(connection_root.find('port').text)
        connection['cycle_time'] = int(connection_root.find('gap').text)
        connection['datagram_size'] = int(connection_root.find('datagram').find('size').text)
        connection['qos'] = (connection_root.find('qos').text == 'true')

    description['connection'] = connection


    # INTERFACES
    interface = dict()
    interface_root = root.find('interface')
    interface['client'] = interface_root.find('client').text
    interface['server'] = interface_root.find('server').text

    description['interfaces'] = interface


    # STRESS
    stress = dict()
    stress_root = root.find('stress')
    stress['type'] = stress_root.find('type').text
    stress['intensity'] = int(stress_root.find('num').text)

    location = stress_root.find('location').text
    if location == 'LOC_BOTH':
        stress['location'] = 'BOTH'
    elif location == 'LOC_CLIENT':
        stress['location'] = 'CLIENT'
    elif location == 'LOC_SERVER':
        stress['location'] = 'SERVER'

    description['stress'] = stress

    return description
