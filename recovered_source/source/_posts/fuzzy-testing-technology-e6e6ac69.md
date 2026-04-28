---
title: "Fuzzy-Testing-Technology"
date: "2024-06-03T08:39:03.000Z"
updated: "2024-06-03T08:58:39.337Z"
description: "学习模糊测试的基本理论和操作技巧；深入理解模糊测试在现代软件开发中的实际应用，特别是在提高软件安全性方面的重要作用。"
categories:
  - 逆向工程与汇编语言
tags:
  - Linux
---

<h1 id="实验目的">实验目的</h1>
<p>1、学习模糊测试的基本理论和操作技巧</p>
<p>2、深入理解模糊测试在现代软件开发中的实际应用，特别是在提高软件安全性方面的重要作用。</p>
<h1 id="实验原理">实验原理</h1>
<p>模糊测试是一种自动化的软件测试技术，通过对程序输入进行随机变异生成大量的测试数据，以此检测程序在非预期输入下的行为，尤其是安全漏洞。American Fuzzy Lop（AFL）是一种流行的模糊测试工具，采用编译时插桩技术和遗传算法优化测试用例生成过程，提高了测试的效率和覆盖率。基于 AFL 的进一步发展，AFL++ 引入了新的优化和功能扩展，能更有效地支持大型项目的模糊测试需求。</p>
<h1 id="实验环境">实验环境</h1>
<p>SEED Labs 2.0（64 位版）虚拟机。</p>
<h1 id="task-1使用十六进制编辑器修改-bare-metal-二进制文件">Task 1：使用十六进制编辑器修改 Bare-Metal 二进制文件</h1>
<h2 id="task-1初探-afl">Task 1：初探 AFL</h2>
<h3 id="task-1a安装-afl">Task 1.a：安装 AFL</h3>
<p>步骤：</p>
<p>1、输入 <code>git clone https://github.com/google/AFL.git</code> 克隆最新版本的源码，输入 <code>cd AFL</code> 进入 AFL 文件夹，输入 <code>make</code> 和 <code>sudo make install</code> 安装 AFL。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.1.png" alt="输出结果" /></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.2.png" alt="输出结果" /></p>
<p>2、输入 <code>ls /usr/local/bin/afl*</code> 查看文件发现安装成功。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.3.png" alt="输出结果" /></p>
<h2 id="task-1b初步尝试">Task 1.b：初步尝试</h2>
<p>步骤：</p>
<p>1、在 Task 1 文件夹中，输入 <code>afl-gcc -g -o test test.c</code> 指令编译 test.c 文件，生成 test 可执行文件。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.4.png" alt="输出结果" /></p>
<p>2、输入 <code>mikir fuzz_in fuzz_out</code> 指令创建 fuzz_in 和 fuzz_out 文件夹，输入 <code>echo 'aaa' &gt; ./fuzz_in/case</code> 指令准备一个测试用例。</p>
<p>3、输入 <code>afl-fuzz -i ./fuzz_in -o ./fuzz_out ./test</code> 命令进行模糊测试。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.5.png" alt="输出结果" /></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.6.png" alt="输出结果" /></p>
<p>Q： 请使用 xxd 查看你触发 crash 的 cases，并判断分别对应 test.c 中哪种漏洞，并解释漏洞产生的原因。注意，你的 crash cases 应覆盖所有 4 个漏洞。</p>
<p>A：进入 fuzz_in 文件夹下的 crashes 目录，可以看到所有的7个 crash cases。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.7.png" alt="输出结果" /></p>
<p>漏洞1: 如果输入的字符串的首字符为C并且长度为30，则异常退出：</p>
<p>输入 <code>xxd id:000002,sig:11,src:000001+000002,op:splice,rep:8</code> 指令查看第3个 crash case，发现这种情况下，输入的字符串的首字符为C并且长度为30。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.8.png" alt="输出结果" /></p>
<p>漏洞2: 如果输入的字符串的首字符为FAS并且长度为6，则异常退出：</p>
<p>输入 <code>xxd id:000001,sig:11,src:000004,op:arith8,pos:2,val:+25</code> 指令查看第2个 crash<br />
case，发现这种情况下，输入的字符串的前三个字符为FAT并且长度为6。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.9.png" alt="输出结果" /></p>
<p>漏洞3：存在栈溢出漏洞：</p>
<p>输入 <code>xxd id:000003,sig:06,src:000004,op:havoc,rep:128</code> 指令查看第4个 crash case，发现这种情况下，输入的字符串满足栈溢出条件。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.11.png" alt="输出结果" /></p>
<p>漏洞 4: 存在格式化字符串漏洞：</p>
<p>输入 <code>xxd id:000004,sig:06,src:000004,op:havoc,rep:16</code> 指令查看第5个 crash case，发现这种情况下，输入的字符串含有%格式化字符串漏洞。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/1.10.png" alt="输出结果" /></p>
<h1 id="task-2-基于-afl-测试-xpdf">Task 2: 基于 AFL++ 测试 Xpdf</h1>
<h2 id="331-afl-安装">3.3.1 AFL++ 安装</h2>
<p>步骤：</p>
<p>安装必要的 packages。输入 <code>sudo apt-get update</code>， <code>sudo apt-get upgrade</code>，<code>sudo apt-get install automake autoconf build-essential llvm</code>，<code>cd $HOME</code>，<code>git clone https://github.com/AFLplusplus/AFLplusplus</code>，<code>cd AFLplusplus</code>，<code>make all</code>和<code>sudo make install</code> 指令。</p>
<h2 id="332-构建环境">3.3.2 构建环境</h2>
<p>步骤：</p>
<p>1、为 Fuzz 目标创建一个新目录。输入 <code>cd \$HOME</code> 和 <code>mkdir fuzzing_xpdf &amp;&amp; cd fuzzing_xpdf</code> 指令。</p>
<p>2、下载 Xpdf 3.02 版本。输入 <code>wget https://dl.xpdfreader.com/old/xpdf-3.02.tar.gz</code> 和 <code>tar -xvzf xpdf-3.02.tar.gz</code> 指令。</p>
<p>3、构建 Xpdf。输入 <code>cd xpdf-3.02</code>， <code>./configure --prefix=&quot;$HOME/fuzzing_xpdf/install/&quot;</code>，<code>make</code> 和 <code>make install</code> 指令。</p>
<p>4、准备一些 PDF 样例文件用于测试。输入 <code>cd $HOME/fuzzing_xpdf</code>，<code>mkdir pdf_examples &amp;&amp; cd pdf_examples</code>，<code>wget https://github.com/mozilla/pdf.js-sample-files/raw/master/helloworld.pdf</code> 和 <code>wget https://www.melbpc.org.au/wp-content/uploads/2017/10/small-example-pdf-file.pdf</code> 指令。</p>
<p>5、测试 pdfinfo 二进制文件。输入 <code>cd $HOME/fuzzing_xpdf</code> 和 <code>./install/bin/pdfinfo -box -meta ./pdf_examples/helloworld.pdf</code> 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/2.1.png" alt="输出结果" /></p>
<h2 id="333-开始-fuzz">3.3.3 开始 Fuzz</h2>
<p>步骤：</p>
<p>1、清理所有先前编译的目标文件和可执行文件。输入 <code>rm -r $HOME/fuzzing_xpdf/install</code>，<code>cd $HOME/fuzzing_xpdf/xpdf-3.02/</code> 和 <code>make clean</code> 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/2.2.png" alt="输出结果" /></p>
<p>2、使用 afl-clang-fast 编译器构建 xpdf。输入<code>CC=$HOME/AFLplusplus/afl-clang-fast CXX=$HOME/AFLplusplus/afl-clang-fast++ ./configure --prefix=&quot;$HOME/fuzzing_xpdf/install/&quot;</code>，make 和 make install 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/2.3.png" alt="输出结果" /></p>
<p>3、使用 AFL++ 进行模糊测试。输入 <code>$HOME/AFLplusplus/afl-fuzz -i $HOME/fuzzing_xpdf/pdf_examples/ -o $HOME/fuzzing_xpdf/out/ -s 123 -- $HOME/fuzzing_xpdf/install/bin/pdftotext @@ $HOME/fuzzing_xpdf/output</code> 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/2.3.png" alt="输出结果" /></p>
<p>发现了6个 crash cases。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/2.4.png" alt="输出结果" /></p>
<p>4、配置 gdb 进行调试。输入 <code>gdb --args $HOME/fuzzing_xpdf/install/bin/pdftotext $HOME/fuzzing_xpdf/out/default/crashes/id:000000,sig:11,src:000001,time:100335,execs:,op:havoc,rep:2 $HOME/fuzzing_xpdf/outputn</code> 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/2.7.png" alt="输出结果" /></p>
<p>输入 <code>run</code> 指令运行。发现错误类型为 SIGSEGV。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/2.8.png" alt="输出结果" /></p>
<p>输入 <code>bt</code> 指令回溯堆栈。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/2.9.png" alt="输出结果" /></p>
<p>Q：在实验报告中，请解释此现象的产生原因。</p>
<p>A：从 GDB 输出可以看出，程序在执行 __GI__IO_file_xsgetn 函数时发生了段错误(SIGSEGV)。该函数从 fileops.c 文件中读取数据，但是找不到该文件。从 bt 回溯中可以发现，此错误是由于在函数 Parser::makeStream 中创建文件时发生错误。</p>
<p>5、在 Parser::getObj() 函数设置断点并执行程序。输入 <code>b Parser::getObj</code> 和 <code>run</code> 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/2.9.png" alt="输出结果" /></p>
<p>Q：请根据上述步骤结合 gdb 的使用，进行 crash 的复现和分析。完成后，请描述观察结果，并解释引起这种漏洞的原因。</p>
<p>A：crash 的复现：输入 <code>gdb --args $HOME/fuzzing_xpdf/install/bin/pdftotext $HOME/fuzzing_xpdf/out/default/crashes/id:000000,sig:11,src:000001,time:100335,execs:87679,op:havoc,rep:2 $HOME/fuzzing_xpdf/outputn</code> 指令即可（见图17和图18）。</p>
<p>crash的分析：输入 c 继续运行，发现程序回到了 Parser::getObj 函数，而堆栈在不断使用。可以发现该程序是由于某种原因一直重复 Parser::getObj 函数直至堆栈耗尽而出错。接下来输入 n 一步步调试该程序：</p>
<pre><code>Parser::getObj (this=0x5555556c9c10, obj=0x7fffffffdc70, 
fileKey=0x0, encAlgorithm=cryptRC4, keyLength=0x0, objNum=0x0, objGen=0x0)
at Parser.cc:41
                int objNum, int objGen) &#123;
Object obj2;
if (inlineImg == 2) &#123;
    if (buf1.isCmd(&quot;[&quot;)) &#123;
        &#125; else if (buf1.isCmd(&quot;&lt;&lt;&quot;)) &#123;
            &#125; else if (buf1.isInt()) &#123;
                num = buf1.getInt();
                shift();
                if (buf1.isInt() &amp;&amp; buf2.isCmd(&quot;R&quot;)) &#123;
                    obj-&gt;initInt(num);
                    return obj;
                    &#125;
                    XRef::readXRefTable (this=0x5555556ca230, parser=0x5555556c9c10, 
                    pos=0x7fffffffdd2c) at XRef.cc:397
                            entry.gen = obj.getInt();
                obj.free();
                parser-&gt;getObj(&amp;obj);
                Parser::getObj (this=0x5555556c9c10, obj=0x7fffffffdc70, 
                fileKey=0x0, encAlgorithm=cryptRC4, keyLength=0x0, objNum=0x0, objGen=0x0)
                at Parser.cc:41
                                int objNum, int objGen) &#123;       
</code></pre>
<p>发现迭代的 Parser::getObj 函数的参数未发生变化，于是导致了无限循环。</p>
<h1 id="task-3-使用-qemu-模式执行模糊测试无程序源码">Task 3: 使用 QEMU 模式执行模糊测试（无程序源码）</h1>
<h2 id="341-安装-qemu-模式aflplusplus-文件夹下">3.4.1 安装 QEMU 模式（AFLplusplus 文件夹下）</h2>
<p>步骤：</p>
<p>1、安装 QEMU 模式所需的依赖包。输入 <code>sudo apt-get install libglib2.0-dev ninja-build</code>，<code>cd qemu_mode</code> 和 <code>./build_qemu_support.sh</code> 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.1.png" alt="输出结果" /></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.2.png" alt="输出结果" /></p>
<p>发现显示 [+] libqasan ready 和 [+] all和 sudo done for qemu_mode, enjoy!，说明安装成功。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.3.png" alt="输出结果" /></p>
<p>2、返回到上级目录并重新安装 AFL++。输入 <code>cd ..</code> 和 <code>sudo make install</code> 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.4.png" alt="输出结果" /></p>
<p>3、验证 afl-qemu-trace 是否已正确安装在 bin 目录下。输入 <code>ls /usr/local/bin/afl*</code> 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.5.png" alt="输出结果" /></p>
<h2 id="342-使用-qemu-模式执行模糊测试">3.4.2 使用 QEMU 模式执行模糊测试</h2>
<p>步骤：</p>
<p>1、更新 libc 库。输入 <code>sudo vi /etc/apt/sources.list</code> 指令打开sources.list文件以添加新的源，在文件中添加 <code>deb http://th.archive.ubuntu.com/ubuntu jammy main</code> 来更新 libc。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.6.png" alt="输出结果" /></p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.7.png" alt="输出结果" /></p>
<p>2、更新系统软件源列表并安装最新版本的 libc。输入 <code>sudo apt update</code> 和 <code>sudo apt install libc6</code> 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.8.png" alt="输出结果" /></p>
<p>3、输入 <code>$HOME/AFLplusplus/afl-fuzz -Q -i $HOME/qemu_fuzz/exif-samples/jpg/ -o $HOME/qemu_fuzz/out -s 123 -- $HOME/qemu_fuzz/install/bin/exif @@</code> 进行模糊测试。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.9.png" alt="输出结果" /></p>
<h2 id="343-分析得到的-crash">3.4.3 分析得到的 crash</h2>
<p>在 crashes 文件夹中，出现了如下的14个 crash cases。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.10.png" alt="输出结果" /></p>
<p>Q：请研究该程序中已知的 CVE-2009-3895 或 CVE-2012-2836 漏洞。结合 afl-fuzz -Q 和 gdb 工具，按照 Task 2 的步骤，找出至少一个漏洞的原因，并详细解释如何产生这些漏洞。</p>
<p>A：crash 的复现：输入 <code>gdb --args $HOME/qemu_fuzz/install/bin/exif ./id:000000,sig:06,src:000060+000464,time:2201871,execs:803513,op:splice,rep:6</code> 指令。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.11.png" alt="输出结果" /></p>
<p>crash 的分析：输入 <code>bt</code> 指令回溯。</p>
<p><img src="https://raw.githubusercontent.com/SuperYzs/MarkdownPicture/main/Fuzzy%20Testing%20Technology/3.12.png" alt="输出结果" /></p>
<p>这个堆栈跟踪显示了一个程序崩溃，原因是在尝试重新分配内存时出现了问题。具体来说，错误消息 &quot;realloc(): invalid next size&quot; 表示程序试图重新分配的内存块的大小不正确。</p>
<p>在堆栈跟踪中，我们可以看到这个问题发生在 exif_entry_realloc 函数中，这个函数试图重新分配一个 ExifEntry 结构的内存。这个函数是在 exif_entry_fix 函数中调用的，该函数试图修复一个 ExifEntry。</p>
<p>这是一个缓冲区溢出漏洞，当输入数据可以控制重新分配的大小，攻击者可能能够利用这个漏洞来引发程序崩溃，或者执行任意代码。</p>
