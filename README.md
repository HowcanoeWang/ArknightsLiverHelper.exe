# AkrnightsSimulatorHelper.exe
Arknights Simulator Helper | 基于python鼠标控制的明日方舟模拟器护肝助手

![](img/md_gui.png)

## 1. 特性

* 采用相对坐标，兼容各类模拟器(**需要将模拟器分辨率设置为1600x900**)
* 控制鼠标进行挂机操作(运行时请不要操作电脑，适合睡前点开挂机)
* 无需安装安卓ADB工具和Python各种包，exe文件点开即用
* 脚本操作与程序分离，将脚本文件拷到Scripts文件夹内即可运行

## 2. Todo
* [x] 界面制作
* [x] 相对坐标坐标系计算
* [x] 图片匹配
* [ ] 多样性脚本开发
* [ ] 脚本任务列表
* [ ] 加载脚本时，显示脚本readme.md文件

## 3. 脚本说明
脚本采用以.ark为后缀的文件夹，里面包含img文件夹，run脚本+说明文件组成。img文件夹存放该脚本需要用到的截图，
如开始，返回等按钮的截图等（需要在1600*900模拟器分辨率下截图）

脚本示例(见Scripts文件夹)：`repeat.ark`  
|- img/*  
|- readme.md  
|- run.ash

```python
set_skip_img('network_err1.png')
click('st1_blue.png | st1_pink.png')
click('st2.png')
click('mission_accomplish.png', frequency=7)
```

### 3.1 函数说明

`set_skip_img(img_name)`: 如果出现了如下的图片，

|network_err1|level_up|
|---|---|
|![](img/network_err1.png)|![等级提升]()|

则简单的点击屏幕跳过即可，不影响后续操作

`set_stop_img(img_name)`:如果出现了如下的图片，如网络错误，需要退出重新登陆的，中断当前的脚本

`click(img_name, frequency)`:点击图片，中间用` | `分隔开为只要存在两张之一，就点击，前面的图片优先

|蓝色的开始按钮|粉色的开始按钮|
|---|---|
|![](img/st1_blue.png)|![](img/st1_pink.png)|

frequency参数为没找到的情况下，再次寻找的等待时间，默认2s

### 3.2 所有脚本可用函数

1. `set_skip_img(img_name)`  
    输入
    
    * `img_name`: string, 使用` | `表示“或”逻辑  
    
    输出  
    
    * `None`
    
2. `set_stop_img(img_name)`  
    输入
    
    * `img_name`: string, 使用` | `表示“或”逻辑  
    
    输出  
    
    * `None`
    
3. `click(img_name, frequency=2)`  
    输入
    
    * `img_name`: string, 使用` | `表示“或”逻辑  
    * `frequency`: int, 再次寻找等待时间，单位秒
    
    输出  
    
    * `None`

4. `click_pos(x, y, sleep_time=0)`
    输入
    
    * `x`: float, 相对横坐标[0, 1]
    * `y`: float, 相对宗坐标[0, 1]
    * `sleep_time`: int, 等待x秒后,点击相对位置
    
    输出  
    
    * `None`

4. `img_exist(img_name)`
    输入
    
    * `img_name`: string, 使用` | `表示“或”逻辑  
    
    输出
    
    * `boolean`: True->再界面上存在; False->界面上不存在
5. Python的关键词
    `if...else...`
    尽量使用上面的关键词进行脚本编写

## 4. 软件开发相关
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
