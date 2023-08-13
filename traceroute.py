import subprocess
import re
import socket 

def get_ip_address(hostname):
    try:
       ip = socket.inet_pton(socket.AF_INET, hostname)
       return hostname
    except:
        try:
          ip = socket.inet_pton(socket.AF_INET6, hostname)
          return hostname
        except:
            try:
                ip_address = socket.gethostbyname(hostname)
                return ip_address 
            except socket.gaierror:
                return "Enter Correct Hostname"

def parseCommand(s):
    time_pattern = r'\(([\d.]+)s\) ICMP'
    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    time_after_send = re.findall(time_pattern, s)
    ip_received = re.findall(ip_pattern, s)
    if (len(time_after_send)<6):
        return -1,-1
    else:
        return time_after_send, ip_received

def traceroute(target_host):
    target_host=get_ip_address(target_host)
    print("Tracing route to " + "["+target_host+"]"+' over a maximum of 30 hops:')
    for i in range(1,31):
        try:
            ping_cmd = 'nping -c 3 --ttl '+ str(i)+' ' + target_host
            result = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            # print("Command output:", result.stdout)
            time,ip=parseCommand(result.stdout)
            if (time!=-1 and ip!=-1):
                taken=[0,0,0]
                ip_address=ip[2]
                j=0
                while (j<len(time)):
                    if (j==0):
                        taken[0]=int((float(time[j+1])-float(time[j]))*1000)
                    if (j==2):
                        taken[1]=int((float(time[j+1])-float(time[j]))*1000)
                    if (j==4):
                        taken[2]=int((float(time[j+1])-float(time[j]))*1000)
                    j+=2
                s1=""
                s1+=str(i)
                s1+=' '
                for c in taken:
                        s1+=str(c)
                        s1+='ms '
                s1+=' '
                s1+=ip_address
                print(s1)
                if (ip_address==target_host):
                    print('\n')
                    print('Trace Complete')
                    break 
            else:
                print(str(i)+"   *    *    * ")
        except subprocess.CalledProcessError as e:
            print("Error executing command:", e)
            print("Command output (stderr):", e.stderr)