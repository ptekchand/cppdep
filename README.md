# Cpp Dependency Analysis

The author for this code is Chris Steinbach. A license statement isn't included in the original source. The original source link seems unavailable:
http://csteinbach.com/public/cppdep-0.2.tar.gz

I made a small patch a long time ago and was recently asked for a copy in the comments of my post. Re-hosting it here.

### Details from
http://www.c2.com/cgi/wiki?CppDependencyAnalysis


Header files, used in the wrong way, can make [CeePlusPlus](http://www.c2.com/cgi/wiki?CeePlusPlus) compilations really slow. The only reason is that they include more source code to compile. And the headers they include have some more source code, and so on.

There are things you can do to prevent including more than you really need to, but the first step is to figure out where all your compilation time is going. I whipped up a small tool in python that helps you find the culprits, you can get it here: http://csteinbach.com/public/cppdep-0.2.tar.gz

It contains three python scripts. `explore.py` lets you see the include tree together with the cumulative number of lines included for each file. It should look something like this:
Missing Image

`explore.py` takes preprocessor output as its input. There is also a script `tree.py` which is simply a text version of `explore.py`.

Another script `report.py` helps pinpoint header file bloat for a whole project. The output is like this,
```
 . . .
 . . .
 /usr/lib/gcc/i686-pc-cygwin/3.4.4/include/c++/bits/stl_algobase.h lines in file(842), all included lines(82076), places included from(22)
 /usr/lib/gcc/i686-pc-cygwin/3.4.4/include/c++/bits/stl_algo.h lines in file(5148), all included lines(91564), places included from(22)
 /usr/lib/gcc/i686-pc-cygwin/3.4.4/include/c++/algorithm lines in file(71), all included lines(91674), places included from(22)
 /usr/lib/gcc/i686-pc-cygwin/3.4.4/include/c++/ios lines in file(53), all included lines(94203), places included from(18)
 /usr/lib/gcc/i686-pc-cygwin/3.4.4/include/c++/bits/char_traits.h lines in file(376), all included lines(94817), places included from(22)
 /usr/lib/gcc/i686-pc-cygwin/3.4.4/include/c++/istream lines in file(774), all included lines(154096), places included from(18)
 /usr/lib/gcc/i686-pc-cygwin/3.4.4/include/c++/sstream lines in file(643), all included lines(161358), places included from(18)
 /usr/lib/gcc/i686-pc-cygwin/3.4.4/include/c++/string lines in file(60), all included lines(278947), places included from(22)
 ../include/log4cpp/OstringStream.hh lines in file(52), all included lines(294740), places included from(22)
```

In this case `OstringStream.hh` that has produced 294740 lines of code for compilation and it has been included in 22 different places.

All these scripts take preprocessor output as their input. Here's how you get hold of preprocessor output:

### Preprocessor output for Windows developers

If you are programming with Visual Studio change the project C++ settings to produce preprocessor output (this works for VS 7, not sure for VS 6 or earlier). After a build you will see a bunch of files with a .i extension. These can be passed directly to the scripts. If you are using the CL (Windows) compiler program from the command line or a script, use the compiler option /P to generate preprocessor output.

### Preprocessor output from GnuCpp

If you are using makefiles, then [GnuCpp](http://www.c2.com/cgi/wiki?GnuCpp) has a flag --save-temps that will leave the preprocessor output in a file with a .ii extension. The -E flag will also produce preprocessor output, but will stop the compilation process at that point.

### Script usage syntax
```
 $ python explore.py <module.i> # or module.ii for g++
 $ python tree.py <module.i>
 $ python report.py module1.i module2.i ...
```

--[ChrisSteinbach](http://www.c2.com/cgi/wiki?ChrisSteinbach)
