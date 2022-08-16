# coding:utf8
# python3

"""
virsh dumpxml win7
virsh net-dumpxml hostonly
virsh net-define hostonly_net.xml
virsh net-destroy hostonly
virsh net-start hostonly

查看、绑定、删除绑定机器与hostonly网络的ip关系
python machine_hostonly_net_ip.py set <machine_name> <ip>
python machine_hostonly_net_ip.py del <machine_name>
python machine_hostonly_net_ip.py get <machine_name>
"""

import sys
import subprocess
import tempfile
from xml.dom.minidom import parseString


def set_ip(machine_name, ip):
    machine_xml = subprocess.run(
        ["virsh", "dumpxml", machine_name], capture_output=True
    )
    machine_doc = parseString(machine_xml.stdout)
    mac = (
        machine_doc.documentElement.getElementsByTagName("devices")[0]
        .getElementsByTagName("interface")[0]
        .getElementsByTagName("mac")[0]
        .getAttribute("address")
    )

    network_xml = subprocess.run(
        ["virsh", "net-dumpxml", "hostonly"], capture_output=True
    )
    network_doc = parseString(network_xml.stdout)

    dhcp_node = network_doc.documentElement.getElementsByTagName("ip")[
        0
    ].getElementsByTagName("dhcp")[0]
    hosts = dhcp_node.getElementsByTagName("host")
    for host in hosts:
        name = host.getAttribute("name")
        if name == machine_name:
            mac = host.getAttribute("mac")
            host.setAttribute("ip", ip)
            break
    else:
        curr_host_node = network_doc.createElement("host")
        curr_host_node.setAttribute("mac", mac)
        curr_host_node.setAttribute("name", machine_name)
        curr_host_node.setAttribute("ip", ip)

        dhcp_node.appendChild(curr_host_node)

    with tempfile.NamedTemporaryFile(mode="w") as temp_file:
        network_doc.writexml(temp_file)
        temp_file.flush()

        # update network
        subprocess.run(["virsh", "net-define", temp_file.name])

        print("Network defined, restarting it")
        subprocess.run(["virsh", "net-destroy", "hostonly"])
        subprocess.run(["virsh", "net-start", "hostonly"])
        print(f"name: {name}, mac: {mac}, ip: {ip}, bind has been set up")


def del_machine_ip(machine_name):
    # machine_name can be "all"
    mac = None
    ip = None
    network_xml = subprocess.run(
        ["virsh", "net-dumpxml", "hostonly"], capture_output=True
    )
    network_doc = parseString(network_xml.stdout)

    dhcp_node = network_doc.documentElement.getElementsByTagName("ip")[
        0
    ].getElementsByTagName("dhcp")[0]
    hosts = dhcp_node.getElementsByTagName("host")
    if machine_name == "all":
        for host in hosts:
            name = host.getAttribute("name")
            mac = host.getAttribute("mac")
            ip = host.getAttribute("ip")
            parent = host.parentNode
            parent.removeChild(host)
            print(f"name: {name}, mac: {mac}, ip: {ip}, bind will be deleted")
    else:
        for host in hosts:
            name = host.getAttribute("name")
            if name == machine_name:
                mac = host.getAttribute("mac")
                ip = host.getAttribute("ip")
                parent = host.parentNode
                parent.removeChild(host)
                break
        else:
            print(f'No host named "{machine_name}"!!!')
            return

    with tempfile.NamedTemporaryFile(mode="w") as temp_file:
        network_doc.writexml(temp_file)
        temp_file.flush()

        # update network
        subprocess.run(["virsh", "net-define", temp_file.name])

        print("Network defined, restarting it")
        subprocess.run(["virsh", "net-destroy", "hostonly"])
        subprocess.run(["virsh", "net-start", "hostonly"])
        if machine_name == "all":
            print("All binds have been deleted")
        else:
            print(f"name: {name}, mac: {mac}, ip: {ip}, bind has been deleted")


def get_ip(machine_name):
    # machine_name can be "all"
    network_xml = subprocess.run(
        ["virsh", "net-dumpxml", "hostonly"], capture_output=True
    )
    network_doc = parseString(network_xml.stdout)

    dhcp_node = network_doc.documentElement.getElementsByTagName("ip")[
        0
    ].getElementsByTagName("dhcp")[0]
    hosts = dhcp_node.getElementsByTagName("host")
    if machine_name == "all":
        for host in hosts:
            name = host.getAttribute("name")
            mac = host.getAttribute("mac")
            ip = host.getAttribute("ip")
            print(f"name: {name}, mac: {mac}, ip: {ip}")
    else:
        for host in hosts:
            name = host.getAttribute("name")
            if name == machine_name:
                mac = host.getAttribute("mac")
                ip = host.getAttribute("ip")
                print(f"name: {name}, mac: {mac}, ip: {ip}")
                return
        else:
            print(f'No host "{machine_name}"')


def print_usage():
    script_path = sys.argv[0]
    print("usage:")
    print(f"    python {script_path} set <machine_name> <ip>")
    print(f"    python {script_path} del|get <machine_name>")
    print("example:")
    print(f"    python {script_path} set win7 192.168.100.131")
    print(f"    python {script_path} del win7")
    print(f"    python {script_path} get all")


def main():
    args = sys.argv
    print(args)
    arg_num = len(args) - 1
    if arg_num not in [2, 3]:
        print_usage()
        return
    action = args[1]
    machine_name = args[2]
    if action not in ["set", "del", "get"]:
        print_usage()
        return
    if action == "set":
        if arg_num != 3:
            print_usage()
            return
        ip = args[3]
        set_ip(machine_name, ip)
    elif action == "del":
        del_machine_ip(machine_name)
    elif action == "get":
        get_ip(machine_name)


if __name__ == "__main__":
    main()
