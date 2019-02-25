#Mail Telemetry ver 0.3 Ansible Script.
#Developed from Marco Righini @ Intel (marco.righini@intel.com) .Thanks for the help to Josh Hilliker (josh.hilliker@intel.com).

Instructions:
There are 2 main script>
Ansible PlayBook files:
1. sshkey.yaml ansible playbook
2. setup_telemetries ansible playbook
Config files:
1. /taks/vars/vars.yaml > variable files (like IP addresses of hosts, Software versions)
2. inventory file > inventory.txt (contains )

Prerequisits:
- Ansible master node up and running and working
- Ansible Playbook downloaded
- Today the Playbook works only with Centos and RHEL. *Ubuntu under work in progress
- All Servers installed with IP configuration set
- Firewall Rulles between nodes require the following ports to be open:
  1. Collectd: TCP/8888
  2. Prometheus Server: TCP/9090
  3. Node exporter: TCP/9100
  4. Grafana: TCP/3000
  5. Collectd_exporter: TCP/9103


  How to run the Playbooks:
  If you do not have password less configuration setup yet follow the steps otherwise skip to Run Telemetries Playbook

Password Less configuration:

  Generate on ansible Master Node pub and private keys:
#  ssh-keygen
Move the the home directory of the user> example for root:
/root/.ssh
open id_rsa.pub

1. copy key and add the key to the sskkey.yaml file.

2. modify /etc/ansible/ansible.cfg under [defaults] host_key_checking = False

once done run to copy the key on all the nodes we need.

#  ansible-playbook -i inventory.txt ./tasks/sshkey.yaml --ask-pass

_________________________________________________________________________________
Run Telemetries Playbook

Once you can login in each node password less run the following command to install telemeries:

#  ansible-playbook setup_telemetries.yaml -i inventory.txt



SSH key echange pre req. to make it happen automatically through sshkey.yaml do the following:
  1. modify /etc/ansible/ansible.cfg under [defaults] host_key_checking = False
  2. copy ur pub key under the ansible host /home/username/.ssh/id_rsa.pub and modify ansible yaml file accordingly
  2. run: ansible-playbook -i <inventory-file> sshkey.yaml --ask-pass --extra-vars='pubkey="<pubkey>" in my case:
  ansible-playbook -vvv -i inventory.txt ./tasks/sshkey.yaml --ask-pass

First launch from ansible server: ansible-playbook -i inventory.txt setup_telemetries.yaml
