# CloudFlare DNS Records Updater

## Pre
Create `A` records as bellow in Zone `YOURDOMAIN.COM` in CloudFlare DNS admin console:

```
mcimain.YOURDOMAIN.COM.	60	IN	A	170.114.45.252 ; MCI Main
rtlmain.YOURDOMAIN.COM.	60	IN	A	191.101.251.250 ; RTL Main
astmain.YOURDOMAIN.COM.	60	IN	A	203.23.103.248 ; AST Main
ircmain.YOURDOMAIN.COM.	60	IN	A	45.85.118.241 ; IRC Main
shtmain.YOURDOMAIN.COM.	60	IN	A	188.42.88.194 ; SHT Main
mkbmain.YOURDOMAIN.COM.	60	IN	A	80.94.83.29 ; MKB Main
mbtmain.YOURDOMAIN.COM.	60	IN	A	185.201.139.68 ; MBT Main
ztlmain.YOURDOMAIN.COM.	60	IN	A	185.109.21.183 ; ZTL Main
prsmain.YOURDOMAIN.COM.	60	IN	A	45.131.208.227 ; PRS Main
hwbmain.YOURDOMAIN.COM.	60	IN	A	104.254.140.11 ; HWB Main
```
## Install
pip install -r .\requirements.txt

Carear `.env` file like bellow:

```
EMAIL='example@exmaple.com'
KEY='YOURE_CLOUD_FLARE_API_KEY'
```

## Usage
```
python app.py [-V|--version] [-h|--help] [-p|--printzones] [-u|--url remote-ip-list-url] [-z|--zonename CloudFlare-zone-name]
```
