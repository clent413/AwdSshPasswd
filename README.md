# AWD批量ssh密码修改

# 前言

此项目在Tkitn师傅的项目上进行的一个二次开发，添加图形化页面。

原项目地址如下：

https://github.com/Tkitn/awd_ssh_passwd_modify

本地环境windwos11+3.11.6并未在其他平台进行测试

## 介绍

在大多数awd场景下，初始服务器的账号密码所有队伍均一至，此项目可对普通用户的密码进行批量修改，并可以批量链接自定义执行命令。

## 使用

### awdsshpasswd 

将全场ip保存在ip.txt文件中并与该项目放入同一目录下，填写好内容，开始修改即可。
![image-20241023170439836](https://github.com/user-attachments/assets/eb4a67e8-9093-4956-9d2a-cec073080982)



####  效果

这里本地只开了一台机器，演示其效果。

![image-20241023171102545](https://github.com/user-attachments/assets/e8dbb92f-3e60-472e-96c2-151069421f1a)


### awdsshexec

将全场ip保存在ip.txt文件中并与该项目放入同一目录下，填写好内容（ip可不填写）读取的是ip.txt中的ip，开始即可。
![image-20241023170846674](https://github.com/user-attachments/assets/ae599d05-8217-435b-a9fb-457636f8a47f)



#### 效果

批量链接执行命令

![image-20241023171439953](https://github.com/user-attachments/assets/216d4cf1-fd14-4a5d-8445-6c716cd48534)


# 注

菜鸡随便写着玩，不喜请轻喷。
