# Google Drive Backup Cleaner

## Service Account
```(bash)
cp service_account-example.json service_account.json
```
Then Create your service account in Google Cloud Console with **Google Drive API** Enabled.

## Commands
1. ```poetry install```
2. ```poetry run python main.py```

## Run as systemd service

1. Create file
```(bash)
sudo nano /etc/systemd/system/backupcleaner.service
```

2. Add content
```(bash)
[Unit]
Description=BackupCleaner service
After=network.target

[Service]
User=username
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/poetry/bin:$PATH"
ExecStart=/path/to/poetry/bin/poetry poetry run python main.py

[Install]
WantedBy=multi-user.target
```

3. Enable and start systemd daemon
```(bash)
sudo systemctl enable backupcleaner
sudo systemctl start backupcleaner
```

4. Check status
```(bash)
sudo systemctl status backupcleaner
```

5. Check logs
```(bash)
sudo journalctl -u backupcleaner
```