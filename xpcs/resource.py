import time
import click
import xpcs.globals
import xpcs.exc


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


@cli.command('wait-for-start')
@click.option('--timeout', '-t', default=0)
@click.argument('name')
@click.pass_context
def wait_for_start(ctx, name, timeout=0):
    '''Wait for the given resource to start'''
    wait_start = time.time()
    while True:
        state = ctx.obj.resource(name)['role'] == 'Started'
        if state:
            break

        if timeout and (time.time() >= wait_start + timeout):
            raise xpcs.exc.TimeoutError(
                'Timed out while waiting for %s' % name)

        time.sleep(1)

    if not xpcs.globals.quiet:
        print 'resource %s is started' % name


@cli.command('wait-for-stop')
@click.option('--timeout', '-t', default=0)
@click.argument('name')
@click.pass_context
def wait_for_stop(ctx, name, timeout=0):
    '''Wait for the given resource to stop'''
    wait_start = time.time()
    while True:
        state = ctx.obj.resource(name)['role'] == 'Stopped'
        if state:
            break

        if timeout and (time.time() >= wait_start + timeout):
            raise xpcs.exc.TimeoutError(
                'Timed out while waiting for %s' % name)

        time.sleep(1)

    if not xpcs.globals.quiet:
        print 'resource %s is stopped' % name


@cli.command('wait-all-stop')
@click.option('--timeout', '-t', default=0)
@click.pass_context
def wait_all_stop(ctx, timeout=0):
    '''Wait for all resources to stop'''
    wait_start = time.time()
    while True:
        started = any(
            rsc['role'] != 'Stopped'
            for rsc in ctx.obj.resources)

        if not started:
            break

        if timeout and (time.time() >= wait_start + timeout):
            raise xpcs.exc.TimeoutError(
                'Timed out while waiting for resources to stop')

        time.sleep(1)

    if not xpcs.globals.quiet:
        print 'all resources are stopped'


@cli.command('wait-all-start')
@click.option('--timeout', '-t', default=0)
@click.pass_context
def wait_all_start(ctx, timeout=0):
    '''Wait for all resources to start'''
    wait_start = time.time()
    while True:
        stopped = any(
            rsc['role'] != 'Started'
            for rsc in ctx.obj.resources)

        if not stopped:
            break

        if timeout and (time.time() >= wait_start + timeout):
            raise xpcs.exc.TimeoutError(
                'Timed out while waiting for resources to start')

        time.sleep(1)

    if not xpcs.globals.quiet:
        print 'all resources are started'


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
