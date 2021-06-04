# CMake Glob Performance

This is a Python script for testing a few 1024-file-and-directory
scenarios for globbing to determine the overhead in a no-op build
setting.

If you don't want to bother with Python (and are running Linux),
the default experiment is basically this:

```shell
$ cat >CMakeLists.txt <<EOF
> cmake_minimum_required(VERSION 3.20)
> project(test-glob)
>
> file(GLOB sources CONFIGURE_DEPENDS "src/*.cpp")
> add_executable(main ${sources})
> EOF
$ mkdir src
$ echo "int main() { return 0; }" > src/main.cpp
$ touch src/src_{1..1023}.cpp
$ cmake -G Ninja -S . -B build
...
$ cmake --build build
...
$ time cmake --build build  # no-op, just measuring glob check
```

