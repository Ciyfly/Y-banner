# Y-banner  
## 使用
`pip install -r requirements.txt`  
`python main.py -d domain`  
`python main.py -f domain.txt`
会在当前目录生成 `output`目录 里面目录会以时间戳作为当前测试目录 生成report.html 作为报告展示  

## 实现
使用 selenium + 线程池的形式实现  
selenium的驱动是在`config`目录下chromediver  
建议使用 windows来测试使用 如果linux有那么高的内存当然也可以  

## 测试
目前是测试基本版本 有bug欢迎来提 谢谢





