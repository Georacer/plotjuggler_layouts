#!/usr/bin/sed -f
# Reset axis ranges.
s|\(\s*\)<range .*/>|\1<range bottom="0" left="0" right="100" top="100" />|
# Reset the initial tab.
s|\(\s*\)<currentTabIndex index="[[:digit:]]" />|\1<currentTabIndex index="0" />|