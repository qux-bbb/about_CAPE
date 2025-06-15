# win7虚机相关

安装win7：  
```r
下载镜像(win7旗舰版)
https://msdn.itellyou.cn
ed2k://|file|cn_windows_7_ultimate_with_sp1_x64_dvd_u_677408.iso|3420557312|B58548681854236C7939003B583A8078|/

安装虚机，内存建议设置4G，硬盘建议设置128G，网络可以暂时用NAT
如果有问题，可以参照该链接安装：
https://www.doomedraven.com/2020/04/how-to-create-virtual-machine-with-virt.html

安装后关机移除镜像，开机设置初始快照
```

配置win7：  
```r
根据系统版本下载安装补丁，安装后需要重启
KB4474419 SHA-2代码签名补丁
https://www.catalog.update.microsoft.com/Search.aspx?q=4474419
https://catalog.s.download.windowsupdate.com/c/msdownload/update/software/secu/2019/09/windows6.1-kb4474419-v3-x64_b5614c6cea5cb4e198717789633dca16308ef79c.msu

下载安装python32位
https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe

配置agent.py
https://capev2.readthedocs.io/en/latest/installation/guest/agent.html#installing-the-agent  
路径: /opt/CAPEv2/agent/agent.py
将agent.py改名为 agent.pyw, 放入该文件夹: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`

安装python依赖，高版本Pillow在win7装不上，所以指定一个低版本的
pip install Pillow==7.2.0
pip install pywintrace

------------------------------------------------------可选：安装.net_start
下载安装.net4.0
https://www.microsoft.com/en-US/Download/confirmation.aspx?id=17718
------------------------------------------------------可选：安装.net_end

------------------------------------------------------可选：安装Office_start
下载安装7zip
https://7-zip.org/

迅雷下载解压安装office2010
https://msdn.itellyou.cn/
应用程序 ->  Office 2010 -> 中文-简体 -> Office Professional Plus 2010 With SP1 VOL (x64) - (Chinese-Simplified)
文件名: SW_DVD5_Office_Professional_Plus_2010w_SP1_64Bit_ChnSimp_CORE_MLF_X17-76742.iso
SHA1: 9D97B220739161CFF3147E169B702A056A6C7F51
文件大小: 1.5GB
ed2k://|file|SW_DVD5_Office_Professional_Plus_2010w_SP1_64Bit_ChnSimp_CORE_MLF_X17-76742.iso|1612515328|032320121E0EE36D8F0C32EC89CA0AB9|/

下载执行HEU_KMS_Activator激活Windows和Office，仅供研究使用，24小时内删除
https://github.com/zbezj/HEU_KMS_Activator

设置Office
左下角 Windows徽标 -> 所有程序 -> Microsoft Office -> Microsoft Word 2010，弹出的"帮助保护和改进 Microsoft Office"，选择"请勿更改"
------------------------------------------------------可选：安装Office_end

关闭屏幕保护程序：
控制面板 -> 外观和个性化 -> 更改屏幕保护程序，选择"无"，确定即可

设置密码：
控制面板 -> 用户账户和家庭安全 -> 用户账户 -> 为您的账户创建密码

设置自动登录：
Win+R，输入"netplwiz"，回车，取消勾选"要使用本机，用户必须输入用户名和密码"，点击"应用"，输入密码生效

删除密码：
控制面板 -> 用户账户和家庭安全 -> 用户账户 -> 删除密码

禁止win7一些默认行为和office保护的脚本，下载后使用管理员权限运行，注意观察输出确认是否正常执行
https://github.com/kevoreilly/CAPEv2/blob/master/installer/disable_win7noise.bat

virt-manager中创建hostonly网络，模式为"Isolated"，将虚机网络切换为hostonly

使用machine_hostonly_net_ip.py绑定虚机在hostonly网络的ip：
usage:   sudo python3 ./machine_hostonly_net_ip.py set <machine_name> <ip>
exmaple: sudo python3 ./machine_hostonly_net_ip.py set win7 192.168.100.131

虚机中设置ipv4网络为"自动获得IP地址"，在"高级"设置中添加默认网关，如: 192.168.100.1
注意手动设置DNS  

重启虚机，命令行确认虚机ip为绑定的ip，任务管理器确认有pythonw.exe进程
如果有问题(无法获取ip)，尝试关机之后在虚机的网络设置页面将"Device model"改成"Hypervisor default"，启动后重新设置ipv4网络试试

创建快照
```

切换为cape用户，修改配置文件，在 `/opt/CAPEv2/custom/conf/kvm.conf` 配置文件中设置虚机相应信息，注意 machines 和 interface 设置正确的值，示例如下(tags和arch不重要)：  
```r
[win7-1]
label = win7-1
platform = windows
ip = 192.168.100.132                                                            
tags = x64 
snapshot = snapshot_new
arch = x64
```
配置生效需要重启 cape 和 cape-web 服务，可以等所有配置修改后重启服务  