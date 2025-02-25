import csv, numpy as np
import math

interval = 3
## SSIP
with open("data/ipsrc.csv", "r") as file:
    reader = csv.reader(file)
    data = [row[0] for row in reader]

# Número de IP's de origens únicos
unique_ips = len(set(data))

# Speed of source IPs (SSIP)
ssip = unique_ips / interval
print("SSIP:", ssip, "IPs/s")

## SSP
with open("data/port.csv", "r") as file:
    reader = csv.reader(file)
    data = [row[0] for row in reader]

# Número de portas de origens distintas
unique_ports = len(set(data))

# Speed of source IPs (SSP)
ssp = unique_ports / interval
print("SSP:", ssp, "Ports/s")

## SDFP
def read_packets_from_file():
    packets = []
    with open("data/packets.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            packets.append(int(row[0]))
    return packets

def calculate_mean_packets(packets):
    return sum(packets) / len(packets)

def calculate_standard_deviation_of_packets(packets, mean_packets):
    sum_of_squared_differences = 0
    for packet in packets:
        sum_of_squared_differences += (packet - mean_packets) ** 2
    variance = sum_of_squared_differences / len(packets)
    return math.sqrt(variance)

if __name__ == "__main__":
    packets = read_packets_from_file()
    mean_packets = calculate_mean_packets(packets)
    sdfp = calculate_standard_deviation_of_packets(packets, mean_packets)
    print("SDFP:", sdfp, "Packets")

## SDFB
# Realiza a leitura de dados de bytes do arquivo
bytes_data = []
with open("data/bytes.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        bytes_data.append(int(row[0]))

# Calcula a média
n = len(bytes_data)
mean_bytes = sum(bytes_data) / n

# Calcula a soma dos quadrados da diferença da média
sum_of_squares = sum([(bytes_i - mean_bytes)**2 for bytes_i in bytes_data])

# Calcula o desvio padrão dos bytes (SDFB)
sdfb = math.sqrt(sum_of_squares / n)

print("SDFB:", sdfb, "Bytes")

## SFE
# Faz a leitura dos fluxos de dados do arquivo tabulado
flow_entries = []
with open('data/flowentries.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        entry = row[0]
        n_packets = sum(1 for row in reader)
        flow_entries.append(n_packets)

# Calcula o número de fluxos de entrada e a velocidade desses fluxos (SFE)
n = len(flow_entries)
flow_entries_array = np.array(flow_entries)
mean_flow_entries = np.mean(flow_entries_array)
sfe = mean_flow_entries / interval

print("SFE:", sfe, "flow entries per second")

## RPF
with open('data/ipsrc.csv') as src, open('data/ipdst.csv') as dst:
    src_ips = [ip.strip() for ip in src.readlines()]
    dst_ips = [ip.strip() for ip in dst.readlines()]
    interactive_flow_entries = len(set(src_ips) & set(dst_ips))
    total_flow_entries = len(src_ips)
    rpf = interactive_flow_entries / total_flow_entries
    print("RPF:", rpf)

headers = ["SSIP", "SSP", "SDFP", "SDFB", "SFE", "RPF"]
features = [ssip, ssp, sdfp, sdfb, sfe, rpf]

with open('realtime.csv', 'w') as f:
   cursor = csv.writer(f, delimiter=",")
   cursor.writerow(headers)
   cursor.writerow(features)

with open('extract.csv', 'a') as f:
    cursor = csv.writer(f, delimiter=",")
    cursor.writerow(features)

#import os

#directory = 'data/'

#for filename in os.listdir(directory):
#    if os.path.isfile(os.path.join(directory, filename)):
#        with open(os.path.join(directory, filename), 'w') as file:
#            file.write('')
