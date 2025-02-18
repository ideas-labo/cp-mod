## Run the Tools

The executable files after compilation are in the folder `cp-mod/taintanalysis/cpp/ExecutableFile ` 

> cp-mod/taintanalysis/cpp/ExecutableFile/forline
> cp-mod/taintanalysis/cpp/ExecutableFile/functionline
> cp-mod/taintanalysis/cpp/ExecutableFile/ifswitchline
> cp-mod/taintanalysis/cpp/ExecutableFile/variableline

Before running, we need to add executable permissions to the file.

```
chmod +x ./forline
chmod +x ./functionline
chmod +x ./ifswitchline
chmod +x ./variableline
```

#### Indroduction

The results will be printed out in the terminal. It may contain some error messages indicating that the link cannot be established. Please ignore them.



**forline**: Search for the locations where loop(while for) control flow appears in the specified file.

```
./forline {cpp/c filepath}
```

The result form is 

```
Line{startline}:{endline}
```

In our test case

```
./forline /testcase/test.cpp
Line17:19
```



**functionline**: Search for the location where the target function is called within the specified file and function.

```
./functionline --functionname {functionname} {cpp/c filepath}
```

The result form is 

```
line: {linenumber}
```

In our test case

```
./functionline --functionname divide /testcase/test.cpp
line: 51
```



**ifswitchline**: Search for the locations where if(switch) control flow appears in the specified file.

```
./ifswitchline {cpp/c filepath}
```

The result form is 

```
Line{startline}:{endline}
```

In our test case

```
./ifswitchline /testcase/test.cpp
Line25:27
```



**variableline**: Search for the target variable initialization location and the location where it is called within the specified file.

```
./variableline {variablename} {cpp/c filepath}
```

The result form is 

```
line: {linenumber}
```

In our test case

```
./variableline num1/testcase/test.cpp
line: 32
line: 35
line: 42
line: 45
line: 48
line: 51
```





## Compile from source code

### 1: Obtaining Clang

1. **Create a working directory and download the LLVM project:**

   ```
   mkdir ~/clang-llvm && cd ~/clang-llvm
   git clone https://github.com/llvm/llvm-project.git
   ```

   - Create a new directory and download LLVM source code.

2. **Download and install the Ninja build tool:**

   ```
   cd ~/clang-llvm
   git clone https://github.com/martine/ninja.git
   cd ninja
   git checkout release
   ./configure.py --bootstrap
   sudo cp ninja /usr/bin/
   ```

   - Download Ninja source code, build, and install it.

3. **Download and install CMake:**

   ```
   cd ~/clang-llvm
   git clone https://gitlab.kitware.com/cmake/cmake.git
   cd cmake
   git checkout next
   ./bootstrap
   make
   sudo make install
   ```

   - Download CMake source code, build, and install it.

4. **Build Clang:**

   ```
   cd ~/clang-llvm
   mkdir build && cd build
   cmake -G Ninja ../llvm-project/llvm -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra" -DCMAKE_BUILD_TYPE=Release -DLLVM_BUILD_TESTS=ON
   ninja
   ninja check
   ninja clang-test
   ninja install
   ```

   - Configure, build, test, and install Clang and related tools.

5. **Set Clang as the compiler:**

   ```
   cd ~/clang-llvm/build
   ccmake ../llvm-project/llvm
   ```

   - Open CMake configuration interface and set `CMAKE_CXX_COMPILER` to `/usr/bin/clang++`.

### 2: Create a ClangTool

1. **Create a new tool directory and add it to the CMake build system:**

   ```
   cd ~/clang-llvm/llvm-project
   mkdir clang-tools-extra/loop-convert
   echo 'add_subdirectory(loop-convert)' >> clang-tools-extra/CMakeLists.txt
   vim clang-tools-extra/loop-convert/CMakeLists.txt
   ```

   - Create a new directory and modify CMake files to include the new tool.

2. **Edit `CMakeLists.txt`:**

   ```
   set(LLVM_LINK_COMPONENTS support)
   
   add_clang_executable(mytool
     mytool.cpp
     )
   target_link_libraries(mytool
     PRIVATE
     clangTooling
     clangBasic
     clangASTMatchers
     clangAST
     clangFrontend
     clangSerialization
     )
   
   ```

With that done, Ninja will be able to compile our tool. Let’s give it something to compile! Put the following code into `clang-tools-extra/mytool.cpp`. 

1. functionsearch.cpp
2. varsearch.cpp
3. loopsearch.cpp
4. ifswitchlsearch.cpp

### 3: Compiling the New Tool

1. Compile the new tool:

   ```
   cd llvm-project/build
   
   cmake -G Ninja ../llvm -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra" -DLLVM_BUILD_TESTS=ON -DCMAKE_BUILD_TYPE=Release
   
   sudo ninja
   ```
   
   - Run the `ninja` build tool from the build directory to compile the new tool.

### 4: Running the New Tool

After compiling, the new tool (syntax checker) will be located in the `~/clang-llvm/build/bin` directory named `mytool`. You can rename it.

