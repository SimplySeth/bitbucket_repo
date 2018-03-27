# Ansible module for Creating/Deleting/Querying Bitbucket Repos

## Example Usage: 

### Creation:

```
---
- hosts: localhost
  connection: local
  gather_facts: yes
  vars:
  tasks:
    - bitbucket_repo:
        password: "NunYaBeez!"
        project_key: "DEVOPS"
        repo: "my-new-repo"
        url: "https://bitbucket.mycorpdomain.net"
        username: "UserNameWithProjectSuperPowers"
        state: present
      register: bbout

    - debug:
        var: bbout

```

### Deletion:

```
---
- hosts: localhost
  connection: local
  gather_facts: yes
  vars:
  tasks:
    - bitbucket_repo:
        password: "NunYaBeez!"
        project_key: "DEVOPS"
        repo: "my-new-repo"
        url: "https://bitbucket.mycorpdomain.net"
        username: "UserNameWithProjectSuperPowers"
        state: absent
      register: bbout

    - debug:
        var: bbout

```

### Query:
state can either be omitted or stated as `query`

```
---
- hosts: localhost
  connection: local
  gather_facts: yes
  vars:
  tasks:
    - bitbucket_repo:
        password: "NunYaBeez!"
        project_key: "DEVOPS"
        repo: "my-new-repo"
        url: "https://bitbucket.mycorpdomain.net"
        username: "UserNameWithProjectSuperPowers"
      register: bbout

    - debug:
        var: bbout

```


