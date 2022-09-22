import click
from compilation import compileClient,compileService


@click.command()
@click.option('--compile-client','-c', is_flag=True, help="Will compile all protos for each service and copy them into the client")
@click.option('--compile-service', '-s', multiple=True, default=[''], help="Will compile each service mentionned")
def cli(compile_client,compile_service):
    if compile_client:
        click.echo("We are in the verbose mode.")
    click.echo("Hello World")
    for n in compile_service:
        click.echo('Bye {0}'.format(n))