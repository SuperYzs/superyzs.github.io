---
title: "Ddigital-Forensics-Lab-2"
date: "2024-03-16T15:44:26.000Z"
updated: "2024-03-19T07:49:22.017Z"
description: "学会使用TSK工具对磁盘镜像进行电子数据校验。"
categories:
  - 计算机取证学
tags:
  - Linux
  - C
---

<h1 id="实验目的">实验目的</h1>
<p>学会使用TSK工具对磁盘镜像进行电子数据校验。</p>
<h1 id="实验环境">实验环境</h1>
<p>安装有kali linux的虚拟机、磁盘镜像文件dfr-11-mft-ntfs.dd.bz2。</p>
<h1 id="实验步骤">实验步骤</h1>
<p>1、使用bzip2命令解压文件 dfr-11-mft-ntfs.dd.bz2 <code>bzip2 -d dfr-11-mft-ntfs.dd.bz2</code></p>
<p>2、使用mmls命令查看磁盘镜像的分区布局，将相关信息记录下来 <code>mmls -t dos dfr-11-mft-ntfs.dd</code>。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_2/1.1.png" alt="运行程序得到的结果" /></p>
<p>3、使用dcfldd命令从磁盘镜像中提取分区镜像 <code>dcfldd if=dfr-11-mft-ntfs.dd bs=512 skip=128 count=2091008 of=ntfs.dd</code></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_2/1.2.png" alt="运行程序得到的结果" /></p>
<p>4、使用fsstat命令显示分区中文件系统的详细信息，查看磁盘详细信息 <code>fsstat -f ntfs ntfs.dd</code></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_2/1.3.png" alt="运行程序得到的结果" /></p>
<p>5、使用fls命令来解析文件系统。-r选项用于递归遍历所有目录 <code>fls -r ntfs.dd</code></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_2/1.4.png" alt="运行程序得到的结果" /></p>
<p>6、使用fls命令显示已删除的文件和目录 <code>fls -r -d ntfs.dd</code></p>
<p>7、使用icat命令恢复被删除的文件，-r表示如果文件被删除，icat将使用文件恢复技术。数字41是被删除文件对应的MFT表项编号，这里的41是Sheliak.txt这个文件对应的。恢复的文件保存到以前缀recovered_开头的文件中 <code>icat -r ntfs.dd 41\&gt;recovered_文件名</code></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_2/1.5.png" alt="运行程序得到的结果" /></p>
<p>8、使用cat命令显示恢复的文件 <code>cat recovered_文件名</code></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_2/1.6.png" alt="运行程序得到的结果" /></p>
<h1 id="试验记录">试验记录</h1>
<table>
<thead>
<tr>
<th>分区的起始扇区地址和分区结束扇区地址</th>
<th>分区的起始扇区地址：0000000128 分区的结束扇区地址：0002091135</th>
</tr>
</thead>
<tbody>
<tr>
<td>分区中文件系统详细信息</td>
<td>FILE SYSTEM INFORMATION -------------------------------------------- File System Type: NTFS Volume Serial Number: 2ACADB0FCADAD5E3 OEM Name: NTFS Volume Name: ntfs Version: Windows XP</td>
</tr>
<tr>
<td>被删除的文件名称（3个）</td>
<td>Sheliak.txt,Vega.txt,Sulafat.txt</td>
</tr>
</tbody>
</table>
