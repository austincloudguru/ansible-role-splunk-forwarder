Ansible Role: splunk-forwarder
=========
[![Molecule](https://github.com/austincloudguru/ansible-role-splunk-forwarder/workflows/Molecule/badge.svg?event=push)](https://github.com/austincloudguru/ansible-role-splunk-forwarder/actions?query=workflow%3AMolecule)
![Latest Version](https://img.shields.io/github/v/tag/austincloudguru/ansible-role-splunk-forwarder?sort=semver&label=Latest%20Version)
[![License](https://img.shields.io/github/license/austincloudguru/ansible-role-splunk-forwarder)](https://github.com/austincloudguru/ansible-role-splunk-forwarder/blob/master/LICENSE)

This role will deploy the Splunk universal forwarder.

Requirements
------------

This role is tested on Ubuntu 16.04, 18.04 and CentOS 7, 8, but should probably work on any systemd based system.  The previous version of this role is available as a tag (v1.0)


Role Variables
--------------

### Default

For most people, the default variables that are set should be fine, but there are use cases for changing them.  They are:


     splunk_forwarder_user                      # Default User (splunk)
     splunk_forwarder_group                     # Default Group (splunk)
     splunk_forwarder_uid                       # Default UID (10011)
     splunk_forwarder_gid                       # Default GID (10011)
     splunk_release                             # Default Release Version (7.1.3)
     splunk_url                                 # Default Download URL              
     splunk_forwarder_rpm                       # Default Splunk RPM Name
     splunk_forwarder_deb                       # Default Splunk Deb Name
     splunk_rpm                                 # Default RPM Full URL
     splunk_deb                                 # Default Deb Full URL
     splunk_deb_checksum                        # Default Deb Checksum
     splunk_rpm_checksum                        # Default RPM Checksum


### Playbook Variables

Within your playbook, you should set the following variables:

    splunk_forwarder_admin_user:    # Set the administrative user for the forwarder
    splunk_forwarder_admin_pass:    # Set the administrative password for the forwarder
    splunk_forwarder_depl_server:   # Set to the URL:Port of your splunk deployment server i.e. "splunk-mgt:8089" (optional)
    splunk_forwarder_indexer:       # Set to the URL:PORT of your splunk indexer i.e. "splunk-indexer:9997"
    splunk_forwarder_index:         # Set to the index that the forwarder should use i.e. "default"
    splunk_forwarder_sourcetype:    # Set the Source type i.e. "nginx"

You also need to set what logs to forward.  You can do using yaml multiline:

    splunk_forwarder_logs:
      - /var/log/nginx/access.log
      - /var/log/nginx/error.log

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
        splunk_forwarder_indexer: "splunk-indexer:9997"
        splunk_forwarder_index: "prodapps"
        splunk_forwarder_sourcetype: "nginx"
        splunk_forwarder_logs:
          - /var/log/nginx/access.log
          - /var/log/nginx/error.log
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
