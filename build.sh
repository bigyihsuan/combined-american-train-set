#!/bin/bash

# NGRF_DIR=/mnt/c/Users/bigyi/OneDrive/Documents/OpenTTD/newgrf
NGRF_DIRS=(/mnt/c/Users/bigyi/Documents/OpenTTD/newgrf /mnt/c/Users/bigyi/OneDrive/Documents/OpenTTD/newgrf)
USAGE="usage: ./build.sh (default | extract | compile | bundle | install | clean)"
GRF_PATH=./dist/cats.grf

function LINE() {
	echo "--------"
}

function default() {
	# extract
    compile
    install
}

function extract() {
    echo "Extracting vehicle info..."
    python3 src/extractProps.py
    echo "Extracting vehicle info complete."
	LINE
}

function compile() {
    echo "Compiling GRF..."
    python3 src/cats-grfpy.py
    echo "Compiling GRF complete."
	LINE
}

function bundle() {
    echo "Bundling GRF..."
	rm -v cats.tar
	mkdir -p dist
	cp -v README.md dist/readme.txt
	cp -v LICENSE dist/license.txt
	cp -v changelog.md dist/changelog.txt
	tar cvf cats.tar dist
	LINE
}

function install() {
    echo "Installing GRF..."
    if [[ -e $GRF_PATH ]]; then
		for dir in "${NGRF_DIRS[@]}"; do
			cp -v $GRF_PATH $dir
		done
		echo "Successfully installed."
	else
		echo "GRF path '$GRF_PATH' does not exist."
	fi
	LINE
}

function clean() {
    echo "Cleaning installation dir..."
	for dir in "${NGRF_DIRS[@]}"; do
		rm -v "$dir/cats.grf"
	done
	echo "Cleaning complete."
	LINE
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