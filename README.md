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
```
(venv37)  ✘host  ~/PycharmProjects/As3Converter   main  python3.9 ProgrammableBIGIPOrchestrator.py
^[[O127.0.0.1 - - [09/Dec/2021 19:01:14] "POST / HTTP/1.1" 200 -
Received request

Processing request of BIGIP:10.145.69.216
Pushed successfully to BIGIP: 10.145.69.216


Processing request
BIGIP 10.145.251.1 is not alive


Processing request of BIGIP:10.144.75.221
Pushed successfully to BIGIP: 10.144.75.221
```