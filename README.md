# pythonScripts
python Scripts
## Running 
first install pipenv, then:

```
pipenv install
pipenv run "python Meteors/findMeteors.py"
```

##Snapshotalyzer-3000

Demo script, uses boto3 to manage aws ec2 instances snapshots

###Config

Shotty uses the aws-cli config file. create a profile for shotty:

`aws configure --profile shotty`

###Running

`pipenv run python Snapshotalyzer-3000/shotty.py`


