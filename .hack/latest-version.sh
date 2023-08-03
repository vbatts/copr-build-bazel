#!/bin/bash

set -eu

previous=0

while getopts 1 flag
do
  case "${flag}" in
    1) previous=1;;
  esac
done

ver="$(curl -sSL "https://www.fedoraproject.org/server/download/" | grep -Eo 'Fedora Server [[:digit:]]+' | head -1 | grep -Eo '[[:digit:]]+')"

if [ "${previous}" -eq 1 ] ; then
  expr $ver - 1
else
  echo "$ver"
fi

# vim:set sts=2 sw=2 et:
