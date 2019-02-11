##  vLab_Python

This project was made to modify the configuration of Juniper devices and build topologies in VMware


### Features

- get the current configuration
- update the configuration by using a prepared config file
- delete selected parts of the configuration
- build complete virtual topologies

------------

##### start ```main.py``` to use every feature

You will find more examples there

------------
------------
------------

### First Step: Connect to the Juniper device

Open ```main.py``` and specify the device you want to connect with in this format:

```
Juniper_MOD("<IP>", "<user>", "<password>", "telnet", "23")
```

------------

#### Example:

```
Juniper_MOD("172.18.10.90", "netconf", "Juniper", "telnet", "23")
```
------------
------------
------------

### Get Configuration

Specify the part of the configuration that you want to have displayed:

- "" (complete configuration)

- hostname | host-name

- router-id | id

- protocol | protocols | ospf | isis | bgp | bfd | mpls | stp | ldp | rsvp | lldp 

- interface | interfaces | ge-0/0/0-9 | lo0 | fxp0

- policy | policies | my-policy-name

- firewall | firewalls

------------

#### Example:

```
router_01.GET_conf("")
router_01.GET_conf("firewall")
```
------------
------------
------------

### Update Configuration


Upload configuration from an external file

------------

#### Example:

```
router_01.set_conf("./my-junos-config.conf")
```

###### Config-File: my-junos-config.conf 
###### (default folder: CONFIG)

```
    interfaces {

        ge-0/0/0 {
            unit 0 {
                family inet {
                    address 7.43.4.2/24;
                }
            }
        }

        lo0 {
            unit 0 {
                family inet {
                    address 1.1.1.1/32;
                }
            }
        }
    }

    protocols {
        ospf {        
            area 0.0.0.0 {
                interface all;
            }
        }
    }
```

------------
------------
------------

### Delete Configuration

Specify in quotes and keyword delete the part of the configuration that you want to delete:


- delete hostname | delete host-name

- delete router-id | delete id

- delete ge-0/0/0-9 | delete fxp0 | delete lo0

- delete ospf | isis | bgp | bfd | mpls | stp | ldp | rsvp | lldp

- delete "policy-name"

- delete "firewall-role"

------------

#### Example:

```
router_01.del_conf("delete ge-0/0/0")
router_01.del_conf("delete ospf")
```

------------
------------
------------
------------
------------

### Create Topologies

- Build a complete custom topology in VMware by using a YMAL-file

- Creates ressouce pool, virtual maschines and all network connections

- Upload a new configuration automatically on each virtual maschine and change the management IPs

- Need Juniper vMX templates >>> more informations at the end of this document

------------

#### Example:

```
Create_MAIN.Create("./TOPOLOGY/Test_01.yml")
```

- The configuration settings of your VMware environment (vcenter_ip, username, password...) are in the connection section of the ymal file

- All names of the new topology will be automatically generated and got the choosen project_name as prefix

###### Topology-File: test.yaml 
###### (default folder: TOPOLOGY)

```
project_name: Test_01

connection:
    vcenter_ip:    
    username:      
    password:      
    host_name:     
    data_center:   
    datastore:     
    vm_folder:     

default_settings_TEMPLATE:
    template_mgmt_IP:   "192.18.10.100"
    default_username:   "netconf"
    default_password:   "Netconf"
    external_interface: "external_network"

devices:
    - name: R01
      type: vMX
      version: 18.2R1.9
      mgmt_ip: 172.18.10.101/24
      mgmt_ip_gw: 172.18.10.1 # gateway
      network: 
          - R01-R03 # ge-0/0/0
          - R01-R02 # ge-0/0/1

    - name: R02
      type: vMX
      version: 18.2R1.9
      mgmt_ip: 172.18.10.102/24
      mgmt_ip_gw: 172.18.10.1 # gateway
      network: 
          - R02-R03 # ge-0/0/0
          - R01-R02 # ge-0/0/1

    - name: R03
      type: vMX
      version: 18.2R1.9
      mgmt_ip: 172.18.10.103/24
      mgmt_ip_gw: 172.18.10.1 # gateway
      network: 
          - R01-R03 # ge-0/0/0
          - R02-R03 # ge-0/0/1
```

------------

#### Create template VMs


- The template VMs are created by using the Juniper ova-files (https://support.juniper.net/support/downloads/?p=vmxeval#sw)

- VM-Names >>> controlPlane: "TEMPLATE_vCP_" + Version /// forwardingPlane: "TEMPLATE_vFPC_" + Version 

- Delete all network connections on both machines 

- Set on the forwardingPlane the CPU-cores to 3 and the RAM to 3 GB

- The template controlPlane needs a default configuration (temporary management IP: 172.18.10.85/24)

###### Template Config File: template.conf 
###### (folder: CONFIG)

```
system {
    login {
        user netconf {
            uid 2001;
            class super-user;
            authentication {
                encryted-password "" 
            }
        }
    }
    host-name TEMPLATE;
    services {
        ssh {
            root-login allow;
        }
        telnet {
            connection-limit 5;
        }
        netconf {
            ssh;
        }
    }
}

interfaces {
    fxp0 {
        unit 0 {
            family inet {
                address 172.18.10.85/24;
            }
        }
    }
}

routing-options {
    static {
        route 0.0.0.0/0 next-hop 172.18.10.1;
    }
}
```
