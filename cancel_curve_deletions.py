#!/usr/bin/env python

import re
import argparse

def cancel_curve_deletions(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        current_hunk = []
        in_hunk = False
        line_offset = 0  # Track cumulative line number offset

        for line in infile:
            # Detect the start of a hunk (e.g., "@@ -1,4 +1,3 @@")
            if line.startswith('@@'):
                breakpoint()
                if in_hunk and current_hunk:
                    # Process the completed hunk
                    updated_hunk, hunk_offset = process_hunk(current_hunk)
                    outfile.writelines(updated_hunk)
                    line_offset += hunk_offset
                    current_hunk = []

                # Write the updated hunk header with adjusted line numbers
                line = adjust_hunk_header(line, line_offset)
                outfile.write(line)
                in_hunk = True

            elif in_hunk:
                # Collect lines of the current hunk
                current_hunk.append(line)

            else:
                # Outside of hunk, write the line as-is
                outfile.write(line)

        # Process any remaining hunk
        if in_hunk and current_hunk:
            updated_hunk, hunk_offset = process_hunk(current_hunk)
            outfile.writelines(updated_hunk)

def process_hunk(hunk_lines):
    breakpoint()
    new_hunk = []
    header = hunk_lines[0]
    
    # Parse the header to get old and new line counts
    match = re.match(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@', header)
    if not match:
        return hunk_lines, 0  # Invalid hunk header; return original lines and no offset

    old_start, old_count, new_start, new_count = map(int, match.groups())
    
    old_count_adjusted = old_count
    new_count_adjusted = new_count
    hunk_offset = 0

    for line in hunk_lines[1:]:
        match_deleted_curve = re.match(r'-\s*<curve.*', line)
        breakpoint()
        if match_deleted_curve:
            # Skip this line to cancel deletion
            old_count_adjusted -= 1
            hunk_offset -= 1
        else:
            new_hunk.append(line)
            if line.startswith('-'):
                old_count_adjusted -= 1
                hunk_offset -= 1
            elif line.startswith('+'):
                new_count_adjusted += 1
                hunk_offset += 1

    # Write the adjusted hunk header
    new_header = f"@@ -{old_start},{old_count_adjusted} +{new_start},{new_count_adjusted} @@\n"
    new_hunk.insert(0, new_header)
    
    return new_hunk, hunk_offset

def adjust_hunk_header(header, offset):
    # Adjust the hunk header line numbers according to the cumulative offset
    match = re.match(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@', header)
    if not match:
        return header  # Return the header unchanged if it doesn't match the expected pattern

    old_start, old_count, new_start, new_count = map(int, match.groups())

    # Apply offset to the start line numbers
    old_start_adjusted = old_start + offset
    new_start_adjusted = new_start + offset

    # Construct the adjusted hunk header
    new_header = f"@@ -{old_start_adjusted},{old_count} +{new_start_adjusted},{new_count} @@\n"
    return new_header

if __name__ == '__main__':
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Cancel deletions of lines starting with <curve> in a git patch file.')
    parser.add_argument('input_file', type=str, help='Path to the input patch file')
    parser.add_argument('output_file', type=str, help='Path to the output patch file')

    args = parser.parse_args()

    # Process the patch file
    cancel_curve_deletions(args.input_file, args.output_file)
