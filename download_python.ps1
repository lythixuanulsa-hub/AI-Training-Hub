[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
[Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile "python_installer.exe"
Start-Process -FilePath ".\python_installer.exe" -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0" -Wait
