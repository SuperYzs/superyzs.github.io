---
title: "Binary-Instrumentation-Analysis"
date: "2024-06-03T08:20:29.000Z"
updated: "2024-06-04T06:28:21.997Z"
description: "学习一种名为二进制插桩的技术。"
categories:
  - 逆向工程与汇编语言
tags:
  - Linux
---

<h1 id="实验目的">实验目的</h1>
<p>学习一种名为二进制插桩的技术。</p>
<h1 id="实验原理">实验原理</h1>
<p>二进制插桩技术能够在二进制程序的任何位置插入几乎无限的代码，以观察或修改该二进制程序的行为。</p>
<h1 id="实验环境">实验环境</h1>
<p>1. 使用 binary 虚拟机，即在 Lab 2 中已经配置过的环境（包括时间戳）。</p>
<p>2. 实验所需文件位于/home/binary/code/chapter9 目录。</p>
<h1 id="task-1pin-使用入门">Task 1：Pin 使用入门</h1>
<p>步骤：</p>
<p>1、输入 <code>cd /pin/pin-3.6-97554-g31f0a167d-gcc-linux/source/tools/ManualExamples 和 make obj-intel64/inscount0.so TARGET=intel64</code> 指令编译生成 <a href="http://inscount0.so">inscount0.so</a>。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/1.1.png" alt="输出结果" /></p>
<p>2、输入 <code>~/pin/pin-3.6-97554-g31f0a167d-gcc-linux/pin -t obj-intel64/inscount0.so -o obj-intel64/inscount0.log -- /bin/ls</code>指令执行插桩分析，并查看inscount0.log 文件中显示得到执行过的指令总数。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/1.2.png" alt="输出结果" /></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/1.3.png" alt="输出结果" /></p>
<h1 id="task-2profiling-with-pin">Task 2：Profiling with Pin</h1>
<h2 id="331-从起始处分析应用程序">3.3.1 从起始处分析应用程序</h2>
<p>步骤：</p>
<p>1、输入 <code>make obj-intel64/profiler.so TARGET=intel64</code> 指令编译生成 <a href="http://profiler.so">profiler.so</a>。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/2.1.png" alt="输出结果" /></p>
<p>2、输入  <code>~/pin/pin-3.6-97554-g31f0a167d-gcc-linux/pin -t ./profiler/obj-intel64/profiler.so -c -s -- /bin/true</code> 指令对/bin/true执行分析。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/2.2.png" alt="输出结果" /></p>
<h2 id="332-将-profiler-附加到运行中的进程">3.3.2 将 Profiler 附加到运行中的进程</h2>
<p>步骤：</p>
<p>1、输入 <code>echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope</code>指令暂时禁用安全机制；输入 <code>nc -l -u 127.0.0.1 9999</code> 指令获取 PID。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/2.3.png" alt="输出结果" /></p>
<p>2、输入  <code>~/pin/pin-3.6-97554-g31f0a167d-gcc-linux/pin -pid 6594 -t ./profiler/obj-intel64/profiler.so -c -s</code> 指令对 PID 为 6594 的进程执行分析。输入 <code>echo \&quot;Testing the profiler\&quot; \| nc -u 127.0.0.1 9999</code> 指令使用另一个 netcat 进程向监听进程发送消息&quot;Testing the profiler&quot;。使用 <code>fg</code> 命令把 netcat 监听进程带到前台，并终止该进程。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/2.4.png" alt="输出结果" /></p>
<p>Q：根据 Pin 执行结果，使用了哪些系统调用？</p>
<p>A：系统调用 0: read，执行了 2 次，占比 28.57%<br />
系统调用 1: write，执行了 1 次，占比 14.29%<br />
系统调用 7: poll，执行了 2 次，占比 28.57%<br />
系统调用 42: connect，执行了 1 次，占比 14.29%<br />
系统调用 45: recvfrom，执行了 1 次，占比 14.29%</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/2.5.png" alt="输出结果" /></p>
<h1 id="task-3automatic-binary-unpacking-with-pin">Task 3：Automatic Binary Unpacking with Pin</h1>
<h2 id="342-测试脱壳器">3.4.2 测试脱壳器</h2>
<p>步骤：</p>
<p>1、输入 <code>cp /bin/ls packed</code> 和 <code>upx packed</code> 指令对测试二进制文件进行加壳。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.1.png" alt="输出结果" /></p>
<p>2、输入 <code>sudo apt-get install --reinstall libxcb-xinerama0</code>指令安装缺少的运行库，安装IDA。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/2.2.png" alt="输出结果" /></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/2.3.png" alt="输出结果" /></p>
<p>3、在IDA中分析 packed 文件，发现其被加壳。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.4.png" alt="输出结果" /></p>
<p>4、输入  <code>/pin/pin-3.6-97554-g31f0a167d-gcc-linux/pin -t obj-intel64/unpacker.so -- ./packed</code> 指令执行解密。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.5.png" alt="输出结果" /></p>
<p>5、输入 <code>head unpacker.log</code> 指令查看解密后的文件。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.6.png" alt="输出结果" /></p>
<p>6、输入 <code>file unpacked.0x400000-0x41da64_entry-0x40000c</code>指令查看解密后的文件类型。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.7.png" alt="输出结果" /></p>
<p>7、输入 <code>strings unpacked.0x400000-0x41da64_entry-0x40000c</code>指令看到脱壳后的二进制文件中包含许多可读的字符串，这表明脱壳成功。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.9.png" alt="输出结果" /></p>
<p>8、使用IDA在脱壳后的二进制文件中找到更多的函数，这也说明脱壳是成功的。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.10.png" alt="输出结果" /></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.10.1.png" alt="输出结果" /></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.10.2.png" alt="输出结果" /></p>
<p>9、输入 <code>objdump -M intel -d /bin/ls &gt; result_ls</code> 和 <code>objdump -M intel -b binary -mi386 -Mx86-64 -D unpacked.0x400000-0x41da64_entry-0x40000c &gt; result_unpack</code> 指令对比加壳前后的汇编代码.</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.11.png" alt="输出结果" /></p>
<p>以 0x2a00处代码为例进行比较。可以看到除了代码地址不同外，二者其余的代码是相同的。地<br />
址不同是因为 objdump 命令缺少节头表而不知道脱壳的二进制文件的预期加载地址。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Binary%20Instrumentation%20Analysis/3.12.png" alt="输出结果" /></p>
