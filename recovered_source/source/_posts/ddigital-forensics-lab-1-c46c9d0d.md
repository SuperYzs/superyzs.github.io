---
title: "Ddigital-Forensics-Lab-1"
date: "2024-03-16T15:15:57.000Z"
updated: "2024-03-17T10:01:33.174Z"
description: "理解计算机是如何存储和处理数据的。"
categories:
  - 计算机取证学
tags:
  - Linux
  - C
---

<h1 id="实验目的">实验目的</h1>
<p>理解计算机是如何存储和处理数据的。</p>
<h1 id="实验环境">实验环境</h1>
<p>安装有kali linux的虚拟机、可以编译C程序。</p>
<h1 id="实验步骤">实验步骤</h1>
<h2 id="task1">Task1</h2>
<p>1、输入<code>touch Task1.c</code> 指令在桌面创造一个空的C语言文件。</p>
<p>2、输入<code>gedit Task1.c</code> 指令使用gedit编辑器打开Task1.c文件。</p>
<p>3、输入<code>gcc Task1.c -o Task1.out</code> 指令编译Task1.c文件，生成Task1.out文件。</p>
<p>4、输入<code>./Task1.out</code> 指令运行Task1.out文件。</p>
<p>5、将显示结果记录到记录表1中。</p>
<table>
<thead>
<tr>
<th style="text-align:center">变量类型</th>
<th style="text-align:center">参数类型</th>
<th style="text-align:center">字节数</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center"><a href="http://student1.id">student1.id</a></td>
<td style="text-align:center">100</td>
<td style="text-align:center">4</td>
</tr>
<tr>
<td style="text-align:center">student1.province</td>
<td style="text-align:center">101</td>
<td style="text-align:center">3</td>
</tr>
<tr>
<td style="text-align:center">student1.age</td>
<td style="text-align:center">102</td>
<td style="text-align:center">4</td>
</tr>
<tr>
<td style="text-align:center">结构体Student</td>
<td style="text-align:center">104</td>
<td style="text-align:center">12</td>
</tr>
</tbody>
</table>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_1/1.1.png" alt="运行程序得到的结果" /></p>
<h2 id="task2">Task2</h2>
<p>1、输入<code>gcc -g Task1.c -o Task1</code> 指令编译Task1.c文件，生成Task1文件。</p>
<p>2、输入<code>gdb Task1</code> 指令启动gdb。</p>
<p>3、输入<code>break 15</code> 指令在第15行设置断点。</p>
<p>4、输入<code>r</code> 指令运行Task1，程序会在第15行停下来。</p>
<p>5、输入<code>x/4bt &amp;student1.id</code> 指令查看student1.id的内存情况；输入<code>x/4bt &amp;student1.province</code> 指令查看student1.province的内存情况；输入<code>x/4bt &amp;student1.age</code> 指令查看student1.age的内存情况；输入<code>x/4bt &amp;student1</code> 指令查看student1的内存情况。</p>
<p>6、将显示结果记录到记录表1中。</p>
<table>
<thead>
<tr>
<th style="text-align:center">变量</th>
<th style="text-align:center">十六进制值的表示</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center"><a href="http://student1.id">student1.id</a></td>
<td style="text-align:center">0x7fffffffddf4： 10001000 01101111 11111011 00000101</td>
</tr>
<tr>
<td style="text-align:center">student1.province</td>
<td style="text-align:center">0x7fffffffddfc： 00010010 00000000 000000000 00000000</td>
</tr>
<tr>
<td style="text-align:center">student1.age</td>
<td style="text-align:center">0x7fffffffddfc： 00010010 00000000 000000000 00000000</td>
</tr>
<tr>
<td style="text-align:center">结构体Student</td>
<td style="text-align:center">0x7fffffffddf4： 10001000 01101111 11111011 00000101</td>
</tr>
</tbody>
</table>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_1/1.2.png" alt="运行程序得到的结果" /></p>
<h2 id="task3">Task3</h2>
<p>前面步骤都和Task2一致。</p>
<p>1、输入<code>break 10</code> 指令在第10行设置断点。</p>
<p>2、输入<code>r</code> 指令运行Task1，程序会在第10行停下来。</p>
<p>3、输入<code>x/1bx &amp;digits[0]</code> 指令查看digits[0]的内容；输入<code>x/1bx &amp;digits[1]</code> 指令查看digits[1]的内容；输入<code>x/1bx &amp;digits[2]</code> 指令查看digits[2]的内容；输入<code>x/1bx &amp;digits[3]</code> 指令查看digits[3]的内容。</p>
<p>4、将显示结果记录到记录表1中。</p>
<table>
<thead>
<tr>
<th style="text-align:center">数字数组项</th>
<th style="text-align:center">第一项</th>
<th style="text-align:center">第二项</th>
<th style="text-align:center">第三项</th>
<th style="text-align:center">第四项</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">内存地址</td>
<td style="text-align:center">0x7fffffffddf4</td>
<td style="text-align:center">0x7fffffffddf5</td>
<td style="text-align:center">0x7fffffffddf6</td>
<td style="text-align:center">0x7fffffffddf7</td>
</tr>
<tr>
<td style="text-align:center">存储的值</td>
<td style="text-align:center">0x12</td>
<td style="text-align:center">0x34</td>
<td style="text-align:center">0x56</td>
<td style="text-align:center">0x78</td>
</tr>
</tbody>
</table>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_1/1.3.png" alt="运行程序得到的结果" /></p>
