# jota-jboss-deployer

Deploy to remote **Jboss EAP6.x+** via HTTP management API using the great **Python Requests library**. I decided to write it in Python mainly because its multiplatform, so you can launch the script in UNIX/Linux, MacOS or even Windows.

Written in Python 3

### Standalone deployment
The usage is very easy, the script takes 4 arguments. Here is an example:
```
./jota-standalone-deployer.py admin admin01 http://192.168.2.131:9990 /repository/packages/example.war
```
Where:

* admin is the name of the user with admin privileges
* admin01 is the password for that user
* http://192.168.2.131:9990 is the destination management URL
* /repository/packages/example.war is the location of the package in local machine

Once launched, **example.war** should be deployed in the remote standalone Jboss node.

### Domain deployment

The script just needs one more argument specifying the target Server Group where you want to deploy the package. Here is an example:
```
./jota-domain-deployer.py admin admin01 http://192.168.2.131:9990 /repository/packages/example.war my-server-group
```
Where:

* admin is the name of the user with admin privileges
* admin01 is the password for that user
* http://192.168.2.131:9990 is the destination management URL
* /repository/packages/example.war is the location of the package in local machine
* my-server-group is the name of the target Server Group

Once launched, **example.war** should be deployed in the remote Jboss Server Group.