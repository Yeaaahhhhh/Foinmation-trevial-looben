All your code should go here and nowhere else.


# 

How to install any libraries that are needed and for which you have the approval of the instructor. Make sure you test your own instructions on a lab machine.
Clear instructions on how to use your programs, including at least one example showing all parameters.
A discussion of which errors your programs detect and how these errors are handled.

# libraries
  

# run program
There are two programs that gonna use, one is indexCreation.py, another is query_program.py. The lines below show how to use them.

  1. create index files for each zone
    assume the current directory is src, run:
      python3 ./indexCreation.py ../data/movie_plots.json ../data/
    
    argument 1 is the path to the json file you want to read from,
    argument 2 is the path to the directory that the index files will be stored.

  2. querys
    
    assume the current directory is src, type and run:
      python3 ./query_program.py ../data/ 'book:Lorax AND line:you'

    comand line argument 1 is the json file the tsv file that are stored
    comand line argument 2 is the query that user wanna search/input.
    When input the command line argument, the user has to add Apostrophe (qotation mark) from the start and at the end,
    for example:
      the user query(command line argument[2]) is: 'book:Lorax AND line:you'
    the result will be printed to stdout, one per line, in ascending order, for example,
    0
    2
    3
    5

# Algorithms and Data Structure used
  - Index Creation

    Add all tokens and postings to a dictionary within seconds:
      read every document in the json object, for each zone, 
      get all the terms, use functions wordListCaseSensitive(terms), 
      removePunctuation(terms), and list(set(terms)) to convert terms into 
      tokens.
      Since we get the term, the current document must contain this term.
      Create a dictionary, 
      If there is not such a term in the dictionary already,
      simply store term as the key, and a list containing the current doc_id as the value.
      or If there is such a term in the dictionary,
      append current doc_id to the value(a list contains doc_id).

  - Query Get IDs
      The main idea of the query is to seperate them using a string.split(' '), into a list,
      Then we will find the zone and term names respectively
      When implementing boolean.py moudule, it will change all 'AND', 'OR', 'NOT' words into &,|,~ form
      Then we will combine the zone:term group with those AND OR NOT logic operators
      The zone:term group will return the corresponding posting, the third position, which contain the stored ids in a list
      We will change the str type list into a list and then turn them into a Set
        for example: '[1,2,3,4,5]'-->[1,2,3,4,5]-->{1,2,3,4,5}
      Then we will use boolean algebra parse internal function and Set operation to find the Union or intersection
        for example:  {1,2,3,4,5} &{1,2,3,4}
      Finally we use python internal function eval() to turn the Set operation and get the final answer
        for example: 'eval({1,2,3,4,5}&{1,2,3,4})
                  ==>{1,2,3,4}
        We will print them out one per line
    **As long as there are some characters in the term, for example, the word 'to' is in word 'tomorrow', then the doc_id of both terms will be returned **
# Assumptions and Errors detected
  
  - Index Creation
    All the checks are done in functions checkId(data) and checkZone(data)
    - Each document must have one required field called doc_id
      print to stderr and exit the program if any document does not have a filed called doc_id
    - Each doc_id must be an integer
      print to stderr and exit the program if any doc_id is not an integer
    - No two documents have the same id
      print to stderr and exit the program if there are two documents have the same id
    - each document has at least one zone with some text   associated with it
      print to stderr and exit the program if any document has only doc_id, and no text in a zone
    - each zone name must be a single token(np space, no punctuations)
      print to stderr and exit the program if any zone name is not a single token

  - Query Program
   ************ -------------> Assumption: The query should be input by a English Keyboard!
    1. the program check whether the parenthesis are paired. If not, print to stderr and exit the program

    2. The program check whether the AND OR NOT logic operators are in correct position
      - for example, AND AND cannot be continuous, (AND, (OR, (), NOT), and so on cannot be in this form (more details in query_program)

    3. The program considers the user input query with lowercase Operator:
      - For example, book:Lorax and line:you, 'and' is in lower case

    4. The program considers if the user input a query in form of 'NOT book:you'
      We will get a total Set that has all doc_id in it and use it to subtract the Set that book:you returned

    5. if the query is in form of 'book: Lorax', i.e. it has a space between zone and term, we can still get the term using a for loop.

    6. If the query has AND, OR, AND NOT, OR NOT Operator, we will use set operators &,|,-, to find the intersection, union, and difference respectively.
      i.e. the logic operators cannot be a query term or zone.

    7. If the input contains a empty string after use list.split(), remove it and return it with the complete sentence.

    8. If the query does not contain ':', print to stderr and exit the program

    9. If the query only contains 'python query_program.py' without command line arguments or with only one command line argument, or the command line arguments not properly written, print to stderr and exit the program.

    10. If the query wanna search a zone that does not in the tsv file, print to stderr and exit the program(no such zone file, please input a correct file name)

    11. Typically user input is (book:Lorax) AND (...) the parenthesis contains no space, so we add a space to turn them into a '( ',' )' form

    12. For a long boolean query, the number of colons will be equal to the number of ('AND' or 'OR') + 1, if not match, then the user input query contains error.
        Then print to stderr and exit the program.

    13. If user input query, its zone or/and term are in lowercase or uppercase, turn all of them into lowercase.

    14. If the user query contains !~`@#$%^&*_+=-{}|\;<,.>?/ symbols, print to stderr and exit the program as symbols error since the indexCreation program removes all those punctuations.
    
    15. If user input like: 'book:      Lorax' or 'book     :abc', the spaces will be removed.
# References: 
  write to a TSV file:
    https://riptutorial.com/python/example/26946/writing-a-tsv-file
    https://stackoverflow.com/questions/50514973/how-to-write-list-elements-into-a-tab-separated-file

  remove punctuations in every word in a list using .translate()
    https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate
  
  normalization of accent Marks:
  https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string

  Check Parenthesis are paired:
  https://stackoverflow.com/questions/38833819/python-program-to-check-matching-of-simple-parentheses

  get all file names in a path:
  https://stackoverflow.com/questions/22207936/how-to-find-files-and-skip-directories-in-os-listdir

  Set operation using python eval function:
  https://realpython.com/python-eval-function/




