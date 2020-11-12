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

`pipenv run python Snapshotalyzer-3000/shotty.py <command> <subcomand> --project=Project`

*command* is instnaces, volumes or snapshots
*subcommand* - depends on command, use  <command> --help for a list of subcomands
*--project* is optional





-----------------------------------------------------------------------------




# Welcome to Unicorn.Rentals!

Rainbow Day is coming, and we need to be prepared!  Forecasting is important, but we kind of need Infrastructure, too!  There's a lot for us to figure out, so read on.  There's a refresher of the main franchise rent/purchase mechanics at the bottom.

# Franchise Set up

They say if you get enough monkeys on typewriters for long enough, through sheer random chance they'll eventually produce The Complete Works of Shakespeare.  We put that theory to the test, not to produce Shakespeare, but to get you the best documentation possible (really, we just wanted an excuse to hire real monkeys for something).

Where to start?

Our **HTTP Order Routing System, Enhanced** (*HORSE*) and **Fulfilment API** are managed by Unicorn.Rentals HQ and are up and ready (see our amazing, *all-you'll-ever-need* architecture diagram below).\
As a new franchisee, we've provisioned an AWS account with some stuff in it for you.  Not sure what stuff, we kinda built all that a while ago, but we think it helps.

Everything else you're going to need to build yourself, but it's (mostly) automated we've been told, so it should be pretty simple.  This diagram should help.  

![Unicorn.Rentals Franchise Architecture](https://s3.amazonaws.com/ee-assets-prod-us-east-1/modules/011a6fc0319e4a25ac041d86c0b7629b/v1/unicorn-architecture.png "Unicorn.Rentals Franchise Architecture")

### These components can be built in parallel, so divide and conquer could be a good strategy for your team.

### Storefront/Store

Kubernetes (EKS) is used to accept our public API calls and host our storefront.  Instructions to set it up are <a href="https://dashboard.eventengine.run/docs?url=https:%2F%2Fs3.amazonaws.com%2Fee-assets-prod-us-east-1%2Fmodules%2F011a6fc0319e4a25ac041d86c0b7629b%2Fv1%2Fstore-eks-install.md" target="_blank">available here</a>.  

With the default config, the storefront wil handle Red, Blue, and Green rent requests.

### Proxy  

There's a *Pipeline* for this one, though apparently it might need some extra configuration? Download and deploy the [Proxy Pipeline Template](https://s3.amazonaws.com/ee-assets-prod-us-east-1/modules/011a6fc0319e4a25ac041d86c0b7629b/v1/toolchain-proxy.yml) in CloudFormation.

This *Toolchain* will create a *CodeCommit* repository, *CodeBuild* job, and *CodePipeline* CI/CD pipeline to deploy the Proxy.

**HINT:** This Pipleine will deploy its own CloudFormation stack for the proxy.  If you run into any issues in the Pipeline, you might need to manually delete this stack before re-releasing any change.  Keep this in mind!

### VPC Endpoint

Instructions on how to configure this are <a href="https://dashboard.eventengine.run/docs?url=https:%2F%2Fs3.amazonaws.com%2Fee-assets-prod-us-east-1%2Fmodules%2F011a6fc0319e4a25ac041d86c0b7629b%2Fv1%2Fvpc-endpoint-setup.md" target="_blank">available here</a>.

### Stock Admin Panel

Theres a CloudFormation template for its *Pipeline* [available here](https://s3.amazonaws.com/ee-assets-prod-us-east-1/modules/011a6fc0319e4a25ac041d86c0b7629b/v1/toolchain-stock.yml).

Once the Stock Admin panel is deployed, we should be fully back online! (Rube Goldberg would be proud!)

# Security

Someone in the security team was playing around with IAM permissions and blocked our access to CloudTrail Events.\
Doesn't seem like this is a huge issue, but CloudTrail can be really handy for knowing what's happening in our account (espeically when things are happening we might not expect!) 

Wonder if there's any other way we could get ~*CloudWatch*~ *Insights* into CloudTrail?

# Marketing

Look out for opportunites to promote ourselves and increase ~~stock prices~~ the joy you derive from working at Unicorn.Rentals.

# Key Concepts

If you've gotten this far, good reading!

There are some basics you should know.  It's pretty simple stuff and was mentioned in your intial franchise introduction, but let's spell it out all the same.

So it's kind of in the name, but the main thing we do here at Unicorn.Rentals is, well, rent unicorns!\
But did you know we also have to buy those unicorns? (They may be mythical creatures and all, but it's not like they appear out of no where!)\
In case the difference wasn't clear...

*Renting* is what our customers do - they send through a request to get a Unicorn for a specific amount of time.\
Once their rental period is over, the Unicorn **will come back to our stables**.\
Unicorns are not rented indefinitely (otherwise, we'd be call Unicorn.Buyals)

*Purchasing* is what we do, since we need to make sure we have enough Unicorns for people to rent at any given time.\
Unicorn.Rentals has always been on an enormous growth trajectory, so we've never needed to sell unicorns.\
Maybe someone should put that feature on the backlog just in case?

What's hard about our business is knowing how many unicorns to have and when!\
Too many unrented unicorns costs us money (stable costs, minions to look after them, etc.).  This is bad.\
Too few unicorns means missed orders, which means unhappy children (and lost money).  This is also bad.

Predicting the right amount of unicorns for any given time will give us maximum points/money.  This, we believe, is better than bad (who knows what makes Kyle happy really).

Long story short - don't buy too many unicorns too early.  Forecasting can help with that.

One final piece of advice - keep our infrastructure up and running!  We may be able to make it slightly more efficient,\
but the key will be keeping it up.  HORSE will help aggregate a lot of our incoming requests (we think),\
so we're not expecting *too* much load (famous last words?).
