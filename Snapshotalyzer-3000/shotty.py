import boto3
import click

session= boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
	instances=[]

	if project:
		filters = [{'Name':'tag:Project', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()	
	return instances

@click.group()
def cli():
	"""Shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
	"""Comands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None, help="Only snapshots pertaining to the specified project tag")
def list_snapshots(project):
	"Lists EC2 snapshots"

	instances = filter_instances(project)
	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshots.all():
				print(" | ".join((
						s.id,
						v.id,
						i.id,
						s.state,
						s.progress,
						s.start_time.strftime("%c")
					)))
	return

@cli.group('volumes')
def volumes():
	"""Commands for Volumes"""
@volumes.command('list')
@click.option('--project', default=None, help="Only Volumes pertaining to the specified project tag")
def list_volumes(project):
	"Lists EC2 volumes"

	instances = filter_instances(project)

	for i in instances:
		for v in i.volumes.all():
			print(" | ".join((
				v.id,
				i.id,
				v.state,
				str(v.size)+"GiB",
				v.encrypted and "Encrypted" or "Not Encrypted"
			)))
	return

@cli.group('instances')
def instances():
	"""Commands For instances"""

@instances.command('snapshot')
@click.option('--project', default=None,help="Only instances for project (tag Project:<name>")
def create_snapshots(project):
	"Create snapshots for EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		i.stop
		for v in i.volumes.all():
			print("Creating snapshot of volume {0} on instance {1}".format(v.id,i.id))
			v.create_snapshot(Description="Created by Snapshotalyzer 3000")
	return


@instances.command('list')
@click.option('--project', default=None,help="Only instances for project (tag Project:<name>")
def list_instances(project):
	"List EC2 instances"
	instances= filter_instances(project)

	for i in instances:
		tags = { t['Key']: t['Value'] for t in i.tags or [] }
		print(' | '.join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,tags.get('Project', '<no project>')
			)))
	return 
@instances.command('stop')
@click.option('--project', default=None, help='Only instances drom startet project')
def stop_instances(project):
	"stop ec2 instances"
	instances = filter_instances(project)

	for i in instances:
		print("Stopping instance {0}".format(i.id))
		i.stop()

@instances.command('start')
@click.option('--project', default=None, help='Only instances drom statet project')
def start_instances(project):
	"start ec2 instances"
	instances = filter_instances(project)

	for i in instances:
		print("Starting instance {0}".format(i.id))
		i.start()



if __name__== '__main__':
	cli()