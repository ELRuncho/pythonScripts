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

def has_pending_snapshot(volume):
	snapshots=list(volume.snapshots.all())
	return snapshots and snapshots[0].state=='pending'

@click.group()
def cli():
	"""Shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
	"""Comands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None, help="Only snapshots pertaining to the specified project tag")
@click.option('--all', 'list_all', default=False, is_flag=True, help='lists al snapshots for each volume, not just the most recent')
def list_snapshots(project, list_all):
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
				if s.state=='completed' and not list_all: break
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

		print("Stopping {0}".format(i.id))

		i.stop()
		i.wait_until_stopped()

		for v in i.volumes.all():
			if has_pending_snapshot(v):
				print("Skipping volume {0}. snapshot already in progress".filter(v.id))
				continue
			print("Creating snapshot of volume {0} on instance {1}".format(v.id,i.id))
			v.create_snapshot(Description="Created by Snapshotalyzer 3000")

		print("Starting {0}....".format(i.id))

		i.start()
		i.wait_until_running()

	print("Completed")

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

	"Stop EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		print("Stopping instance {0}".format(i.id))
		try:
			i.stop()
		except botocore.exeptions.ClientError as e:
			print("Could not stop instance {0}. ".filter(i.id))
			continue

	return


@instances.command('start')
@click.option('--project', default=None, help='Only instances drom statet project')
def start_instances(project):

	"Start EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		print("Starting instance {0}. ".format(i.id))
		try:
			i.start()
		except botocore.exeptions.ClientError as e:
			print("Could not start instnance {0}".filter(i.id))
			continue
	return



if __name__== '__main__':
	cli()