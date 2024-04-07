#!/usr/bin/env python3

import argparse
import os
import time

DIR_TMP_OLD = 'tmp_old'
DIR_TMP_NEW = 'tmp_new'

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-r', '--repo', required=True)
arg_parser.add_argument('-o', '--old', required=True)
arg_parser.add_argument('-n', '--new', type=str, default='master')
arg_parser.add_argument('-m', '--main', type=str, default='main')
args = arg_parser.parse_args()

repo = args.repo
old_co = args.old
new_co = args.new
main_file = args.main

def clean():
    os.system(f'rm -rf {DIR_TMP_OLD}')
    os.system(f'rm -rf {DIR_TMP_NEW}')
    os.system(f'rm -f *.pdf')

def git_clone(repo, co, dir):
    cmd = f'git clone {repo} {dir}; cd {dir}; pwd; git checkout {co}; cd ..'
    print(cmd)
    os.system(cmd)

def flatten(dir, main):
    cmd = f'cd {dir}; latexpand {main}.tex > {main}_flat.tex; cd ..'
    print(cmd)
    os.system(cmd)

def diff(old_dir, new_dir, main):
    cmd = f'cd {new_dir}; latexdiff ../{old_dir}/{main}_flat.tex {main}_flat.tex > {main}_diff.tex; cd ..'
    print(cmd)
    os.system(cmd)

def pdfgen(dir, main):
    main_diff = f'{main}_diff'
    cmd = f'cd {dir}; bibtex {main_diff}; pdflatex -shell-escape -interaction=nonstopmode {main_diff}.tex; pdflatex -shell-escape -interaction=nonstopmode {main_diff}.tex; cd ..'
    print(cmd)
    os.system(cmd)

def copy_to_root(dir, main):
    cmd = f'cp {dir}/{main}_diff.pdf .'
    print(cmd)
    os.system(cmd)

clean()

git_clone(repo, old_co, DIR_TMP_OLD)
git_clone(repo, new_co, DIR_TMP_NEW)

flatten(DIR_TMP_OLD, main_file)
flatten(DIR_TMP_NEW, main_file)

diff(DIR_TMP_OLD, DIR_TMP_NEW, main_file)

pdfgen(DIR_TMP_NEW, main_file)

copy_to_root(DIR_TMP_NEW, main_file)
