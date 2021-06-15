#!/usr/bin/env python3
import argparse
import contextlib
import os
import shutil
import subprocess
import time
from multiprocessing import cpu_count
from pathlib import Path
from textwrap import dedent


@contextlib.contextmanager
def chdir(path):
    prev = Path.cwd()
    try:
        yield os.chdir(path)
    finally:
        os.chdir(prev)


def create_sources(n):
    Path('src').mkdir()

    sources = [Path('src/main.cpp')]

    sources[0].write_text(dedent(
	    '''
        int main () {
            return 0;
        }
        '''
    ).lstrip())

    for i in range(1, n):
        p = Path(f'src/src{i}.cpp')
        p.touch()
        sources.append(p)

    return sources


def create_testcase(source, *, n=1024, depth=1, use_globs=True):
    assert depth == 1, "Not implemented"

    source.mkdir()
    with chdir(source):
        sources = create_sources(n)

        if use_globs:
            sources_list = 'file(GLOB_RECURSE sources CONFIGURE_DEPENDS "src/**.cpp")'
        else:
            sources_list = " ".join(map(Path.as_posix, sources))
            sources_list = f'set(sources {sources_list})'

        Path('CMakeLists.txt').write_text(dedent(
            f'''
            cmake_minimum_required(VERSION 3.20)
            project(glob-test)

            {sources_list}
            add_executable(main ${{sources}})
            '''
        ).lstrip())


def time_command(cmd):
    proc = subprocess.Popen(cmd, shell=True)
    start = time.perf_counter()
    proc.communicate()
    return time.perf_counter() - start


def is_single_config(generator):
    return (('Ninja' in generator or 'Make' in generator)
            and 'Multi' not in generator)


def test_overhead(source, build, generator):
    if is_single_config(generator):
        os.system(f'cmake -G "{generator}" -S {source} -B {build} -DCMAKE_BUILD_TYPE=Release')
        build_cmd = f'cmake --build {build} -j {cpu_count()}'
    else:
        os.system(f'cmake -G "{generator}" -S {source} -B {build}')
        build_cmd = f'cmake --build {build} --config Release -j {cpu_count()}'
    os.system(build_cmd)
    return time_command(build_cmd)


def run_test(source, build, generator, *, test_args):
    if source.exists():
        shutil.rmtree(source)
    if build.exists():
        shutil.rmtree(build)

    create_testcase(source, **test_args)
    return test_overhead(source, build, generator)


def main():
    default_generator = os.getenv('CMAKE_GENERATOR', default=(
        'Visual Studio 16 2019' if os.name == 'nt' else 'Ninja'
    ))

    parser = argparse.ArgumentParser(description='Test CMake glob performance')
    parser.add_argument('--generator', type=str, default=default_generator,
                        metavar='GEN',
                        help='the CMake generator to use (e.g. Ninja)')
    parser.add_argument('--source', type=Path, default=Path('./test'),
                        help='directory in which to place the test case')
    parser.add_argument('--build', type=Path, default=Path('./build'),
                        help='directory in which to build the test case')
    parser.add_argument('-n', type=int, default=1024,
                        help='number of files to create')
    args = parser.parse_args()


    no_op_glob = run_test(
        args.source,
        args.build,
        args.generator,
        test_args=dict(
            n=args.n,
            use_globs=True
        )
    )

    no_op_explicit = run_test(
        args.source,
        args.build,
        args.generator,
        test_args=dict(
            n=args.n,
            use_globs=False
        )
    )
    
    print(f'Overhead was: {no_op_glob - no_op_explicit:.04f} seconds')


if __name__ == '__main__':
    main()
