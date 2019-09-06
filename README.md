# AkrnightsSimulatorHelper.exe
Arknights Simulator Helper | 基于python鼠标控制的明日方舟模拟器护肝助手

![](img/md_gui.png)

## 1. 特性

* 采用相对坐标，兼容各类模拟器
* 控制鼠标进行挂机操作(运行时请不要操作电脑，适合睡前点开挂机)
* 无需安装安卓ADB工具和Python各种包，exe文件点开即用
* 脚本操作与程序分离，将脚本文件拷到Scripts文件夹内即可运行
* **以上功能均没有实现**

## 2. Todo
* [x] 界面制作
* [ ] 相对坐标坐标系计算
* [ ] 图片匹配
* [ ] 配置文件读写(记住目前模拟器的尺寸)
* [ ] 脚本解释器
* [ ] 脚本编辑器

## 3. 脚本说明
脚本采用以.ark为后缀的文件夹，里面包含img文件夹，run脚本+说明文件组成。img文件夹存放该脚本需要用到的截图，如开始，返回等按钮的截图等，类似于sikulix

![](img/md_script.png)

需要在程序内部集成运行解释器，还需要另写一个脚本编辑器方便大家自己写脚本

> 为什么不直接用sikulix? 因为想搞一个绿色的exe，不需要安装额外的依赖，减少使用难度

## 4. 开发相关
本项目使用pipenv进行依赖管理，保证python>=3.6安装在电脑上之后，进入项目目录

```cmd
C:\...\ArknightsLiverHelper.exe>pip install pipenv
```

### 4.1 初始化安装环境
在默认路径下(`我的文档\.virtualenv\`)创建虚拟环境
```cmd
C:\...\ArknightsLiverHelper.exe>pipenv install
```
（pipenv install --target dist 启用日，家祭勿忘告乃翁）

### 4.2 更新安装环境
如果之前初始化过，但是github上又增加了新的依赖，需要同步更新的话，只需要
```cmd
C:\...\ArknightsLiverHelper.exe>pipenv sync
```

### 4.3 运行
**方法一：**直接运行
```cmd
C:\...\ArknightsLiverHelper.exe>pipenv run app.py
```
> 注意，直接python app.py会使用默认的，而不是该项目的虚拟环境，详情请了解Pipenv的其他教程

**方法二：**启用虚拟环境shell
```cmd
C:\...\ArknightsLiverHelper.exe>pipenv shell
（venv-randomcode）C:\...\ArknightsLiverHelper.exe>python app.py
```
**方法三：**pycharm中加载该pipenv，直接调试

> [https://www.jetbrains.com/help/pycharm/pipenv.html]

### 4.4 打包
Pyqt5 == 5.12.1保证打包成功

> https://github.com/pyinstaller/pyinstaller/issues/4293
