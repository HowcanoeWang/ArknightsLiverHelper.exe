# AkrnightsSimulatorHelper.exe
Arknights Simulator Helper | 基于python鼠标控制的明日方舟模拟器护肝助手

![](img/md_gui.png)

## 特性

* 采用相对坐标，兼容各类模拟器
* 控制鼠标进行挂机操作(运行时请不要操作电脑，适合睡前点开挂机)
* 无需安装安卓ADB工具和Python各种包，exe文件点开即用
* 脚本操作与程序分离，将脚本文件拷到Scripts文件夹内即可运行
* **以上功能均没有实现**

## Todo
* [x] 界面制作
* [ ] 相对坐标坐标系计算
* [ ] 图片匹配
* [ ] 配置文件读写(记住目前模拟器的尺寸)
* [ ] 脚本解释器
* [ ] 脚本编辑器

## 脚本说明
脚本采用以.ark为后缀的文件夹，里面包含img文件夹，run脚本+说明文件组成。img文件夹存放该脚本需要用到的截图，如开始，返回等按钮的截图等，类似于sikulix

![](img/md_script.png)

需要在程序内部集成运行解释器，还需要另写一个脚本编辑器方便大家自己写脚本

> 为什么不直接用sikulix? 因为想搞一个绿色的exe，不需要安装额外的依赖，减少使用难度

## 打包
Pyqt5 == 5.12.1保证打包成功
> https://github.com/pyinstaller/pyinstaller/issues/4293