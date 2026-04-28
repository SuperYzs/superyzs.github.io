---
title: "Ddigital-Forensics-Lab-5"
date: "2024-04-05T16:35:19.000Z"
updated: "2024-04-05T16:44:42.500Z"
description: "使用 winhex 对删除的文件进行恢复。"
categories:
  - 计算机取证学
tags:
  - Windows
---

<h1 id="实验目的">实验目的</h1>
<p>使用 winhex 对删除的文件进行恢复。</p>
<h1 id="实验环境">实验环境</h1>
<p>安装有 winhex 的 windows 系统、shiyan.vhd 文件。</p>
<h1 id="实验步骤">实验步骤</h1>
<p>1、将 shiyan.vhd 挂载到C盘。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_5/1.1.png" alt="将 shiyan.vhd 挂载到C盘" /></p>
<p>2、找到 MFT 中 paper.zip 的位置。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_5/1.2.png" alt="找到 MFT 中 paper.zip 的位置" /></p>
<p>3、ctrl + f 搜索关键词 paper 。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_5/1.3.png" alt="搜索关键词 paper" /></p>
<p>4、在上方复制并查找16进制数值。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_5/1.4.png" alt="复制16进制数值" /></p>
<p>5、由下图可以获取以下消息：文件大小：1226D8(十进制 1189592)；簇数：1123；首簇号：042D(十进制 1069)。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_5/1.5.png" alt="查找16进制数值" /></p>
<p>6、ctrl + g 搜索首簇号的位置。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_5/1.6.png" alt="搜索搜簇号的位置" /></p>
<p>7、alt + g 输入文件大小查找末bit的位置。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_5/1.7.png" alt="查找末bit的位置" /></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_5/1.8.png" alt="末bit的位置" /></p>
<p>8、保存为paper.zip，解压后发现获得了一个PDF文件，恢复成功。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_5/1.9.png" alt="将 shiyan.vhd 挂载到C盘" /></p>
