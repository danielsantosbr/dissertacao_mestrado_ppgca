#!/bin/bash
while true;
do
    packets=$(shuf -i 1-100 -n 1)
    port=$(shuf -i 1-1024 -n 1)
    bytes=$(shuf -i 64-128 -n 1)
    delay=$(shuf -i 1-5 -n 1)
    ip=$(shuf -i 1-20 -n 1)
    proto=$(shuf -i 1-2 -n 1)
    if [ $proto -eq 1 ]; 
	then
		sudo hping3 -c $packets -d $bytes 10.0.0.$ip
    	else
        	sudo hping3 -$proto -c $packets -d $bytes -p $port 10.0.0.$ip
	fi
    sleep $delay
done
