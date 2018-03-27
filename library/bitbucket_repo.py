#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '2.2',
    'status': ['preview'],
    'supported_by': 'maintainer'
}

DOCUMENTATION = '''
---
module: bitbucket_repo

short_description: Create|Delete|Query Bitbucket Repo.

version_added: "3.5"

description:
    - "A module to create|delete|query a bitbucket repo"

options:
    username:
        description:
            - Bitbucket username.
        required: true
    password:
        description:
            - Bitbucket password.
        required: true
    url:
        description:
            - URL of the bitbucket server.
            - i.e. https://bitbucket.mycorpdomain.com
        required: true
    project_key:
        description:
          - Project key the repo is under.
          - i.e. /projects/DevOps/repos ... `DevOps` is the project_key
        required: true
    repo:
        description:
          - Name of the desired repo.
        required: true

    state:
        choices: [absent|present|query]
        default: query
        description:
          - The state you want the repo to be in.
'''

EXAMPLES = '''
# Get Info
- name: "Query the repo"
  bitbucket_repo:
    username: "MyUserName"
    password: "myPassword!"
    url: "https://mybitbucketserver.corpcomain.com"
    project_key: "DevOpsInfra"
    repo: "my-code-repo"

# Create new repo
- name: "Query the repo"
  bitbucket_repo:
    username: "MyUserName"
    password: "myPassword!"
    url: "https://mybitbucketserver.corpcomain.com"
    project_key: "DevOpsInfra"
    repo: "new-code-repo"
    state: present

'''
RETURN = '''
forkable:
    Description: "Whether true or false"
id:
    Description: "Repo ID"
links:
    Description: "A dictionary of links"
name:
    Description: "The name of the repo."
project:
    Description: "A project info dictionary."
public:
    Description: "Whether the repo is public [False|True]"
scmId:
    Description: "What type of SCM (hardcoded to 'git')"
slug:
    Description: "Repo slug."
state:
    Description: "Repo state."
statusMessage:
    Description: "Whether available or not ..."
'''


from ansible.module_utils.basic import AnsibleModule
try:
  from ansible.module_utils import six
  HAS_SIX = True
except ImportError:
  HAS_SIX = False

try:
  import requests
  HAS_REQUESTS = True
except ImportError:
  HAS_REQUESTS = False

import pprint
import sys
import json

def repoAction(**kwargs):
  if not HAS_REQUESTS:
    module.fail_json(msg='`requests` python module required for this module')
  if not HAS_SIX:
    module.fail_json(msg='`six` python module required for this module')

  api_url = '{0}/projects/{1}/repos/{2}'.format(kwargs['base_url'],kwargs['project'],kwargs['repo'])

  try:
    if kwargs['action'] == 'delete':
      r = requests.delete(api_url,headers=kwargs['headers'], auth=(kwargs['username'], kwargs['password']))
      return r.json()
    else:
      r = requests.get(api_url,headers=kwargs['headers'], auth=(kwargs['username'], kwargs['password']))
      # print(r.status_code)
      if r.status_code == 200:
        return r.json()
      else:
        return False
  except requests.ConnectionError:
    module.fail_json(msg='Can\'t connect to {}'.format(api_url))
    sys.exit(1)

def makeRepo(**kwargs):
  if not HAS_REQUESTS:
    module.fail_json(msg='`requests` python module required for this module')
  if not HAS_SIX:
    module.fail_json(msg='`six` python module required for this module')
  try:
    payload = dict(
      scmId='git',
      forkable='true',
      name=kwargs['repo']
    )
    api_url = '{0}/projects/{1}/repos'.format(kwargs['base_url'],kwargs['project'])
    payload = json.dumps(payload, sort_keys=True, indent=2)
    r = requests.post(api_url,
                      data=payload,
                      headers=kwargs['headers'],
                      auth=(kwargs['username'], kwargs['password']))

    # print(r.status_code)
    return r.json()
  except requests.ConnectionError:
    print("Can't connect to {0}".format(api_url))
    sys.exit(1)


def main():
  # define the available arguments/parameters that a user can pass to
  # the module
  module_args = dict(
    password=dict(type='str', required=True,no_log=True),
    project_key=dict(type='str', required=True),
    repo=dict(type='str', required=True),
    state=dict(type='str', required=False, default='query'),
    url=dict(type='str', required=True),
    username=dict(type='str', required=True),
  )
  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=False
  )

  result = dict(
      changed=False,
      repo=''
  )

  pp = pprint.PrettyPrinter(indent=2)

  if not module.params['password']:
      module.fail_json(msg="Password not specified.")
  if not module.params['project_key']:
      module.fail_json(msg="Project_key not specified.")
  if not module.params['repo']:
      module.fail_json(msg="Repo not specified.")
  if not module.params['url']:
      module.fail_json(msg="URL not specified.")
  if not module.params['username']:
      module.fail_json(msg="Username not specified.")

  funcvars = dict()
  funcvars['headers'] = {'Content-Type': 'application/json'}
  funcvars['base_url'] = '{}/rest/api/1.0'.format(module.params['url'])
  funcvars['username'] = module.params['username']
  funcvars['password'] = module.params['password']
  funcvars['project'] = module.params['project_key']
  funcvars['repo'] = module.params['repo']
  funcvars['action'] = 'get'
  state = module.params['state']

  facts = repoAction(**funcvars)
  if not facts and state == 'present':
    result['repo']=makeRepo(**funcvars)
    if result['repo']:
      result['changed'] = True
  elif facts:
    if state == 'absent':
      funcvars['action'] = 'delete'
      result['repo']=repoAction(**funcvars)
      if result['repo']:
        result['changed'] = True
    elif state == 'query':
      result['repo']=facts

  module.exit_json(**result)

if __name__ == '__main__':
    main()
