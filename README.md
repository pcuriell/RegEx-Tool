# RegEx-Tool
A tool that allows for real time RegEx check of documents.

Status:
  As of 4/2/2021, This app Regex functionally works fine. Many of the options are hardcoded. Ideas to improve the tool would be:
    -Allow to choose the source file (currently hardcoded)
    -Show all matches on a tab and add go-to functionality.
    -Improve the GUI.
    -Complex but usefull: Add RegEx groups functionality. Even add an export to excel or csv as a table functionality.
    -Ignore cases (which are used to improve performance skipping redundant RegEx searches) are hardcoded. Maybe add an option to manipulate this.
    -Use re.compile instead of re.search to improve performance.
