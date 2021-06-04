#!/usr/bin/env python3
import contextlib
import os
import shutil
import subprocess
import time
from pathlib import Path
from textwrap import dedent


@contextlib.contextmanager
def chdir(path):
    prev = Path.cwd()
    try:
        yield os.chdir(path)
    finally:
        os.chdir(prev)


def create_testcase(source, *, n=1024, depth=1):
    assert depth == 1, "Not implemented"

    source.mkdir()
    with chdir(source):
        Path('CMakeLists.txt').write_text(dedent(
            '''
            cmake_minimum_required(VERSION 3.20)
            project(glob-test)
    
            file(GLOB_RECURSE sources CONFIGURE_DEPENDS "src/**.cpp")
            add_executable(main ${sources})
            '''
        ).lstrip())

        Path('src').mkdir()

        Path('src/main.cpp').write_text(dedent(
            '''
            int main () {
                return 0;
            }
            '''
        ).lstrip())

        for i in range(1, n):
            Path(f'src/src{i}.cpp').touch()


def time_command(cmd):
    proc = subprocess.Popen(cmd, shell=True)
    start = time.perf_counter()
    proc.communicate()
    return time.perf_counter() - start


def is_single_config(generator):
    return (('Ninja' in generator or 'Make' in generator)
            and 'Multi' not in generator)


def test_overhead(source, build, generator='Ninja'):
    if is_single_config(generator):
        os.system(f'cmake -G "{generator}" -S {source} -B {build} -DCMAKE_BUILD_TYPE=Release')
        build_cmd = f'cmake --build {build}'
    else:
        os.system(f'cmake -G "{generator}" -S {source} -B {build}')
        build_cmd = f'cmake --build {build} --config Release'
    os.system(build_cmd)
    return time_command(build_cmd)


def main():
    source = Path('./test')
    if source.exists():
        shutil.rmtree(source)

    build = Path('./build')
    if build.exists():
        shutil.rmtree(build)

    default_generator = ('Visual Studio 16 2019' if os.name == 'nt'
                         else 'Ninja')

    create_testcase(source, n=1024)
    overhead = test_overhead(source, build, default_generator)

    print(f'Overhead was: {overhead} seconds')


if __name__ == '__main__':
    main()
