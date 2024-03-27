import json

from datetime import datetime
now = datetime.now()
from math import floor

# Function to open and read a JSON file
def open_file(_file) :
	# Opening the JSON file in read mode
	f = open(_file)
	# Parsing the JSON file into a Python dictionary
	data = json.load(f)
    # Closing the file to free up resources
	f.close()
	return data


filename="config.json"
# Loading the JSON content into a dictionary
json_object = open_file(filename)


def write_file() :
    script="!\n\n!\n"
    script+="version 15.2\n"
    script+="service timestamps debug datetime msec\n"
    script+="service timestamps log datetime msec\n"
    script+="!\nhostname "+r['hostname']+"\n!\n"
    script+="boot-start-marker\n"
    script+="boot-end-marker\n!\n!\n!\n"
    script+="no aaa new-model\n"
    script+="no ip icmp rate-limit unreachable\n"
    script+="ip cef\n!\n"

    # VRF configuration if applicable
    if r['vrf_apply']!=0:
        for x in r['vrf']:
            script+="ip vrf "+x['name']+"\n"
            script+=" rd "+str(r['bgp']['AS_number'])+":"+str(x['id'])+"\n"
            script+=" route-target export "+str(r['bgp']['AS_number'])+":"+str(x['id'])+"\n"
            script+=" route-target import "+str(r['bgp']['AS_number'])+":"+str(x['id'])+"\n"
            script+="!\n"

    script+="!\n!\n!\n!\n!\n"
    script+="no ip domain lookup\n"
    script+="no ipv6 cef\n!\n!\n"
    script+="multilink bundle-name authenticated\n"
    script+="!\n!\n!\n!\n!\n!\n!\n!\n!\n"
    script+="ip tcp synwait-time 5\n"
    script+="!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n"
    
    # Loop through each interface in the router's configuration
    for x in r['interfaces']:
        # Add the interface configuration
        script+="interface "+str(x['interface_name'])+"\n"
        
        if str(x['interface_name'])=="Loopback0":
            script+=" ip address "+str(r['id'])+"."+str(r['id'])+"."+str(r['id'])+"."+str(r['id'])+" 255.255.255.255\n"
            
        else:
            # Configuration for interfaces connecting PE to CE
            if x['link']<10 and r['id']>100 : 
                if x['vrf_apply']!=0:
                    script+=" ip vrf forwarding "
                    for y in r['vrf']:
                        if y['id'] == x['vrf_id']:
                            script+=y['name']+"\n"
                script+=" ip address 192.168."+str(x['link'])+".1 255.255.255.0\n"
                script+=" negotiation auto\n"

            # Configuration for interfaces connecting PE to P      
            elif r['id']>100 and x['link']>10 and x['link']<20 :
                script+=" ip address 10.10."+str(r['id'])+".1 255.255.255.252\n"
                script+="ip ospf 1 area 0\n"
                script+=" negotiation auto\n"
                script+=" mpls ip\n"

            # Configuration for interfaces connecting P to PE
            elif x['link']>100 and r['id']>10 and r['id']<20 :
                script+=" ip address 10.10."+str(x['link'])+".2 255.255.255.252\n"
                script+="ip ospf 1 area 0\n"
                script+=" negotiation auto\n"
                script+=" mpls ip\n"
            
            # Configuration for interfaces connecting P to P
            elif x['link']>10 and x['link']<20 and r['id']>10 and r['id']<20 :
                if x['link']<r['id']:
                    script+=" ip address 10.10."+str(x['link'])+".2 255.255.255.252\n"
                else:
                    script+=" ip address 10.10."+str(r['id'])+".1 255.255.255.252\n"
                script+="ip ospf 1 area 0\n"
                script+=" negotiation auto\n"
                script+=" mpls ip\n"
            
            # Configuration for interfaces connecting CE to PE
            elif r['id']<10 and x['link']>100 : 
                script+=" ip address 192.168."+str(r['id'])+".2 255.255.255.0\n"
                script+=" negotiation auto\n"
        script+="!\n"
    
    # Configuring OSPF for VRFs if VRF is applied. It redistributes BGP routes into OSPF within the VRF context,
    # and defines the network area for OSPF within each VRF. Additionally, it specifies OSPF networks for interfaces in the VRF.   

    
    
    # Check if OSPF is applied for the router        
    if r['ospf']['ospf_apply']!=0:
        # Configure OSPF with the router's OSPF process ID
        script+="router ospf "+str(r['ospf']['process_id'])+"\n"
        
        # Iterate through interfaces to configure OSPF networks
        for x in r['interfaces']:
            # If OSPF is applied to the interface, add network command
            if x['ospf_apply']!=0:
                # Configure loopback interface OSPF network
                if x['link']==r['id']:
                    script+=" network "+str(r['id'])+"."+str(r['id'])+"."+str(r['id'])+"."+str(r['id'])+" 0.0.0.0 area 0\n"
                # Configure OSPF network for PE connecting with P    
                elif r['id']>100 and x['link']>10 and x['link']<20 :
                    script+=" network 10.10."+str(r['id'])+".0 0.0.0.3 area 0\n"
                # Configure OSPF network for P connecting with PE    
                elif x['link']>100 and r['id']>10 and r['id']<20 :
                    script+=" network 10.10."+str(x['link'])+".0 0.0.0.3 area 0\n"
                # Configure OSPF network for CE connecting with PE
                elif x['link']>100 and r['id']<10 :
                    script+=" network 192.168."+str(r['id'])+".0 0.0.0.255 area 0\n"
                # Configure OSPF network for P connecting with P
                elif x['link']>10 and x['link']<20 and r['id']>10 and r['id']<20 :
                    if x['link']<r['id']:
                        script+= " network 10.10."+str(x['link'])+".0 0.0.0.3 area 0\n"
                    else:
                        script+=" network 10.10."+str(r['id'])+".0 0.0.0.3 area 0\n"

        #if r["role"]=="provider" or r["role"]=="provider_edge" :
            #script+=" mpls ldp autoconfig\n"

        script+="!\n"
        
    # Check if BGP is applied   
    if r['bgp']['bgp_apply']!=0 :
        script+="router bgp "+str(r['bgp']['AS_number'])+"\n"
        script+=" bgp log-neighbor-changes\n"
        script+=" no bgp default ipv4-unicast\n"
        if r['bgp']['AS_number'] == 5:
            script+=" neighbor "+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+" remote-as "+str(r['bgp']['AS_number'])+"\n"
            script+=" neighbor "+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+" update-source Loopback0\n"
        else:
            script+=" neighbor 192.168."+str(r['id'])+".1 remote-as 5\n"
            
            
        #####
        #script+="ip ospf 1 area 0\n"
        #####
        script+=" !\n"
        script+=" address-family ipv4\n"
        if r['bgp']['AS_number'] == 5:
            script+=" neighbor "+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id']) +" activate\n"
        else:
            script+="  neighbor 192.168."+str(r['id'])+".1 activate\n"
        script+=" exit-address-family\n"
        script+=" !\n"
        
        if r['bgp']['neighbor']['vpn_apply']!=0:
            script+=" address-family vpnv4\n"            
            script+="  neighbor "+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+" activate\n"
            script+="  neighbor "+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+"."+str(r['bgp']['neighbor']['id'])+" send-community extended\n"
            script+=" exit-address-family\n"
            
          
    # Apply VRF configuration if enabled   
    if r['vrf_apply']!=0:
        petit_compteur = 0
        for x in r['vrf']:
            script+=" !\n"
            script+=" address-family ipv4 vrf "+x['name']+"\n"
            
            script+="  neighbor 192.168."+str(r['interfaces'][petit_compteur]['link'])+".2 remote-as " + str(r['interfaces'][petit_compteur]['link'])+"\n"; 
            script+="  neighbor 192.168."+str(x['id'])+".2 activate\n"; 
            script+="  network 192.168."+str(r['interfaces'][petit_compteur]['link'])+".0\n"

            script+=" exit-address-family\n"
            petit_compteur +=1
           

    script+="!\n"
    script+="ip forward-protocol nd\n!\n!\n"
    script+="no ip http server\n"
    script+="no ip http secure-server\n!\n"
    script+="!\n!\n!\n!\ncontrol-plane\n!\n!\n"
    script+="line con 0\n"
    script+=" exec-timeout 0 0\n"
    script+=" privilege level 15\n"
    script+=" logging synchronous\n"
    script+=" stopbits 1\n"
    script+="line aux 0\n"
    script+=" exec-timeout 0 0\n"
    script+=" privilege level 15\n"
    script+=" logging synchronous\n"
    script+=" stopbits 1\n"
    script+="line vty 0 4\n"
    script+=" login\n!\n!\nend"
    return script		
		
  
petit_compteur = 1  	
for r in json_object['routers'] :
    
    # Generate a file name based on the router's hostname and create a text file
    finalname="i"+str(petit_compteur)+"_startup-config.cfg"
    petit_compteur+=1
    with open(finalname, "w") as output:
        output.write(write_file())
