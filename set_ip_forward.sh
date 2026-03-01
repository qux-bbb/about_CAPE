#!/bin/bash

current=$(cat /proc/sys/net/ipv4/ip_forward)
echo "ip_forward 当前值为: $current"

if [ "$current" -eq 0 ]; then
    if [ "$(id -u)" -ne 0 ]; then
        echo "修改值需要 root 权限"
        exit 1
    fi
    echo 1 > /proc/sys/net/ipv4/ip_forward
    echo "已从 0 修改为 1"
else
    echo "无需修改"
fi