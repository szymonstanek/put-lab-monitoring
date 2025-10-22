#!/bin/bash

echo "Cleaning up lab result files..."

files=(
    "blocking_probabilities.txt"
    "average_occupancy.txt"
    "task_22_blocking_probabilities.txt"
    "task_22_plot.png"
    "task_23_blocking_probabilities.txt"
    "task_23_plot.png"
)

count=0

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "  Deleted: $file"
        ((count++))
    fi
done

if [ $count -eq 0 ]; then
    echo "  No files to delete."
else
    echo "Cleanup complete. Removed $count file(s)."
fi
