CloudPing - AWS Hosted Uptime Monitoring
========================================


Overview
--------

This project is an experiment in using AWS Lambda + CloudWatch for a nearly-free
website uptime alert service. Similar to a basic Pingdom account, this fetches
configured webpages and sends configurable alerts when they are down. It's
slightly complicated to set up but runs almost entirely within the AWS free
tier supporting multiple sites with configurable notifications.


Getting Started
---------------

To get started running your own monitoring service you'll need a clone of
repository, Python 2.7, and the latest
`virtualenv <https://virtualenv.readthedocs.org/en/latest/>`_ installed.

    $ git clone https://github.com/mlavin/cloudping.git
    $ cd cloudping
    $ make bundle

This will create a ``cloudping.zip`` file containing the ``cloudping.py``
handler script and all of its dependencies.


Configuring AWS Services
------------------------

This bundled script will run in `an AWS account <https://www.amazon.com/ap/signin>`_.
If you don't already have one then you should create one and continue using an
administrative user for that account.


Lambda
______

The bundled ``cloudping.zip`` is used to run an AWS Lambda script. This should
be uploaded using the AWS console selecting the following options:

- Name: CloudPing
- Description: Monitor webpages using Lambda
- Runtime: Python2.7
- Upload Zip: ``cloundping.zip``
- Handlder: ``cloudping.ping``
- Role: Basic Execution Role
- Memory: 128 MB
- Timeout: 10 secs


CloudWatch
__________

CloudWatch is used to run the script periodically and monitor its results.
To run the script periodically you need to create a new Rule:

- Event Selector: Schedule every 5 mins
- Target
  - Lambda Function: CloudPing
  - Configure Input (Constant JSON text): {"domain": "example.com", "protocol": "http"}
- Name: example_com-ping
- Description: Ping the example.com domain periodically
- State: Enabled

You can adjust the schedule to fit the granularity of the checks that you would like.
Here the ``example.com`` references would be replaced with the domain that you wish
to monitor. The input JSON can take the following options:

- domain (default: example.com)
- protocol (default: http)
- path (default: /)
- method (default: GET)
- allow_redirects (default: False)
- timeout (default: 5)

``domain``, ``protocol``, ``path``, and ``method`` determine what page is requested and how.
``allow_redirects`` determines whether 30X response is considered and error or if
the redirect should be followed to the final page to determine the status. ``timeout``
is the timeout of the request in seconds.

The final piece is to setup an alarm which watches for errors when running the
script. For this you need a new CloudWatch Alarm:

- Metric: CloudPing Errors
- Threshold:
  - Name: SiteDown
  - Description: Too many site errors in the window.
  - Whenever: Errors is >= 2 for 1 consecutive period
  - Period: 15 mins
  - Statistic: Sum

As with the rate of the checks, you can adjust these thresholds to fit your own
needs. You can also configure the actions to send emails or SMS when the state
reaches ALARM or take other actions as needed.


Cost Estimation
---------------

This makes use of 3 main AWS services which have the potential to incur costs
to your AWS account: Lambda, CloudWatch, and SNS. Each has some level of free
usage.


Lambda
______

https://aws.amazon.com/lambda/pricing/

- The Lambda free tier includes 1M free requests per month and 400,000 GB-seconds of compute time per month.

With 128 MB of memory allocated to the Lambda function that translates to
a 1,000,000 checks or 3,200,000 seconds of compute time. If each check takes
less than 3 seconds then you can use the full million calls. That's enough to
check ~23 pages once every minute assuming ~43,200 (60 x 24 x 30) minutes in
a month.


CloudWatch
__________

https://aws.amazon.com/cloudwatch/pricing/

- New and existing customers also receive 3 dashboards of up to 50 metrics each per month at no additional charge.
- New and existing customers also receive 10 metrics (applicable to Detailed Monitoring for Amazon EC2 instances, Custom Metrics, or CloudWatch Logs*), 10 alarms, and 1 million API requests each month at no additional charge.
- New and existing customers also receive 5 GB of data ingestion and 5 GB of archived storage per month at no additional charge.

Each domain that you want to check requires firing a periodic event which is charged at $1.00/1M.
If you were to max out the free Lambda calls with 1M checks in a month this would cost you $1.
Each domain requires an alarm, the first 10 of which are free.


SNS
___

http://aws.amazon.com/sns/pricing/

- First 1 million Amazon SNS requests per month are free
- Free deliveries
  - Mobile Push Notifications: 1 million
  - SMS: 100
  - Email: 1,000
  - HTTP(s): 100,000

If you choose to have notifications on changes to the alarm state then you can be
charged for the delivery of those notifications. If you are only notified when
the site is down and it doesn't go down every day then you should have enough
for SMS or email to be free each month.


Total Cost
__________

Overall, the usage for a single site checked every 5 mins should be free. Checking
every 5 mins requires ~8,640 CloudWatch events which cost $1 per million. Assuming
that it doesn't generate multiple emails/SMS alerts on every check those should
stay under the monthly limits or cost you $0.01/month with rounding up.

You should refer to the AWS documentation to see the most up to date usage
tiers and pricing.


License
-------

This is free software distributed under the included
`BSD license <https://github.com/mlavin/cloudping/blob/master/LICENSE.rst>`_. You
are free to copy, modify, and redistribute under the terms listed there. Please
note that this is provide "as-is" without warranty. You are responsible for any
changes that using this software might generate on your AWS account.
