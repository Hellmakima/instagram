in wsl do git clone
then we need to copy and edit the .env file

put the right mongo url mongodb://172.17.192.1:27017

add new rule to the firewall
allow port 27017 TCP

next is `C:\Program Files\MongoDB\Server\<ver>\bin\mongod.cfg`

```
net:
  port: 27017
  bindIp: 127.0.0.1,172.17.192.1
```

restart mongodb

```bash
net stop MongoDB
net start MongoDB
```

here `172.17.192.1` is the ip of wsl.

reference:

```bash
~ $ ipconfig

Windows IP Configuration


Ethernet adapter Ethernet 2:

   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::ab7f:e71a:4b04:d76%9
   IPv4 Address. . . . . . . . . . . : 192.168.56.1
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . :

Wireless LAN adapter Local Area Connection* 1:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

Wireless LAN adapter Local Area Connection* 2:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

Wireless LAN adapter Wi-Fi:

   Connection-specific DNS Suffix  . :
   IPv6 Address. . . . . . . . . . . : 2401:4900:ad2d:7e3:4b30:2dd8:97e8:400a
   Temporary IPv6 Address. . . . . . : 2401:4900:ad2d:7e3:7408:6b4d:4b71:b09d
   Link-local IPv6 Address . . . . . : fe80::2bd4:8e91:6c30:10eb%11
   IPv4 Address. . . . . . . . . . . : 10.236.107.229
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : fe80::d896:c1ff:fe08:489a%11
                                       10.236.107.131

Ethernet adapter vEthernet (WSL (Hyper-V firewall)):

   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::26f8:2c63:932d:7598%55
   IPv4 Address. . . . . . . . . . . : 172.17.192.1
   Subnet Mask . . . . . . . . . . . : 255.255.240.0
   Default Gateway . . . . . . . . . :
~ $ net stop MongoDB
System error 5 has occurred.

Access is denied.

~ $ net start MongoDBnetstat -ano | findstr 27017^C
~ $ netstat -ano | findstr 27017
  TCP    127.0.0.1:27017        0.0.0.0:0              LISTENING       24628
  TCP    172.17.192.1:27017     0.0.0.0:0              LISTENING       24628
~ $
```

## UV

curl -LsSf https://astral.sh/uv/install.sh | sh
