from email.policy import default
import click
from compilation import compileClient,compileService,runService,createService


@click.command()
@click.option('--compile-client','-c', is_flag=True, help="Will compile all protos for each service and copy them into the client")
@click.option('--compile-service', '-cs', multiple=True,show_default="no service",default=[], help="Will compile the given service")
@click.option('--run-service', '-s',show_default="no service",default=None, help="Will run the given service")
@click.option('--new-service', '-ns',show_default="client",default=None, help="Will create a proto file and a dir for the service")
def cli(compile_client,compile_service,run_service,new_service):

    #CLIENT
    if compile_client:
        click.echo("Compiling all services and giving them to client...")
        compileClient()

    #SERVICES
    if len(compile_service) > 0 :
        for service in compile_service:
            click.echo(f"Trying compiling {service}...")
            compileService(service)

    if run_service != None :
        runService(service_name=run_service)
    
    if new_service != None :
        createService(service_name=new_service)