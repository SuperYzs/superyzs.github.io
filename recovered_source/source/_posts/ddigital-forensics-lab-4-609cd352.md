---
title: "Ddigital-Forensics-Lab-4"
date: "2024-04-05T08:54:58.000Z"
updated: "2024-04-05T09:15:32.628Z"
description: "FAT 文件系统检验分析和数据恢复。"
categories:
  - 计算机取证学
tags:
  - Linux
---

<h1 id="实验目的">实验目的</h1>
<p>1、了解 FAT 文件系统的工作原理。<br />
2、依据 FAT 文件系统的残留元数据恢复已删除的文件。</p>
<h1 id="实验环境">实验环境</h1>
<p>使用名为&quot;thumbimage_fat.dd&quot;的镜像文件，将其复制到实验环境 kali 中。</p>
<h1 id="实验步骤">实验步骤</h1>
<h2 id="task1">Task1</h2>
<p>输入 <code>mmls thumbimage_fat.dd</code> 指令进行磁盘分析：</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/1.1.png" alt="运行程序得到的结果" /></p>
<table>
<thead>
<tr>
<th style="text-align:center">第一个分区</th>
<th style="text-align:center">属性</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">在扇区中起始位置</td>
<td style="text-align:center">0x0000000097</td>
</tr>
<tr>
<td style="text-align:center">分区中的扇区数</td>
<td style="text-align:center">2482223</td>
</tr>
<tr>
<td style="text-align:center">分区大小 （MB）</td>
<td style="text-align:center">121.25 MB</td>
</tr>
<tr>
<td style="text-align:center">分区类型</td>
<td style="text-align:center">Win95 FAT32（0x0b）</td>
</tr>
</tbody>
</table>
<h2 id="task2">Task2</h2>
<p>使用 <code>dd if=thumbimage_fat.dd of=partition1.dd bs=512 skip=96 count=2482223</code> 指令将第一个分区复制到新的文件中。其中，if=thumbimage_fat.dd指定输入文件为 &quot;thumbimage_fat.dd&quot;，of=partition1.dd指定输出文件为 &quot;of=partition1.dd&quot;，bs=512表示每次读取512字节，skip=96表示跳过前96个扇区，count=2482223表示读取2482223个扇区。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/2.1.png" alt="运行程序得到的结果" /></p>
<h2 id="task3">Task3</h2>
<p>输入 <code>hexdump -C partition1.dd -n 1024</code> 指令来分析第一个分区的引导扇区：</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/3.1.png" alt="运行程序得到的结果" /></p>
<pre><code>   00000000  eb 58 90 4d 53 44 4f 53  35 2e 30 00 02 02 ac 18  |.X.MSDOS5.0.....|
   00000010  02 00 00 00 00 f8 00 00  3f 00 ff 00 61 00 00 00  |........?...a...|
   00000020  9f c9 03 00 aa 03 00 00  00 00 00 00 02 00 00 00  |................|
   00000030  01 00 06 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
   00000040  80 00 29 b9 d3 3d ae 4e  4f 20 4e 41 4d 45 20 20  |..)..=.NO NAME  |
   00000050  20 20 46 41 54 33 32 20  20 20 33 c9 8e d1 bc f4  |  FAT32   3.....|
   00000060  7b 8e c1 8e d9 bd 00 7c  88 4e 02 8a 56 40 b4 41  |&#123;......|.N..V@.A|
</code></pre>
<p>1、FAT 版本:从引导扇区的 0x52 偏移处可以看到 &quot;FAT32 &quot; 字符串,说明这是一个 FAT32 文件系统。</p>
<p>2、保留扇区的大小:从引导扇区的 0x0E 偏移处可以看到保留扇区的数量是 0x18ac,也就是 6316 个扇区。</p>
<p>3、FAT0 的位置:从引导扇区的 0x0E 偏移处可以看到 FAT 区的起始扇区号是 0x18ac,也就是FAT0之前共有6316个扇区，即FAT0的起始地址是第6316个扇区。从引导扇区的 0x16 偏移处可以看到 FAT 表的扇区数是 0x000003aa,也就是每个FAT拥有 938 个扇区，因此FAT0的结束地址为第7253个扇区，因此FAT0的位置为6316-7253个扇区。</p>
<p>4、FAT 的备份数量:从引导扇区的 0x10 偏移处可以看到 FAT 表的备份数是 0x02,也就是 2 个备份。</p>
<p>5、根目录的位置:从引导扇区的 0x2C 偏移处可以看到根目录的起始簇号是 0x00000002,也就是第 2 个簇。从引导扇区的0x0D 偏移处可以看到有 2 个FAT。从引导扇区的 0x0E 偏移处可以看到 FAT 区的起始扇区号是 0x18ac,也就是FAT0之前共有6316个扇区，即FAT0的起始地址是第6316个扇区。从引导扇区的 0x16 偏移处可以看到 FAT 表的扇区数是 0x000003aa,也就是每个FAT拥有 938 个扇区。因此根目录的起始地址为6316 + 938 * 2 = 8192，即第8192个扇区。因此根目录的位置为第2簇，第8192-8193个扇区。</p>
<p>6、簇的大小:从引导扇区的 0x0D 偏移处可以看到每个簇的扇区数为 0x02，也就是 2，每个扇区的大小为 512 kb，因此簇的大小为 1 kb（1024 bytes）。</p>
<p>7、数据区的位置:从根目录 8192。因此数据区的起始位置为第8192个扇区，结束位置为第 248222 个扇区。总簇数为（248222-8192）/2=120015，因此数据区的位置为第 2-120017 个簇。</p>
<p>8、卷标签:从引导扇区的 0x47 偏移处可以看到卷标签是 &quot;NO NAME &quot;。</p>
<p>9、文件系统的扇区数:从引导扇区的 0x20 偏移处可以看到总扇区数是 0x0003c99f,也就是 248223 个扇区。</p>
<p><a href="https://blog.csdn.net/yangyang031213/article/details/79030247">参考文章</a></p>
<p>后来发现了另一种方法（在实验2中）：</p>
<p>输入指令 <code>fsstat partition1.dd</code>：</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/3.2.png" alt="运行程序得到的结果" /></p>
<pre><code>FILE SYSTEM INFORMATION
--------------------------------------------
File System Type: FAT32

OEM Name: MSDOS5.0
Volume ID: 0xae3dd3b9
Volume Label (Boot Sector): NO NAME    
Volume Label (Root Directory):
File System Type Label: FAT32   
Next Free Sector (FS Info): 8236
Free Sector Count (FS Info): 239986

Sectors before file system: 97

File System Layout (in sectors)
Total Range: 0 - 248222
* Reserved: 0 - 6315
** Boot Sector: 0
** FS Info Sector: 1
** Backup Boot Sector: 6
* FAT 0: 6316 - 7253
* FAT 1: 7254 - 8191
* Data Area: 8192 - 248222
** Cluster Area: 8192 - 248221
*** Root Directory: 8192 - 8193
** Non-clustered: 248222 - 248222

METADATA INFORMATION
--------------------------------------------
Range: 2 - 3840502
Root Directory: 2

CONTENT INFORMATION
--------------------------------------------
Sector Size: 512
Cluster Size: 1024
Total Cluster Range: 2 - 120016

FAT CONTENTS (in sectors)
--------------------------------------------
8192-8193 (2) -&gt; EOF
8194-8211 (18) -&gt; EOF
8214-8237 (24) -&gt; EOF
</code></pre>
<p>从输出结果中可以直接得出：</p>
<p>1、FAT版本：FAT32。</p>
<p>2、保留扇区的大小：6316个扇区。</p>
<p>3、FAT0的位置：6316-7253个扇区。</p>
<p>4、FAT的备份数量：2个备份。</p>
<p>5、根目录的位置：第2个簇，第8192-8193个扇区。</p>
<p>6、簇的大小：1 kb（1024 bytes）。</p>
<p>7、数据区的位置：第 2-120017 个簇。</p>
<p>8、卷标签：NO NAME。</p>
<p>9、文件系统的扇区数：248223个扇区。</p>
<h2 id="task4">Task4</h2>
<p>输入 <code>stat -c '%b %s' readme.txt</code> 指令获取 readme.txt 文件的信息，其中 %b4 获取 readme.txt 的文件扇区数，%s 获取 readme.txt 的文件大小。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/4.1.png" alt="运行程序得到的结果" /></p>
<p>1、文件大小（十进制）单位：8827。</p>
<p>2、起始簇号（十进制）：3。</p>
<p>3、起始扇区地址（十进制）。注意，需要将簇号转换为扇区地址：8194。</p>
<p>4、分配给文件&quot;readme.txt&quot;的簇数：扇区数为18，一个簇包含两个扇区，因此簇数为9。</p>
<p>5、分配给文件&quot;readme.txt&quot;的扇区数：18。</p>
<p>6、按顺序列出分配给文件&quot;readme.txt&quot;的簇链：3，4，5，6，7，8，9，10，11。</p>
<h2 id="task5">Task5</h2>
<p>1、输入 <code>cd /mnt</code> 指令切换到/mnt 目录，并输入 <code>sudo mkdir forensics</code> 指令创建一个名为&quot;forensics&quot;的目录。</p>
<p>2、输入 <code>sudo mount -o rw /home/kali/Desktop/partition1.dd /mnt/forensics</code> 指令将第二题提取的 FAT 分区挂载到具有读写访问权限的/mnt/forensics 目录下。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/5.1.png" alt="运行程序得到的结果" /></p>
<p>3、输入 <code>cd /mnt/forensics</code> 指令切换到&quot;/mnt/forensics&quot;目录，然后输入 <code>sudo rm -f readme.txt</code> 指令删除 readme.txt 文件。</p>
<p>4、输入 <code>sudo umount /mnt/forensics</code> 指令卸载已挂载的 FAT 分区。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/5.2.png" alt="运行程序得到的结果" /></p>
<h2 id="task6">Task6</h2>
<p>步骤：</p>
<p>1、输入 <code>dd if=partition1.dd of=fat0.dd bs=512 skip=6316 count=1</code> 指令将 partition1.dd 的 fat0 的部分存储到 fat0.dd 文件中，输入 <code>ghex fat0.dd</code> 修改为下图所示：</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/6.1.png" alt="运行程序得到的结果" /><br />
<img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/6.2.png" alt="运行程序得到的结果" /></p>
<p>2、输入 <code>dd if=partition1.dd of=rootdir.dd bs=512 skip=8192 count=1</code> 指令将 partition1.dd 的第3个簇的部分存储到 rootdir.dd 文件中，输入 <code>ghex rootdir.dd</code> 修改为下图所示：</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/6.3.png" alt="运行程序得到的结果" /><br />
<img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/6.4.png" alt="运行程序得到的结果" /></p>
<p>3、输入 <code>dd if=partition1.dd of=recover.dd bs=512 skip=0 count=6316</code> ；<br />
<code>dd if=fat0.dd bs=512 skip=0 count=1 &gt;&gt;recover.dd</code> ；<code>dd if=partition1.dd bs=512 skip=6317 count=1875 &gt;&gt;recover.dd</code> ；<code>dd if=rootdir.dd bs=512 skip=0 count=1 &gt;&gt;recover.dd</code> ；<code>dd if=partition1.dd bs=512 skip=8193 count=240030 &gt;&gt;recover.dd</code> 指令，将所有文件整合在一起。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/6.5.png" alt="运行程序得到的结果" /><br />
<img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/6.6.png" alt="运行程序得到的结果" /></p>
<p>4、输入 <code>sudo mount -o rw /home/kali/Desktop/recover.dd /mnt/forensics</code> 将 recover.dd 挂载到 /mnt/forensics 目录下；输入 <code>cd /mnt/forensics</code> 进入到该目录下；输入 <code>ls</code> 发现readme.txt 文件已经恢复。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/6.7.png" alt="运行程序得到的结果" /><br />
<img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Digital%20Forensics/Lab_4/6.8.png" alt="运行程序得到的结果" /></p>
