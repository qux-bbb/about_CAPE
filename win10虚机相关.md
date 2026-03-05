# win10虚机相关

```r
安装虚机，内存建议设置4G，硬盘建议设置128G，网络可以暂时用NAT
(这里内存设置4G是因为本机内存只有16G，设置太大内存如8G会运行很慢导致超时错误，如果内存足够大可以设置8G)

管理员权限打开命令行，激活Administrator
net user Administrator /active:yes

关机移除镜像
开机选择帐户Administrator登陆
设置初始快照

下载安装python32位
https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe

配置agent.py
https://capev2.readthedocs.io/en/latest/installation/guest/agent.html#installing-the-agent  
路径: /opt/CAPEv2/agent/agent.py
将agent.py改名为 agent.pyw, 放入该文件夹: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`

安装python依赖
pip3 install pillow pywintrace

管理员权限打开powershell命令行，设置允许执行pwoershell脚本
Set-ExecutionPolicy Unrestricted
使用powershell脚本禁用Windows上一些不需要的功能
下载脚本前先关闭Defender，避免被隔离
https://raw.githubusercontent.com/kevoreilly/CAPEv2/refs/heads/master/installer/win10_disabler.ps1

使用Windows Update Blocker 禁用虚机windows更新
https://www.sordum.org/

关闭传递优化

virt-manager中创建hostonly网络，模式为"Isolated"，将虚机网络切换为hostonly
等待出现hostonly网络的ip，如: 192.168.100.133
如果没出现尝试取消勾选“Link state”，应用后再勾选“Link state”应用看看
在虚机中手动设置静态网络，包括
ip(192.168.100.133)
子网掩码(255.255.255.0)
DNS地址(如114.114.114.114)
默认网关(192.168.100.1)
启用“设为按流量计费的连接”

如果后续需要批量复制虚机，可以这样设置网络：
使用machine_hostonly_net_ip.py绑定虚机在hostonly网络的ip：
usage:   sudo python3 ./machine_hostonly_net_ip.py set <machine_name> <ip>
exmaple: sudo python3 ./machine_hostonly_net_ip.py set win10 192.168.100.133
虚机中设置ipv4网络为"自动获得IP地址"
手动设置DNS，如: 114.114.114.114
在"高级"设置中添加默认网关，如: 192.168.100.1

重启虚机，命令行确认虚机ip为设置或绑定的ip，DNS正确，确认有pythonw.exe进程
ipconfig /all
tasklist | findstr pythonw.exe
如果有问题(无法获取ip)，尝试关机之后在虚机的网络设置页面将"Device model"改成"Hypervisor default"，启动后重新设置ipv4网络试试

创建快照

切换为cape用户，修改配置文件 /opt/CAPEv2/custom/conf/kvm.conf
设置虚机相应信息，注意 machines 和 interface 设置正确的值
示例如下(tags和arch不重要)：  
[win10-1]
label = win10-1
platform = windows
ip = 192.168.100.129                                               
tags = x64 
snapshot = snapshot_new
arch = x64
配置生效需要重启 cape 和 cape-web 服务，可以等所有配置修改后重启服务  
```
