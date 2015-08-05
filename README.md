# Overview

The `xpcs` command is a small suite of utilities for interacting with
a Pacemaker cluster.  Unlike existing Pacemaker commands such as `pcs`
and `crm`, `xpcs` is designed to be useful in scripts.

# Installing

`xpcs` is a standard Python package.  You can install it using `pip`:

    pip install xpcs

Or by cloning the source and running `setup.py`:

    $ git clone http://github.com/larsks/xpcs.git
    $ cd xpcs
    $ python setup.py install

# Resources

The `xpcs` command supports the follow resource operations:

- `is-active`:   Check if the given resource is active
- `is-failed`:   Check if the given resource is failed
- `is-managed`:  Check if the given resource is managed
- `is-started`:  Check if the given resource is started
- `is-stopped`:  Check if the given resource is stopped
- `list`:        List resources
- `wait`:        Wait for resources to reach desired state

## Resource examples

### List stopped resources

    # xpcs resource list --stopped

### Check if a resource is stopped

    # xpcs resource is-active httpd-clone &&
        echo httpd is active.

### Wait for all resources to start

This will wait until all Pacemaker managed resources have started.

    # xpcs resource wait

### Stop resources matching a pattern

This example demonstrates you can use `xpcs` as part of a more complex
shell pipeline.

    # xpcs resource list |
        grep neutron |
        xargs -n1 pcs resource disable
    
### Wait for specific resources to stop

This command will block until the three named resources have stopped.

    # xpcs resource wait --stopped \
        heat-api-clone heat-api-cfn-clone heat-api-cloudwatch-clone

# Nodes

The `xpcs` command supports the following operations on nodes:

- `is-online`:    Check if the given node is online
- `is-shutdown`:  Check if the given node is shutdown
- `is-standby`:   Check if the given node is standby
- `list`:         List nodes
- `wait`:         Wait for node to reach a given state

## Node examples

### Check if the given node is online

    # xpcs node is-online pcmk-mac5254007feba5 &&
        echo The node is online.

### Wait for a specific node to go into standby mode

    # xpcs node wait --standby pcmk-mac5254007feba5

### Wait for all nodes to become active

    # xpcs node wait
