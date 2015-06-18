HOW TO USE

To run the script, run the executable run.py with the --run option and your file. Ex. '$ ./run.py --run entries.txt'

also a help function, '% ./run.py --help

TESTS

To run '$ ./run.py --test'

IMPLEMENTATION

I modeled this in the follow way:

There is a run script - this script is as dumb as possible, and all that it knows how to do is read in lines from an
input file. It takes each line and passes in how many lines have been read as well as stripped down values.If there
are no more lines to be read, we print out the results.

There are two classes in my rolodex models. The Rolodex class as well as the RolodexEntry class. The Rolodex class
is what interacts with our run script. It handles the logic of seeing if the line is a valid entry, how to create a new
RolodexEntry, and how to print out all the entries. The RolodexEntry class is where the meat of the work is being done.
This is the class that actually parses out the information fed into it and assigns the correct values to the correct fields.
I went back and forth on where the parsing logic should be, namely I debated whether the RolodexEntry should do parsing
logic or just know how to create a new entry.

I decided that it made more sense for the RolodexEntry to own the logic from the point that we know it's a valid entry.
The only part that I'm not pleased with is the common_names and suffixes are on the Rolodex, as they are only used
in the RolodexEntry class, but I placed them there because I didn't want to incur the cost of recreating them for every entry.

Explanation of common_first_names:

Grabbed the names from : https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv which contains
the top 1000 girl and boy baby names from 1880 to 2009. I took this raw list, grabbed just the names, the compiled them
alphabetically by name and number of times they appeared in this list. ( sort | uniq -c )

The suffix list is a list of common last name suffixes that I scraped from:
http://en.wikipedia.org/wiki/List_of_family_name_affixes


