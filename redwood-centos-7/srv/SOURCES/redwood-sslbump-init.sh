#!/usr/bin/env bash 

DOMAIN="ngtech.co.il"
COUNTRYCODE="IL"
STATE="Shomron"
REGION="Center"
ORGINZATION="NgTech LTD"
CERTUUID=`uuidgen | awk 'BEGIN { FS="-"}; {print $1}'`
SUBJECDETAILS=`echo -n "/C=$COUNTRYCODE/ST=$STATE/L=$REGION/O=$ORGINAZATION/CN=px-$CERTUUID.$DOMAIN"`
source /etc/sysconfig/redwood
echo $SUBJECDETAILS
if [ -d "/etc/redwood/ssl-cert" ];then
  echo "Abort since /etc/redwood/ssl-cert exists"
  exit 1
else
  mkdir -p /etc/redwood/ssl-cert
  openssl req -new -newkey rsa:2048 -sha256 -days 365 -nodes -x509 -subj "$SUBJECDETAILS" \
    -extensions v3_ca -keyout /etc/redwood/ssl-cert/myCAkey.pem -out /etc/redwood/ssl-cert/myCAcert.pem
fi

egrep "^(tls-cert\ |tls-key\ )" /etc/redwood/redwood.conf 
if [ "$?" -eq "1" ];then
  echo "" >> /etc/redwood/redwood.conf
  echo "# ssl-bump tls key and certificate" >> /etc/redwood/redwood.conf
  echo "tls-cert /etc/redwood/ssl-cert/myCAcert.pem" >> /etc/redwood/redwood.conf
  echo "tls-key /etc/redwood/ssl-cert/myCAkey.pem" >> /etc/redwood/redwood.conf
  cat /etc/redwood/sslbump-defaultbypass-acls.conf /etc/redwood/acls.conf > /tmp/$CERTUUID-acls.conf
  cp /etc/redwood/acls.conf /etc/redwood/acls.conf.backup
  cp /tmp/$CERTUUID-acls.conf /etc/redwood/acls.conf
  systemctl restart redwood
else
  echo "some sslbump settings are already in-place"
fi

if [ -e  "/etc/redwood/ssl-cert/myCAcert.pem" ];then
	cp -v /etc/redwood/ssl-cert/myCAcert.pem /var/redwood/static/
	echo "/etc/redwood/ssl-cert/myCAcert.pem was copied to /var/redwood/static/"
	openssl x509 -outform der -in /etc/redwood/ssl-cert/myCAcert.pem -out /var/redwood/static/myCAcert.der
	echo "/etc/redwood/ssl-cert/myCAcert.pem was converted to der and now at => /var/redwood/static/myCAcert.der"
fi

