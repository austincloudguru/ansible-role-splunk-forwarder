# Ansible Role: splunk-forwarder

[![Molecule](https://github.com/troyfontaine/ansible-role-splunk-forwarder/workflows/Molecule/badge.svg?event=push)](https://github.com/troyfontaine/ansible-role-splunk-forwarder/actions?query=workflow%3AMolecule)
![Latest Version](https://img.shields.io/github/v/tag/troyfontaine/ansible-role-splunk-forwarder?sort=semver&label=Latest%20Version)
[![License](https://img.shields.io/github/license/troyfontaine/ansible-role-splunk-forwarder)](https://github.com/troyfontaine/ansible-role-splunk-forwarder/blob/master/LICENSE)

This role will deploy the Splunk Universal Forwarder package on Linux systems running on AMD64 or ARM64 platforms running recent Ubuntu LTS releases or Red Hat Enterprise Linux derived releases.

## Requirements

This role is tested using Molecule via GitHub Actions with Ubuntu 16.04, 18.04, 20.04, 22.04, Oracle Linux 8 and Amazon Linux 2, but should probably work on any systemd based system on a compatible platform.

## Functionality

This role deploys Splunk Universal Forwarder from version 8.2.8 (AMD64) or 9.0.2 (ARM64) through to 9.1.0.1 (both architectures).

To use this role as part of a Packer build pipeline, set the variable `building_image` to `true`.

This role can accept a list of indexers to ["load balance"][splunk_load_balance] log output as per Splunk's recommendations.

### TLS

Based on the configuration of the environment variable `splunk_forwarder_output_use_tls`, the Splunk2Splunk (S2S) port used with the provided list of indexers (via `splunk_forwarder_indexer_hostname`) will be set to match the default ports that a Splunk Indexer would use (TCP 9997 for unencrypted, TCP 9998 for TLS encrypted traffic).  The unencrypted S2S port setting can be overriden by specifying a value for `splunk_forwarder_indexer_notls_port`.  Similarly, if you use a non-standard encrypted port for S2S, you can modify `splunk_forwarder_indexer_tls_port` to configure that.

To enable TLS certificate verification, specify a path value for the variable `splunk_forwarder_output_root_ca_path`.  To enable Mutual TLS, you will need to specify a path to a valid certificate for `splunk_forwarder_output_client_cert_path`.

### Log Ingestion

This role accepts a list of dictionaries to allow for some customization of the monitor entries in the [inputs.conf](./templates/inputs.conf.j2).  This allows for disabling, configuring sourcetype, specifying a non-default index (NOTE: The index MUST already exist on the indexer for you to send logs to the index specified) and crcSalt.  This is a non-exhaustive list of options-but covers a variety of use-cases.

## Role Variables

### Default

This role provides a variety of options that can be enabled/disabled based on variables configured in the playbook used to reference this role.

For most people, the default variables that are set should be fine, but there are use cases for changing them.  You can find the defaults in the [defaults/main.yml](defaults/main.yml).  From there, you can copy the variable you want to override and specify it in your calling playbook.

#### Required variables

The following variables must be configured in order for the SplunkForwarder to capture logs and send them to an unauthenticated/unencrypted Indexer endpoint:
    splunk_forwarder_indexer_hostname:
      - "splunk-indexer-hostname-goes-here"
    splunk_forwarder_logs:
      - { 'path': '/var/log/syslog' }
      - { 'path': '/var/log/nginx/access.log', 'sourcetype': 'nginx', 'index': 'nginx' }
      - { 'path': '/var/log/nginx/error.log', 'sourcetype': 'nginx', 'index': 'nginx' }

The following variables are examples of what you can configure:

    splunk_forwarder_admin_user:            # Set the administrative user for the forwarder
    splunk_forwarder_admin_pass:            # Set the administrative password for the forwarder
    splunk_forwarder_depl_server:           # Set to the URL:Port of your splunk deployment server i.e. "splunk-mgt:8089" (optional)
    splunk_forwarder_indexer_hostname:      # Set to a list of the hostnames of your splunk indexer(s) i.e. "splunk-indexer"
    splunk_forwarder_output_use_tls:        # Set to true then adjust your variables as necessary
    splunk_forwarder_default_index:         # Set to the index that the forwarder should use i.e. "default"
    splunk_forwarder_default_sourcetype:    # Set the Source type i.e. "nginx"


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
        splunk_forwarder_indexer_hostname:
          - "splunk-indexer"
        splunk_forwarder_default_index: "prodapps"
        splunk_forwarder_default_sourcetype: "nginx"
        splunk_forwarder_logs:
          - { 'path': '/var/log/nginx/access.log', 'sourcetype': 'nginx', 'index': 'nginx' }
          - { 'path': '/var/log/nginx/error.log', 'sourcetype': 'nginx', 'index': 'nginx' }
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

Original by Mark Honomichl aka [AustinCloudGuru](https://austincloud.guru).


[splunk_load_balance]: https://docs.splunk.com/Documentation/Splunk/9.1.0/Forwarding/Setuploadbalancingd
