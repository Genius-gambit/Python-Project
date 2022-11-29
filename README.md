# Goal

A program which can extract the data from the json files and visualize them based on the number of users who are working on the document which is passed in an argument during the execution.

# Run Guide

1. Edit Makefile for sending any json file.
2. run "make" in bash

# Work Log

1. Created a Makefile which can compile the sources for the program.
2. Created srcs directory for all the python files.
3. Reading part done for json files.
4. Created function main which will run the main process
5. Created function read_data which will open the document for reading, extract the data and close the file descriptor to avoid leaks.
6. Created function which can fetch each row and return them as a string.