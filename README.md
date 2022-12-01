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
15. Got the GUI for the first task of Number of Viewers for the countries based on the valid UUID.
16. Histogram working for the occurences of countries with the given UUID.
17. Histogram working for the occurences of continents with the given UUID.
18. Histogram working for the occurences for browsers with the given UUID.
19. Histogram working for the occurences for specific browsers with the given UUID.
20. Created a function get_count_conts for getting the number of occurences after converting the country codes to continent names.
21. Created a function get_count_brows for getting the number of occurences for every uuid viewing their browsers.
22. Created a function get_count_sbrows for getting the number of occurences for every uuid viewing their common browsers.
23. Created a function create_dict_uuid_conts for getting the dictionary of continents with the given UUID.
24. Created a function create_dict_uuid_brows for getting the dictionary of browsers with the given UUID.
25. Created a function create_dict_uuid_sbrows for getting the dictionary of common browsers with the given UUID.
26. Created a function filt_brows for filtering the name of the browser along with the version.
27. Created a function get_hist_countries for building the histogram for the countries.
28. Created a function get_hist_continents for building the histogram for the continents.
29. Created a function get_hist_browser for building the histogram for the browsers.
30. Created a function get_hist_sbrowser for building the histogram for the common browsers.
31. 