# breakout_groups

generate breakout groups over multiple sessions - repetition of members in the breakout group is limited 

### design approach ###

The general approach:

* config.py contains the configuration and run parameters.  It reads a breakout_groups.ini file from the data folder.  If the file does not exist, it is created.  The breakout_groups.ini file is not managed by git and should be modified for the specific run.  See comments in the file.
* The member size and group size is pulled from the breakout_groups.ini file. The number of groups is calculated by members/group size.
* The possible combinations of the group size is generated, without replacement within a round or session.
* The combinations are gathered in sets of length of the number of groups, each member can only be present once in a session.
* Multiple session must account for least redundancy members in the same group across the sessions
* Labels are assigned to each group within a session.  If no label is provided, then the group is labeled group1, group2 ....etc

the output:

The output is a set of documents listing the breakout groups for each member.  There are several formats of the output to permit use as needed.
* a pdf
* a text file
* a csv file ??

### What is this repository for? ###

* Version 
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact
