from pysnmp.hlapi import *  # pip install pysnmp


def get_by_ids(*oids):
    engine = SnmpEngine()
    community = CommunityData('public')
    target = UdpTransportTarget(('192.168.10.4', 161))
    cntxt = ContextData()

    prepared_paths = list(map(lambda elem: ObjectType(ObjectIdentity(elem)), list(oids)))

    g = getCmd(engine, community, target, cntxt, *prepared_paths)

    result = []

    data = next(g)
    for x in data[3]:
        result.append(x)

    return result


# get all fields by parent oid
def get_by_parent_oid(parent_oid):
    engine = SnmpEngine()
    community = CommunityData('public')
    target = UdpTransportTarget(('192.168.10.4', 161))
    cntxt = ContextData()

    prepared_parent = ObjectType(ObjectIdentity(parent_oid))
    g = nextCmd(engine, community, target, cntxt, prepared_parent)

    result = []

    is_finish = False
    while not is_finish:
        data = next(g)
        for x in data[3]:
            if str(x[0]).startswith(parent_oid):
                result.append(x)
            else:
                is_finish = True
                break

    return result


def get_bulk_by_parent_oid(parent_oid, bulk_size=25):
    engine = SnmpEngine()
    community = CommunityData('public')
    target = UdpTransportTarget(('192.168.10.4', 161))
    cntxt = ContextData()

    result = []
    is_finish = False
    start_bulk_oid = ObjectType(ObjectIdentity(parent_oid))
    while True:
        g = bulkCmd(engine, community, target, cntxt, 0, bulk_size, start_bulk_oid)

        for i in range(0, bulk_size):
            data = next(g)
            for x in data[3]:
                if str(x[0]).startswith(parent_oid):
                    result.append(x)
                    start_bulk_oid = ObjectType(x[0])
                else:
                    is_finish = True
                    break

            if is_finish:
                break

        if is_finish:
            break

    return result


def get_interfaces_data(index_oid, descr_oid, in_octets_oid, out_octets_oid):
    indexes = get_bulk_by_parent_oid(index_oid)
    decriptions = get_bulk_by_parent_oid(descr_oid)
    in_octets = get_bulk_by_parent_oid(in_octets_oid)
    out_octets = get_bulk_by_parent_oid(out_octets_oid)

    second_table_indexes = list(map(lambda elem: tuple(elem[0])[-1], in_octets))

    result = []
    for i in range(0, len(indexes)):
        try:
            second_table_index = second_table_indexes.index(indexes[i][1])

            result.append({
                'index': indexes[i][1],
                'description': decriptions[i][1],
                'in_octets': in_octets[second_table_index][1],
                'out_octets': out_octets[second_table_index][1]
            })
        except ValueError:
            print('Can\'t find index {} in second table'.format(i))
            continue

    return result


if __name__ == '__main__':
    # res = get_by_ids('1.3.6.1.2.1.1.1.0', '1.3.6.1.2.1.1.2.0')
    # res = get_by_parent_oid('1.3.6.1.2.1.1')
    # res = get_bulk_by_parent_oid('1.3.6.1.2.1.1', 15)
    res = get_interfaces_data(index_oid='1.3.6.1.2.1.2.2.1.1', descr_oid='1.3.6.1.2.1.2.2.1.2',
                              in_octets_oid='1.3.6.1.2.1.31.1.1.1.6', out_octets_oid='1.3.6.1.2.1.31.1.1.1.10')

    for elem in res:
        print('{} {} {} {}'.format(elem['index'], elem['description'], elem['in_octets'], elem['out_octets']))
