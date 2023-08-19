#!/bin/sh

read -p "Do you want to update .vimrc? "
echo
if [[ $REPLY =~ ^[Yy] ]]; then
  FILE_NAME="$HOME/.vimrc"
  FILE_CONTENTS="colorscheme elflord\nsyntax on\nset colorcolumn=81,89\nset indentexpr=\nset clipboard=unnamed\n" 
  printf "$FILE_CONTENTS" > $FILE_NAME
fi
