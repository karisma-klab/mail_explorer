#!/bin/bash

# Function to display the help message
display_help() {
    echo "Usage: $0 [options] <argument>"
    echo "Options:"
    echo "  -h, --help           Display this help message"
    echo "  -s, --source <dir>   Specify the source directory (default: summarized)"
    echo "  -d, --dest <dir>     Specify the destination directory (default: summarized_bin)"
}

# Default values
source_dir="summarized"
dest_dir="summarized_bin"

# Process command-line options
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            display_help
            exit 0
            ;;
        -s|--source)
            source_dir="$2"
            shift
            shift
            continue
            ;;
        -d|--dest)
            dest_dir="$2"
            shift
            shift
            continue
            ;;
        *)
            # Ignore any other positional arguments
            break
            ;;
    esac
done

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "Error: Argument missing!"
    display_help
    exit 1
fi

# Continue with the script logic using the provided argument, source directory, and destination directory
echo "Argument: $1"
echo "Source Directory: $source_dir"
echo "Destination Directory: $dest_dir"
# Add your script logic here...

cd $source_dir
echo "Moving files..."
time grep -rlZ "$1" * | xargs -0 -I {} sh -c 'echo "Moving:{}" &&  mkdir -p ../'"$dest_dir"'/$(dirname {}) &&  mv {} ../'"$dest_dir"'/{}' | wc -l
