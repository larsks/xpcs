import time
import click

import xpcs.globals
import xpcs.exc


def make_filterfunc(filter):
    if filter == 'all':
        filterfunc = lambda node: True
    elif filter in ['online', 'standby', 'shutdown', 'unclean',
                    'maintenace']:
        filterfunc = lambda node: node[filter] == 'true'
    else:
        raise ValueError(filter)

    return filterfunc


@click.group('node')
def cli():
    pass


@cli.command('is-online')
@click.argument('name')
@click.pass_context
def is_managed(ctx, name):
    '''Check if the given node is online'''
    state = ctx.obj.node(name)['online'] == 'true'
    if not xpcs.globals.quiet:
        print 'node %s %s online' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('is-standby')
@click.argument('name')
@click.pass_context
def is_standby(ctx, name):
    '''Check if the given node is standby'''
    state = ctx.obj.node(name)['standby'] == 'true'
    if not xpcs.globals.quiet:
        print 'node %s %s standby' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('is-shutdown')
@click.argument('name')
@click.pass_context
def is_shutdown(ctx, name):
    '''Check if the given node is shutdown'''
    state = ctx.obj.node(name)['shutdown'] == 'true'
    if not xpcs.globals.quiet:
        print 'node %s %s shutdown' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('wait')
@click.option('--timeout', '-t', default=0)
@click.option('--negate', '-!', is_flag=True, default=False)
@click.option('--online', 'filter', flag_value='online', default=True)
@click.option('--standby', 'filter', flag_value='standby')
@click.option('--shutdown', 'filter', flag_value='shutdown')
@click.option('--unclean', 'filter', flag_value='unclean')
@click.option('--maintenance', 'filter', flag_value='maintenance')
@click.argument('nodes', nargs=-1, default=None)
@click.pass_context
def wait(ctx, negate=False, timeout=0, all=False, filter=None, nodes=None):
    filterfunc = make_filterfunc(filter)
    wait_start = time.time()

    while True:
        if not len(nodes):
            _nodes = [node for node in ctx.obj.nodes]
        else:
            _nodes = [node for node in ctx.obj.nodes
                      if node['name'] in nodes]

        if negate:
            matched = any(filterfunc(node) for node in _nodes)
        else:
            matched = any(not filterfunc(node) for node in _nodes)

        if not matched:
            break

        if timeout and (time.time() >= wait_start + timeout):
            raise xpcs.exc.TimeoutError(
                'Timed out while waiting for nodes')

        time.sleep(1)


@cli.command('list')
@click.option('--all', 'filter', flag_value='all', default=True)
@click.option('--online', 'filter', flag_value='online')
@click.option('--standby', 'filter', flag_value='standby')
@click.option('--shutdown', 'filter', flag_value='shutdown')
@click.option('--unclean', 'filter', flag_value='unclean')
@click.option('--maintenance', 'filter', flag_value='maintenance')
@click.pass_context
def list(ctx, filter='all'):
    '''List resources'''
    filterfunc = make_filterfunc(filter)
    print '\n'.join(node['name'] for node in ctx.obj.nodes
                    if filterfunc(node))
