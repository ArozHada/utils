#!/bin/bash

SEARCH_DIR="."  # Change this to your TIFF root directory
CHK_FILE="checklist.chk"

# Create empty .chk if it doesn't exist
[[ ! -f "$CHK_FILE" ]] && touch "$CHK_FILE"

# Create an associative array for fast lookup of existing file paths
declare -A existing_files

# Read existing entries and store file paths in the associative array
while read -r md5sum filepath; do
    existing_files["$filepath"]=1
done < "$CHK_FILE"

# Find all *.TIFF files in SEARCH_DIR
find "$SEARCH_DIR" -type f \( -iname \*.tif -o -iname \*.tiff \) | while read -r file; do
    if [[ -z "${existing_files["$file"]}" ]]; then
        # File not found in .chk, compute MD5 and append
        md5=$(md5sum "$file" | awk '{print $1}')
        echo "$md5 $file" >> "$CHK_FILE"
        echo "Added: $file"
    fi
done

#find . -type f \( -iname \*.tif -o -iname \*.tiff \) -exec md5sum "{}" + > checklist.chk
