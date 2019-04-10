from setuptools import setup

setup(
		name ='snapshotalyzer3000',
		version ='0.1',
		author ='Rafael Franco',
		author_email ='francorafae@gmail.com',
		description = 'SnapshotAlyzer 3000 is a tool for managing AWS EC2 snapshots',
		license = "GPLv3+",
		packages = ['shotty'],
		url = "https://github.com/ELRuncho/pythonScripts",
		install_requires=[
			'click',
			'boto3'
		],
		entry_points='''
			[console_script]
			shotty=shotty.shotty:cli
		''',
	)
