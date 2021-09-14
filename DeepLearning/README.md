## Awesome Course/Material
https://fleuret.org/

## Awesome Project
### Image Captioning
- 带注意力机制的看图说话: https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Image-Captioning
### Bert
词库外的词汇: https://medium.com/@pierre_guillou/nlp-how-to-add-a-domain-specific-vocabulary-new-tokens-to-a-subword-tokenizer-already-trained-33ab15613a41

## 常用命令总结(Common Commands)

### Download Tricks
#### Download Google Drive file when using Kaggle Notebook:
- Use gdown(Very efficient!)
- example ```!gdown https://drive.google.com/uc?id=15kJ8cY63wUwiMstHZ5wsX4_JFLnLJTjZ```
- Other Usage: 
```python
!pip install gdown
import gdown 
url = 'https://drive.google.com/uc?id=1Z2cVU3lBWExu2zw7aQX47vGF5a4K4X-T' output = 'new-data.csv' 
gdown.download(url, output, quiet=False)
```
### Linux Command
#### ls -laSh:
- List file size
- laSh具体含义:output all(a) the file sizes(S) in human-readable(h) format 

#### tar -xvf
- unzip .tar or .tar.gz file
- x means extract and v means verbose f means tar file
<!-- - alternative: **!gzip** -d FILENAME.tar.gz -->
