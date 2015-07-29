import click


@click.group('node')
def cli():
    pass


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
    if filter == 'all':
        filterfunc = lambda node: True
    elif filter == 'online':
        filterfunc = lambda node: node['online'] == 'true'
    elif filter == 'standby':
        filterfunc = lambda node: node['standby'] == 'true'
    elif filter == 'shutdown':
        filterfunc = lambda node: node['shutdown'] == 'true'
    elif filter == 'unclean':
        filterfunc = lambda node: node['unclean'] == 'true'
    elif filter == 'maintenance':
        filterfunc = lambda node: node['maintenance'] == 'true'

    print '\n'.join(node['name'] for node in ctx.obj.nodes
                    if filterfunc(node))
