# coding:utf8
# python3

"""
用来删除虚机的脚本

1. 删除快照
virsh snapshot-list --domain win7-2 --name
virsh snapshot-delete --domain win7-2 --snapshotname snapshot_new

2. 查看虚机信息，得到硬盘文件路径
virsh dumpxml win7-2

3. undefine虚机，删除硬盘文件
virsh undefine win7-2 --storage /opt/VMs/win7-2.qcow2

4. 删除hostonly网络中的ip绑定关系
virsh net-dumpxml hostonly  # 然后移除指定的ip绑定信息，写xml文件
virsh net-define hostonly_net.xml
virsh net-destroy hostonly
virsh net-start hostonly
"""

import subprocess
import sys
import tempfile
from xml.dom.minidom import parseString


def delete_machines(machine_names):
    process_result = subprocess.run(
        ["virsh", "list", "--all", "--name"],
        capture_output=True,
    )
    all_machine_names_bytes = process_result.stdout.strip()
    if not all_machine_names_bytes:
        print("No machine.")

    all_machine_names = all_machine_names_bytes.decode().split("\n")

    for machine_name in machine_names:
        if machine_name not in all_machine_names:
            print(f"{machine_name} does not exist.")
            continue

        process_result = subprocess.run(
            ["virsh", "snapshot-list", "--domain", machine_name, "--name"],
            capture_output=True,
        )
        snapshot_names_bytes = process_result.stdout.strip()
        if snapshot_names_bytes:
            snapshot_names = snapshot_names_bytes.decode().split("\n")
            for snapshot_name in snapshot_names:
                subprocess.run(
                    [
                        "virsh",
                        "snapshot-delete",
                        "--domain",
                        machine_name,
                        "--snapshotname",
                        snapshot_name,
                    ]
                )

        machine_xml = subprocess.run(
            ["virsh", "dumpxml", machine_name], capture_output=True
        )
        machine_doc = parseString(machine_xml.stdout)
        disk_list = machine_doc.documentElement.getElementsByTagName("devices")[
            0
        ].getElementsByTagName("disk")
        disk_path_list = []
        for disk in disk_list:
            device = disk.getAttribute("device")
            if device == "disk":
                disk_path = disk.getElementsByTagName("source")[0].getAttribute("file")
                disk_path_list.append(disk_path)

        subprocess.run(
            ["virsh", "undefine", machine_name, "--storage", ",".join(disk_path_list)]
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
        if name in machine_names:
            parent = host.parentNode
            parent.removeChild(host)
            break

    with tempfile.NamedTemporaryFile(mode="w") as temp_file:
        network_doc.writexml(temp_file)
        temp_file.flush()

        # update network
        subprocess.run(["virsh", "net-define", temp_file.name])

        print("Network defined, restarting it")
        subprocess.run(["virsh", "net-destroy", "hostonly"])
        subprocess.run(["virsh", "net-start", "hostonly"])


def print_usage():
    script_path = sys.argv[0]
    print("usage:")
    print(f"    python {script_path} <machine_names>")
    print("example:")
    print(f"    python {script_path} win7-2 win7-3")


def main():
    args = sys.argv
    arg_num = len(args) - 1
    if arg_num == 0:
        print_usage()
        return

    machine_names = args[1:]
    delete_machines(machine_names)


if __name__ == "__main__":
    main()
