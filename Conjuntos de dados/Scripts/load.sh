#!/bin/bash

while true
do
wget http://10.0.0.20:80/Catalogo2023.pdf -P /tmp
wget http://10.0.0.20:80/OfficeSetup.exe -P /tmp
sleep 5
done

