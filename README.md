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
7. Created an array of list from the data to seperate rows.
8. Created a list to get the visitor_uuids from the array of list.
9. Working on adding the visitor_country for every visitor__uuid in dictionary.
10. Created function get_visitor_uuids which fetches the uniue id from the list.
11. Created function get_visitor_countries which collects the initials of the countries in the same order as in the data.
12. Created a function get count whoch can take the country and uuid as an argument and returns the total number of occurences of uuid along with the country from the argument.
13. Creating a dictionary which will hold the key value of uuid with vaues of the countries viewed in every count of occurences.
14. Got the algorithm for getting the keys and values with respect to the uuid
15. Got the histogram working for the occurences of countries with the given UUID.
16. Got the GUI for the first task of Number of Viewers for the countries based on the valid UUID.
17. 