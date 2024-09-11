#!/usr/bin/bash

# Sort the XML tags and attributes.
./sort_layout.py $1 $1

# Do in-place sanitization.
./sanitize.sed -i $1

# Extract the git patch.
PATCHFILE=git.patch
git diff $1 > $PATCHFILE

# Remove the changes that delete a curve.
./cancel_curve_deletions.py $PATCHFILE "$PATCHFILE"2

# Reset the file.
git checkout HEAD -- $1
# Apply the patch.
git apply --recount "$PATCHFILE"2
# Delete the patches.
rm $PATCHFILE
rm "$PATCHFILE"2
