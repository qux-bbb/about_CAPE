# ubuntu虚机相关

```r
安装虚机，内存建议设置4G，硬盘建议设置128G，网络可以暂时用NAT
之后的步骤建议ssh连接操作，方便输入
设置root密码
  sudo passwd root
设置ssh允许root用户使用密码登陆
  sudo vim /etc/ssh/sshd_config.d/50-cloud-init.conf
  增加内容
    PasswordAuthentication yes
    PermitRootLogin yes
安装后关机移除镜像，开机设置初始快照

在host复制agent到guest
scp /opt/CAPEv2/agent/agent.py root@192.168.122.84:/root/

设置agent自启动
crontab -e
@reboot python3 /root/agent.py

apt update
# 为了避免这个警告: WARNING:root:Cannot call Open vSwitch: ovsdb-server.service is not running.
apt install openvswitch-common openvswitch-switch
# 安装analyzer依赖
apt install python3-pip
pip3 install pyinotify
pip3 install Pillow

用netplan配置ubuntu的ip
cp /etc/netplan/00-installer-config.yaml /etc/netplan/00-installer-config.yaml.bak
vim /etc/netplan/00-installer-config.yaml
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp1s0:
      dhcp4: true
      routes:
        - to: default
          via: 192.168.100.1
      nameservers:
        addresses: [114.114.114.114, 8.8.8.8]
  version: 2

netplan apply

virt-manager中创建hostonly网络，模式为"Isolated"，将虚机网络切换为hostonly

使用machine_hostonly_net_ip.py绑定虚机在hostonly网络的ip：
usage:   sudo python3 ./machine_hostonly_net_ip.py set <machine_name> <ip>
exmaple: sudo python3 ./machine_hostonly_net_ip.py set ubuntu22.04 192.168.100.132

重启，确认ip已修改，进程中有agent.py
ip -br a | grep 192.168.100.132
ps -ef | grep agent.py

建快照

在 /opt/CAPEv2/custom/conf/kvm.conf 配置文件中设置虚机相应信息
在 /opt/CAPEv2/custom/conf/web.conf 配置文件中启用linux文件分析

暂时看起来只能监控文件操作和网络操作，没有细粒度的api操作

参考链接：
https://stackoverflow.com/questions/77352932/ovsdb-server-service-from-no-where
https://docs.openvswitch.org/en/latest/intro/install/distributions/#debian-ubuntu
```
