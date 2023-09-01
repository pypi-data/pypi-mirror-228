#!/bin/bash

set -e
set -u

includedir=../src/assorthead/include
mkdir -p $includedir
transplant_headers() {
    local src=$1
    dest=$includedir/$(basename $src)
    rm -rf $dest
    cp -r $src $dest
}

# Simple fetching, when a submodule can be directly added and the
# header files are directly available from the repository.

fetch_simple() {
    local name=$1
    local url=$2
    local version=$3

    if [ ! -e $name ]
    then
        git submodule add $url $name
    else
        cd $name
        git fetch --all
        git checkout $version
        cd -
    fi
}

fetch_simple aarand https://github.com/LTLA/aarand v1.0.1
transplant_headers aarand/include/aarand 

fetch_simple powerit https://github.com/LTLA/powerit v1.0.0
transplant_headers powerit/include/powerit

fetch_simple kmeans https://github.com/LTLA/CppKmeans v1.0.0
transplant_headers kmeans/include/kmeans

fetch_simple byteme https://github.com/LTLA/byteme v1.0.1
transplant_headers byteme/include/byteme

# Fetch + CMake, when a repository requires a CMake configuration
# to reorganize the headers into the right locations for consumption.
# This also handles transitive dependencies.

fetch_cmake() {
    local name=$1
    local url=$2
    local version=$3

    fetch_simple $name $url $version

    cd $name
    if [ ! -e build ]
    then
        cmake -S . -B build
    fi
    cd -
}

fetch_cmake knncolle https://github.com/LTLA/knncolle master
transplant_headers knncolle/include/knncolle
transplant_headers knncolle/build/_deps/annoy-build/include/annoy
transplant_headers knncolle/build/_deps/hnswlib-src/hnswlib
