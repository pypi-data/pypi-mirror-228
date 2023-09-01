## Requirements:
`conda env create -f environment.yml`

## Usage
在`server_register.py`里登记提供的设备型号和显存大小。  
例如```device = "NVIDIA GTX 1080Ti", device_mem = "11GB"```  

在`antgrid.pku.edu.cn`完成注册，拿到用户名和密码。  
使用命令`python server_register.py -u <用户名> -p <密码>`即可加入AntGrid算力池。


## Notice
模型使用<b>Huggingface repo</b>作为CDN，部分参数文件较大，下载时间取决于网络环境。