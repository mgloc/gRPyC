import click
from compilation import compileClient,compileService


@click.command()
@click.option('--compile-client','-c', is_flag=True, help="Will compile all protos for each service and copy them into the client")
@click.option('--compile-service', '-s', multiple=True,show_default="no service",default=[], help="Will compile the given service")
def cli(compile_client,compile_service):

    #CLIENT
    if compile_client:
        click.echo("Compiling all services and giving them to client...")
        compileClient()

    #SERVICES
    if len(compile_service) > 0 :
        for service in compile_service:
            click.echo(f"Trying compiling {service}...")
            compileService(service)