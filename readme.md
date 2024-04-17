# Log

## change serial

由于树莓派串口默认用于终端调试，如需使用串口，则需要修改树莓派设置。执行如下命令进入树莓派配置：

```
sudo raspi-config
```

选择 Interfacing Options ->Serial ->no -> yes，关闭串口调试功能。 [![A7600C1-Cat-Hat-OpenSerial.jpg](https://www.waveshare.net/w/upload/thumb/f/f7/A7600C1-Cat-Hat-OpenSerial.jpg/800px-A7600C1-Cat-Hat-OpenSerial.jpg)](https://www.waveshare.net/wiki/%E6%96%87%E4%BB%B6:A7600C1-Cat-Hat-OpenSerial.jpg)
需要重启

```
sudo reboot
```

打开/boot/config.txt 文件，找到如下配置语句使能串口，如果没有，可添加在文件最后面：

```
enable_uart=1
```

[ref](https://blog.csdn.net/Mark_md/article/details/107181151)

`sudo vi /boot/config.txt`

末尾添加一行：dtoverlay=pi3-miniuart-bt
