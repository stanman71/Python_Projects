##  vLab_Python

This code can modify the configuration on Juniper devices and build topologies in VMware


### Features

- Get configuration
- Set basic configuration
- Delete basic configuaration
- Build complete topologies (by using Juniper vMX templates)

------------
------------


### Deviceconnection

The device you want to connect with:

```
Juniper_MOD("<IP>", "<user>", "<password>", "telnet", "23")
Juniper_MOD("172.18.10.90", "netconf", "Juniper", "telnet", "23")

```

------------
------------

### Get Configuration

Specify in ```main.py``` the part of the configuration that you want to have displayed

- "" (complete configuration)

- hostname | host-name

- router-id | id

- protocol | protocols | ospf | isis | bgp | bfd | mpls | stp | ldp | rsvp | lldp 

- interface | interfaces | ge-0/0/0-9 | lo0 | fxp0

- policy | policies | my-policy-name

- firewall | firewalls

------------
------------

### Delete Configuration

Specify in quotes and keyword delete the part of the configuration that you want to delete


- delete hostname | delete host-name

- delete router-id | delete id

- delete ge-0/0/0-9 | delete fxp0 | delete lo0

- delete ospf | isis | bgp | bfd | mpls | stp | ldp | rsvp | lldp

- delete "policy-name"

- delete "firewall-role"

```
router_01.del_conf("delete ge-0/0/0")
router_01.del_conf("delete ospf")

```
------------
------------

### Set Configuration


Upload configuration from an external file

```
router_01.set_conf("./my-junos-config.conf")

```

#### Example Config

my-junos-config.conf

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

### Create Topologies

- Build a complete custom topology in VMware by using a YMAL-file

- Creates ressouce pool, virtual maschines and all network connections

- Need Juniper vMX templates (control / forwarding plane)

- Configuration upload on each virtual maschine


------------



#### Example Topology

test.yaml

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


#### Template Config

- Need a default management connection

template.conf

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
