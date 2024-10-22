AWS Beanstalk is a Paas provider in which Beanstalk platform is creating a EC2 server 
and launching a server

For CICD pipeline development , use AWS Code Pipeline for CodeBuild and CodeDeploy using s3 Artifacts and we want to configure the Project with buildspec.yml and Procfile in Github . buildspec.yml contain docker compose code to build it using docker image and container which we have to configure with buildspec.yml. 

In Procfile , Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model ported from Ruby's Unicorn project. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resource usage, and fairly speedy.

adding necessary Libraries in requirements.txt




CICD
![CI/CD Pipeline](https://raw.githubusercontent.com/VikasSivashankaran/AWS_Beanstalk_CICD_Pipeline/main/cicdaws.jpg)