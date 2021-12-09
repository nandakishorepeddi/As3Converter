# To run this Orcherator 
Use: <python3.9 ProgrammableBIGIPOrchestrator.py>


#Example:
Start Server and then send JSON request using client
- Send Json Request from client:
```
host  ~/PycharmProjects/hackathon/pboctl/pboctl   main  ./pboctl push -f sampleRequests/requestmultiple.json
Config File ".pbo" Not Found in "[/Users/nanda]"
[2021-12-09 19:01:14]  INFO pboctl client initiated
[2021-12-09 19:01:14]  INFO Extracted Configuration from:sampleRequests/requestmultiple.json
[2021-12-09 19:01:14]  INFO Pushing Configuration to BIGIP:127.0.0.1
^[[OSuccesfully Pushed Configuration
```
- Start Server:
```sh
# python server.py
```
- Start Redis
```sh
# docker run --name=redis-pbo --publish=6379:6379 --hostname=redis --restart=on-failure --detach redis:latest
```
- Start Celery Worker
```sh
# celery -A server.celery worker --loglevel=INFO
```
