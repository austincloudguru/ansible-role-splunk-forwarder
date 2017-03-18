Role Name
=========
[![Build Status](https://travis-ci.org/AustinCloudGuru/ansible-role-splunk-forwarder.svg?branch=master)](https://travis-ci.org/AustinCloudGuru/ansible-role-splunk-forwarder)

This role will deploy the Splunk univeral forwarder.

Requirements
------------

None

Role Variables
--------------

### Default

For most people, the default variables that are set should be fine, but there are use cases for changing them.  They are:


     splunk_forwarder_user
     splunk_forwarder_group
     splunk_forwarder_uid
     splunk_forwarder_gid
     splunk_forwarder_url
     splunk_forwarder_rpm

### Playbook Variables

Within your playbook, you should set the following variables:

    splunk_forwarder_indexer: # Set to the URL:PORT of your splunk indexer i.e. "splunk-indexer.blackbaudcloud.com:9997"
    splunk_forwarder_index:  # Set to the index that the forwarder should use i.e. "default"
    splunk_forwarder_sourcetype:  # Set the Source type i.e. "nginx"

You also need to set what logs to forward.  You can do using yaml multiline:

    splunk_forwarder_logs: |
      [monitor:///var/log/nginx/access.log*]
      [monitor:///var/log/nginx/error.log*]

Dependencies
------------

You must have a splunk indexer running in your environment.

Example Playbook
----------------

You should define the required variables in your playbook and call the role:

    - hosts: nginx
      remote_user: ec2-user
      become: True
      vars:
        splunk_forwarder_indexer: "splunk-indexer.blackbaudcloud.com:9997"
        splunk_forwarder_index: "prodapps"
        splunk_forwarder_sourcetype: "nginx"
        splunk_forwarder_logs: |
           [monitor:///var/log/nginx/access.log*]
           [monitor:///var/log/nginx/error.log*]
        roles:
        - splunk-forwarder

If you want to run this against an AmazonLinux instances, add the following to your playbook, otherwise it will fail.:

     pre_tasks:
       - set_fact: ansible_distribution_major_version=6
         when: ansible_distribution == "Amazon" and ansible_distribution_major_version == "NA"


License
-------

MIT


Author Information
------------------

Mark Honomichl aka [AustinCloudGuru](https://austincloud.guru)
Created in 2016 
