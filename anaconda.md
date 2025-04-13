

`conda create -n env_name python=3.8.12`

`conda env list`

`conda activate env_name`

`conda list`    #查看当前环境下安装的库

`conda search package_name`  

`conda install package_name`

`conda update package_name`

`pip install --default-timeout=1000 -r a/path/to/requirements.txt`   #安装依赖

`conda install  --yes --file requirements.txt`   #安装时，超时时间要长一点

`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

`pip install 包名 -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com`

`pip install -r requirements.txt -i https://pypi.douban.com/simple/ --trusted-host pypi.douban.com`

