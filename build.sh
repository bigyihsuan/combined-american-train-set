#!/bin/bash

NGRF_DIR=/mnt/c/Users/bigyi/OneDrive/Documents/OpenTTD/newgrf
USAGE="usage: ./build.sh (default | extract | compile | bundle | install | clean)"
GRF_PATH=./dist/cats.grf

function default() {
    extract
    compile
    install
}

function extract() {
    echo "Extracting vehicle info..."
    cd extract/
    python3 extract-vehicle-props.py
    cd ..
}

function compile() {
    echo "Compiling GRF..."
    python3 src/cats.py
}

function bundle() {
    echo "Bundling GRF..."
	rm cats.tar
	mkdir -p dist
	cp README.md dist/readme.txt
	cp LICENSE dist/license.txt
	cp changelog.md dist/changelog.txt
	tar cvf cats.tar dist
}

function install() {
    echo "Installing GRF..."
    if [[ -e $GRF_PATH ]]; then
		cp $GRF_PATH $NGRF_DIR
        echo "Successfully installed."
	fi
}

function clean() {
    echo "Cleaning installation dir..."
	rm "$NGRF_DIR/cats.grf"
}

if [[ "$#" -eq 0 ]]; then
	default
	exit 0
fi

if [[ "$1" = "default" ]]; then
	default
elif [[ "$1" = "extract" ]]; then
	extract
elif [[ "$1" = "compile" ]]; then
	compile
elif [[ "$1" = "install" ]]; then
	install
elif [[ "$1" = "bundle" ]]; then
	bundle
elif [[ "$1" = "clean" ]]; then
	clean
else
	echo $USAGE
	exit 1
fi