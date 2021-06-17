常用命令总结(Common Commands)

### Download Google Drive file when using Kaggle Notebook:
- Use gdown(Very efficient!)
- example ```!gdown https://drive.google.com/uc?id=15kJ8cY63wUwiMstHZ5wsX4_JFLnLJTjZ```
- Other Usage: 
```python
!pip install gdown
import gdown 
url = 'https://drive.google.com/uc?id=1Z2cVU3lBWExu2zw7aQX47vGF5a4K4X-T' output = 'new-data.csv' 
gdown.download(url, output, quiet=False)
```

#### ls -laSh:
- List file size
- laSh具体含义:output all(a) the file sizes(S) in human-readable(h) format 

#### tar -xvf
- unzip .tar or .tar.gz file
- x means extract and v means verbose f means tar file
- alternative: **!gzip** -d FILENAME.tar.gz
