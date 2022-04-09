
# SFU CMPT 756 project directory of team AngelaBaby

This is the course repo for CMPT 756 (Spring 2022) of team AngelaBaby.


## Directory Structure


## Prerequisite

~~~
# fill in all the required values in `tpl-vars.txt`.
$ cp cluster/tpl-vars-blank.txt cluster/tpl-vars.txt 
$ echo $your_github_token > cluster/ghcr.io-token.txt
$ make -f k8s-tpl.mak templates
~~~
If you have `~/.aws/config` in your local machine, please make sure the region in this file is the same with the one of `cluster/tpl-vars.txt`.


## Deployment
### 1. Ensure AWS DynamoDB is accessible/running

Regardless of where your cluster will run, it uses AWS DynamoDB
for its backend database. Check that you have the necessary tables
installed by running

~~~
$ make -f k8s.mak ls-tables
~~~

The resulting output should include tables `User`, `Music` and `Playlist`. If it isn't, You can clean the old ones and init new tables.

~~~
$ make -f k8s.mak dynamodb-clean
# wait 30 seconds
$ make -f k8s.mak dynamodb-init
~~~

### 2. Start up an Amazon EKS cluster

~~~
$ make -f eks.mak start
~~~
This is a slow operation, often taking 10–15 minutes

### 3. Create namespace 

~~~
$ kubectl config use-context aws756
$ kubectl create ns c756ns
$ kubectl config set-context aws756 --namespace=c756ns
~~~

### 4. Installing the service mesh istio and tunneling into your cluster in the cloud

To install Istio and label the c756ns namespace:

~~~
$ kubectl config use-context aws756
$ istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
$ kubectl label namespace c756ns istio-injection=enabled
$ kubectl get svc --all-namespaces | cut -c -140
~~~

### 5. Building your images
In this step, you will build four services, db, s1, s2 and s3. 

~~~
$ make -f k8s.mak cri
~~~

There is one manual step left before the system can come up auto-magically: **to switch your container repositories to public access.** 


### 6. Deploying all the services

~~~
$ make -f k8s.mak gw db s1 s2 s3
~~~

### 7. Check the logs of the services
~~~
$ k9s -n c756ns
~~~
If you deploy the services successfully, you'd get a lot of `200` status code for the requests to the services.
<img src="media/ts1.png" width="80%" height="80%" />
<img src="media/ts2.png" width="80%" height="80%" />
<img src="media/ts3.png" width="80%" height="80%" />

### 8. Test your Api

~~~
# get the external ip address
kubectl -n istio-system get service istio-ingressgateway | cut -c -140
~~~
Then your APIs are
```
http://external-ip-address:80/api/v1/user/
http://external-ip-address:80/api/v1/music/
http://external-ip-address:80/api/v1/playlist/
```

Try to send a `create_playlist` to the playlist service by postman. In normal case, you'd get a `200` return status code and a `playlist_id`.

<img src="media/ts4.png" width="80%" height="80%" />



## Gatling



