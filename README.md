## RoboHost - ReadMe

Group Members:         
Jaicie Smallwood  
Miriam Harb  
Adam Juwaied  
Robert Guy  
Brandon Woods  
Robert Johnson  

This document contains the sequence of steps for running RoboHost locally. It assumes that  
you are running **Python 3.x**, have **git** installed and have access to a **Linux** shell.

## Cloning RoboHost

The first step towards cloning RoboHost is to make an empty directory (name is not important), such as:

```
mkdir robohost_local
```

Secondly, you will need to initialize an empty repository using git.

```
git init
```

Next, you will need to clone the **main** branch from the GitLab repository.

```
git clone -b main https://gitlab.cs.ecu.edu/csci-4230-spring-2022/section-002/electronic-hostess/robohost.git
```

## Installing Dependencies

A **requirements.txt** file is provided in our repository. Dependencies are explicitly stated in this file and they
may all be installed as follows:

```
pip install -r requirements.txt
```

## Final Steps and Running RoboHost

The repository contains a subdirectory that is labeled **robohost**. You will need to navigate to this directory.

```
cd robohost
```

Subsequently, you will want to export an environment variable that specifies where the execution point file for the  
Flask server is located. This file is **app.py** and it is located in the directory that you are now in. Export the
variable as follows:

```
export FLASK_APP=app.py
```

Lastly, you can run the application from here by issuing the following command:

```
flask run
```

By default, this runs the server on host - **127.0.0.1** and port - **5000**. If these configurations
are occupied on your system you may need to modify this behavior. You can do that as follows:

```
flask run -h <host_name> -p <port_number>
```

Where **<host_name>** is the targeted host and **<port_number>** is the port that you would like the server
to listen on.

Lastly, you may navigate to the index page of our application at the following URL:  

http://<host_name>:<port_number>  
