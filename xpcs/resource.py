import time
import click
import xpcs.globals
import xpcs.exc


def make_filterfunc(filter):
    if filter == 'all':
        filterfunc = lambda rsc: True
    elif filter == 'started':
        filterfunc = lambda rsc: rsc['role'] == 'Started'
    elif filter == 'stopped':
        filterfunc = lambda rsc: rsc['role'] == 'Stopped'
    elif filter in ['active', 'failed', 'managed', 'orphaned']:
        filterfunc = lambda rsc: rsc[filter] == 'true'
    else:
        raise ValueError(filter)

    return filterfunc


@click.group('resource')
def cli():
    pass


@cli.command('is-managed')
@click.argument('name')
@click.pass_context
def is_managed(ctx, name):
    '''Check if the given resource is managed'''
    state = ctx.obj.resource(name)['managed'] == 'true'
    if not xpcs.globals.quiet:
        print 'resource %s %s managed' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('is-active')
@click.argument('name')
@click.pass_context
def is_active(ctx, name):
    '''Check if the given resource is active'''
    state = ctx.obj.resource(name)['active'] == 'true'
    if not xpcs.globals.quiet:
        print 'resource %s %s active' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('is-failed')
@click.argument('name')
@click.pass_context
def is_failed(ctx, name):
    '''Check if the given resource is failed'''
    state = ctx.obj.resource(name)['failed'] == 'true'
    if not xpcs.globals.quiet:
        print 'resource %s %s failed' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('is-started')
@click.argument('name')
@click.pass_context
def is_started(ctx, name):
    '''Check if the given resource is started'''
    state = ctx.obj.resource(name)['role'] == 'Started'
    if not xpcs.globals.quiet:
        print 'resource %s %s started' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('is-stopped')
@click.argument('name')
@click.pass_context
def is_stopped(ctx, name):
    '''Check if the given resource is stopped'''
    state = ctx.obj.resource(name)['role'] == 'Stopped'
    if not xpcs.globals.quiet:
        print 'resource %s %s stopped' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('list')
@click.option('--all', 'filter', flag_value='all', default=True)
@click.option('--started', 'filter', flag_value='started')
@click.option('--stopped', 'filter', flag_value='stopped')
@click.option('--active', 'filter', flag_value='active')
@click.option('--failed', 'filter', flag_value='failed')
@click.pass_context
def list(ctx, filter='all'):
    '''List resources'''
    if filter == 'all':
        filterfunc = lambda rsc: True
    elif filter == 'started':
        filterfunc = lambda rsc: rsc['role'] == 'Started'
    elif filter == 'stopped':
        filterfunc = lambda rsc: rsc['role'] == 'Stopped'
    elif filter == 'active':
        filterfunc = lambda rsc: rsc['active'] == 'true'
    elif filter == 'failed':
        filterfunc = lambda rsc: rsc['failed'] == 'true'

    print '\n'.join(rsc['id'] for rsc in ctx.obj.resources
                    if filterfunc(rsc))


@cli.command('wait')
@click.option('--timeout', '-t', default=0)
@click.option('--negate', '-!', is_flag=True, default=False)
@click.option('--active', 'filter', flag_value='active', default=True)
@click.option('--started', 'filter', flag_value='started')
@click.option('--stopped', 'filter', flag_value='stopped')
@click.argument('resources', nargs=-1, default=None)
@click.pass_context
def wait(ctx, negate=False, timeout=0, filter=None, resources=None):
    filterfunc = make_filterfunc(filter)
    wait_start = time.time()

    while True:
        if not len(resources):
            _resources = [resource for resource in ctx.obj.resources]
        else:
            _resources = [resource for resource in ctx.obj.resources
                          if resource['id'] in resources]

        if negate:
            matched = any(filterfunc(rsc) for rsc in _resources)
        else:
            matched = any(not filterfunc(rsc) for rsc in _resources)

        if not matched:
            break

        if timeout and (time.time() >= wait_start + timeout):
            raise xpcs.exc.TimeoutError(
                'Timed out while waiting for resources')

        time.sleep(1)
