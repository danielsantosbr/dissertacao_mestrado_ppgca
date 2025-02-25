#!/bin/bash
n=6     # number of switches
for i in {1..2000}
do
    for ((j = 1; j <= n; j++))
    do
        echo "Inspeção $i <--> Switch s$j"
        # Extrai 5 características do tráfego em arquivo temporário para posterior processamento
        sudo ovs-ofctl dump-flows s$j > data/raw
        grep "nw_src" data/raw > data/flowentries.csv
        packets=$(awk -F "," '{split($4,a,"="); print a[2]","}' data/flowentries.csv)
        bytes=$(awk -F "," '{split($5,b,"="); print b[2]","}' data/flowentries.csv)
        ipsrc=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($11,d,"="); print d[2]","}')
        ipdst=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($12,d,"="); print d[2]","}')
        port=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($8,d,"="); print d[2]","}')
        
        # Verifica se há tráfego
        if test -z "$packets" || test -z "$bytes" || test -z "$ipsrc" || test -z "$ipdst" || test -z "$port"
        then
            state=0
        else
            echo "$packets" > data/packets.csv
            echo "$bytes" > data/bytes.csv
            echo "$ipsrc" > data/ipsrc.csv
            echo "$ipdst" > data/ipdst.csv
            echo "$port" > data/port.csv
            
            python3 computeTuples.py # Aplica as fórmulas relacionadas no trabalho (SSIP, SSP, SDFB, SDFP, SFE, RPF) e as grava no arquivo extract.csv (ou realtime.csv, caso o sistema já tenha sido treinado)
            python3 inspector.py
            state=$(awk '{print $0;}' .result)
        fi

        if [ $state -eq 1 ];
        then
            echo "DETECTADO ATAQUE NA REDE <--> SWITCH S$j"
            # AÇÃO DE MITIGAÇÃO
        fi
    done
    sleep 3
done