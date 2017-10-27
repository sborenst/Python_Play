#!/usr/local/bin/python3.6
'''
This script is a first draft of json dictionary play
'''
import json

'''
ec2_hostvar_attributes is a list containing all the attributes
 that are going to be parsed from our json inventory input
'''
ec2_hostvar_attributes=[
"ec2_state",
"ec2_tag_AnsibleGroup",
"ec2_tag_internaldns",
"ec2_region",
"ec2_public_dns_name",
"ec2_private_ip_address",
"ec2_private_dns_name",
"ec2_placement",
"ec2_key_name",
"ec2_image_id",
"ansible_ssh_host"]

'''
group_identifier is a used to filter out all the hosts we want to
 parse in the script
group_identifier="tag_aws_cloudformation_stack_name_ocp_workshop_rhpds"

cloud_provider defines the cloud provider, this will effect which attributes
 will be used and collected from the json inventory input
cloud_provider="ec2"
verbose=2
'''

group_identifier="tag_aws_cloudformation_stack_name_ocp_workshop_rhpds"
cloud_provider="ec2"
verbose=2

def jsonToDictionary(filename):
'''
This Function just takes Json and returns a dictionary
'''
    JSONFILE = open(filename)
    jsonFilePointer = JSONFILE.read()
    return json.loads(jsonFilePointer)

def parse_Hostvars(inventory_dict,identifing_tag, hostvar_attributes):
'''
This Functions parses the dictionary object into a simpler dictionary
First we find the hosts that have our "identifing_tag"
For each host, grab attributes that we want based on "hostvar_attributes"
'''
    if cloud_provider=="ec2":
        verbose>=3 and print("identifing_tag is: ", identifing_tag)
        hosts_list=inventory_dict[identifing_tag]
        verbose>=3 and print("hosts_list is: ",hosts_list)
        parsed_hostvars = dict()

        for host in hosts_list:
            verbose>=4 and print("host is:",host)
            parsed_hostvars[host]=dict()
            for hostvar_attribute in hostvar_attributes:
                verbose>=4 and print(hostvar_attribute, ":", inventory_dict['_meta']['hostvars'][host][hostvar_attribute])
                parsed_hostvars[host][hostvar_attribute]=inventory_dict['_meta']['hostvars'][host][hostvar_attribute]
        return parsed_hostvars
def printTable(parsed_hosts):
'''
Print the host information in a table format
This was a good excercise in using len and some string manipulation
'''
    tableLength=120
    for host in parsed_hosts.keys():
        print("="*tableLength)

        print("|",host, " "*(tableLength-5-len(host)),"|")
        print("="*tableLength)
        for attribute in parsed_hosts[host].keys():
            atr_string=attribute + " "*((tableLength//2)-len(attribute)) + "| " + parsed_hosts[host][attribute]
            print("|", atr_string, " "*(tableLength-5-len(atr_string)),"|")
            print("-"*tableLength)

def printStaticInventory(parsed_hosts):
'''
Print the host information in a inventory format
'''
    topGroup="TopGroupName"
    ansible_user="ec2-user"
    #primary_ansible_ssh_host="ansible_ssh_host"
    primary_ansible_ssh_host="ec2_tag_internaldns"
    print('[{0}:vars]'.format(topGroup))
    print('''
timeout=60
ansible_become=yes
ansible_ssh_user={0}
    '''.format(ansible_user))
    print('[{0}:children]'.format(topGroup))
    groups=dict()
    for host in parsed_hosts.keys():
        groups[parsed_hosts[host]['ec2_tag_AnsibleGroup']]=1
    for group in groups.keys():
        print("[",group,"]", sep="")
        for host in parsed_hosts.keys():
            if parsed_hosts[host]['ec2_tag_AnsibleGroup']==group:
                print(parsed_hosts[host][primary_ansible_ssh_host]," ", end="")
                for attribute in ec2_hostvar_attributes:
                    print(attribute,"=\'",parsed_hosts[host][attribute],"\' ",end="",sep="")
                print()

def main():
    inventory_dict=jsonToDictionary("bigjson.json")
    parsed_hosts = dict()
    parsed_hosts=parse_Hostvars(inventory_dict,group_identifier,ec2_hostvar_attributes)

    #printTable(parsed_hosts)
    printStaticInventory(parsed_hosts)



main()
