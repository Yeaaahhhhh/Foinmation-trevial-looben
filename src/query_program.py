
import json
import sys
import os
import ast
def basicOperatorCheck(Q):
    '''
    Function: This function is a total check of parenthesis and "logic operators",i.e. (,),AND,OR,NOT
              If both of them return True, then it passes the basic check of operators
              It will change the Q, the argument, in str type, to a list, splited by spaces.

    Argument:Argument Q is a input query, in the type of string, for example: 'book:Harry AND line:Potter'

    Return: return a boolean value True or False
    '''
    syms = "!~`@#$%^&*_+=-|\;<,.>?/"+'{'+'}'
    for i in Q:
        if ':' not in Q:
            return False
        elif i in syms:
            return False

    Q = Q.replace('(','( ')  # make each brackets separately, i.e. (book:Harry) ---> '(', 'book:harry', ')'
    Q = Q.replace(')',' )')
    Q = Q.split(' ')  #turn the query into a list which contain several zone, term, logic operators
    if (parenCheck(Q) and andOrCheck(Q)) == True:
        return True
    return False

def organized(Q):
    '''
    Function: This function will edit a bit of the input query, make sure the editted query does not have empty string

    Argument: Q, the query user input

    Return: return a complete no empty spaces string
    '''
    Q = Q.split(' ')
    
    happyList = []  # a list that contain a bunch of terms, zones, logic operators.

    for i in range(0,len(Q)):
        if Q[i]:
            happyList.append(Q[i]) 
            
    sentence = " ".join(happyList)   #turn the list element into a string
    
    return sentence  
def parenCheck(Q):
    '''
    Function: This function check whether the input query has the paired parenthesis, the core is it should be balanced,
              so if meet the left brackets, the count +1, otherwise right brackets -1.
    Argument: Q, the user input query.

    Return: a boolean value, True or False.
    '''
    count = 0
    for i in Q:
        if i == '(':
            count += 1
        elif i == ')':
            count -= 1
        if count < 0:
            return False
    return count == 0

def andOrCheck(Q):
    '''
    Function: This function check whether the AND OR NOT operators are in the correct place, for example (AND, (OR, AND),OR), AND AND, OR OR, NOT NOT are not acceptable
              for a query, the user should try again.
    
    Argument: Q, the user input query.

    Return: A boolean value, True or False.
    '''
    
    if (Q[0].upper() == 'AND') or (Q[0].upper() == 'OR') or (Q[-1].upper() == 'AND') or (Q[-1].upper() == 'OR') or (Q[-1].upper() == 'NOT') or (Q[-1] == '('):
        return False
    for i in Q:
        if (i.upper() == 'AND' and Q[Q.index(i) - 1] == '(') or (i.upper() == 'OR' and Q[Q.index(i) - 1] == '(') or (i == ')' and Q[Q.index(i) - 1].upper() == 'OR') or (i == ')' and Q[Q.index(i) - 1].upper() == 'AND') or (i == ')' and Q[Q.index(i) -1].upper() == 'NOT') or (i == ')' and Q[Q.index(i) -1] == '(') :  # means the form '......(AND abcd...)' are not acceptable, should be '...AND (abcd ...)'
            return False
        elif (i.upper() == 'AND' and  Q[Q.index(i) - 1].upper() == 'AND') or (i.upper() == 'AND' and Q[Q.index(i) - 1].upper() == 'OR') or (i == 'OR'.upper() and  Q[Q.index(i) - 1].upper() == 'OR') or (i.upper() == 'OR' and Q[Q.index(i) - 1].upper() == 'AND'):   #AND OR should break up
            return False  
    return True
def checkLogiExist(Q):
    '''
    Function: This function check whether the logic operator and the colon are matched, the final count should be colon - 1 == the number of logic operators

    Argument: user input query

    return: A Boolean value, True or False  
    '''

    colons = 0
    logList = ['AND','OR']
    logCount = 0
    Q = Q.replace('(','( ')
    Q = Q.replace(')',' )')
    Q = Q.split(' ')
    for i in range(0,len(Q)):
        if ':' in Q[i]:
            colons +=1
        elif Q[i].upper() in logList:
            logCount += 1
    
    for i in Q:
        if (':' in i) and (i.index(':') == len(i)-1) and len(Q) -1 == Q.index(i):
            return False
    return (logCount == colons -1)

def getQuery():
    '''
    Function: This function get the user second input comand line argument, which is a query in '...abc:de AND asdf:fsa' form
              Then it check whether the input query are properly formed using above functions basicOperatorCheck and checkLogiExist()
              If something error occurred, it should print out a stderr message.
    
    Argument: None

    Return: a query in str type.

    
    '''
    try:
        query =  str(sys.argv[2])        #the second arg is the query
        
        if basicOperatorCheck(query) == False:
            sys.stderr.write('query logic operator has error, please input a valid query again\n')
            sys.exit()
        elif checkLogiExist(query) == False:
            sys.stderr.write('query zone and term not paired or lack of AND OR connection word, try again\n')
            sys.exit()
    except Exception:
        sys.stderr.write('User input argument error\n')
        sys.exit()                                
    return query

def getZoneTerm(Q):
    '''
    Function: This function will get the zone, and corresponding term in the query and append them into lists for later use

    Argument: Q, the query, which will be editted into a list.

    Return: two lists, the first one zoneNames contains all zone names in the query, second one contains all terms match to the zone.
    '''
    zone = ''
    term = ''
    stopsign = [')','(','AND','NOT','OR'] 
    zoneNames = []                           # record every zone name in this list
    terms = []                           # record every term name in this list accordingly to zones
    
    for i in range(0, len(Q)):           # read every token in query after split it.
        
        termhalf1 = ''
        
                      # above are prepared
        if ':' in Q[i] :                 # if : in a token, for example  ab:cd, 
            pos = Q[i].index(':')

            for st in range(0,pos):      # ab:cd, this for loop get the 'ab' which is the zone
                zone += Q[i][st]
            for en in range(pos+1,len(Q[i])): # get ab:cd's cd, i.e. the term
                termhalf1 += Q[i][en]
            zoneNames.append(zone.lower())
            zone = ''
            
            term = termhalf1 
            terms.append(term.lower())

    return zoneNames, terms

def qSearch(zone,term):
    '''
    Function: this function get the zone and term that are matched, then read the (zone name)file (.tsv file) in the given path
              it will get all formal elemnts by encoding utf-8
    
    Argument: zone and term, which will get from the zoneNames list and terms list.

    Return: the doc_id list created by indexCreation.py file and if the file does not exist, it will raise an error.
    '''
    
    try:
        with open(str(sys.argv[1])+ zone +".tsv", encoding='utf-8') as files:
            c = []
            ro = 1
            
            
            for line in files:
                if ro == 1 or ro == 2:
                    ro += 1
                    continue
                # print(line)
                columns = line.strip().split("\t")
                # print(columns[0])
                if term.lower() in columns[0]:
                    # print(columns[2])
                # convert postings(string) into list type
                    col = eval(columns[2])
                    c.extend(col)
                    c = list(set(c))  
                    c.sort()
                # return columns[2]
    except Exception:
        sys.stderr.write("no such zone file, please input a correct file name, please try again\n")
        sys.exit()
    return c
    
def getAll(zone):
    '''
    Function: this function will get all  doc_id from the tsv file, the indexCreation.py will insert a line at the very beginning to show all doc_ids,
              The function will be used later for 'NOT book:Lorax', we will use set operation to find its complement by implementing U set
    
    Argument: zone, as a file name without extension.

    Return: a set contains all doc_id in that appear in the zone.tsv file, first line index.
    '''
    with open(str(sys.argv[1])+zone+'.tsv', encoding='utf-8') as file:
        ro = 1
        for line in file:
            row1 = line.strip().split('\t')
            ro += 1
            if ro == 3:
                # print(row1)
                rowList = ast.literal_eval(row1[1])
                # print(rowList)
                postings = set(rowList)
                # print(postings)
                return postings

def getfileNames(path):
    '''
    Function: this function will get the file name of the given directory path, the return value will be used later with zoneNames list.

    Argument: path, which is the user input comand line argument[1]

    Return: return the file name only without .tsv extension
    '''
    filenames = os.listdir(path)
    for filename in filenames:
        base_name = os.path.basename(filename)
        file_name_without_extension = os.path.splitext(base_name)[0]
    return file_name_without_extension  #return a list contain a all zone.tsv file, each element is the filename.


def main():
    path = sys.argv[1]
    userQuery = getQuery()  # example: '( book:birthday potter dada) NOT title:helo OR (NOT review:good AND rate:eight)'  ---> 
    
    userQuery = organized(userQuery)
    userQuery = userQuery.replace(': ',':')
    tsvFileList = getfileNames(path)  #contain all zone name, filetype: tsv

    userQuery = userQuery.replace('(','( ')
    userQuery = userQuery.replace(')',' )')      
    Que = userQuery.split(' ')              # Que is a list, looks like ['(','book:birthday','potter', 'dada', 'AND', 'title:hello','kakaka']
        
    zoneNames, termNames = getZoneTerm(Que) 
    # zoneNames              [book,title,review,rate],
    # termNames              [birthday, helo, good,eight] all in string type
    # inputQuery to Que may be 'book:harry potter AND line:harry OR ( title:stone AND NOT rate:eight )'
    
    result = [] # contain several sets, for example ---->[{1,2,3,5,4}-{2,3,4},{3,5},{1,3}]
    
    logiOp = ['(',')','AND','OR','NOT']  
    
    for i in zoneNames:
        terms = termNames.pop(0)

        partResult = qSearch(i,terms)

        result.append(set(partResult))
    finalResult = ''
    k = 0

    loop = 0
    for i in Que:
        
        if i.upper() in logiOp:
            if i.upper() == 'AND':
                i = '&'  
            elif i.upper() == 'OR':
                i = '|'  
            elif i.upper() == 'NOT':
                i = '-'  
            finalResult += i

        elif Que.index(i) == len(Que)-1:

            finalResult += str(result[k])
            
        else:
            if Que[loop+1].upper() not in logiOp:
                pass
            else:
                finalResult += str(result[k])
                k += 1
        loop += 1
    # print(finalResult)
    # U = getAll()  # (review:a AND line:b) OR NOT (book:C OR review:D)  ---> ({1,2,3,4}&{2,3,4})|U-(asdasdaggsg)
    finalResult = finalResult.replace('&-','-')

    if '|-' in finalResult:
        start = finalResult.index('|-')
        for i in range(start, len(finalResult)):
            if finalResult[i] == '}':
                end = i
        finalResult = finalResult[:start]+finalResult[end+1:]
    
    U = getAll(zoneNames[0])
    if '-' == finalResult[0]:
        finalResult = str(U) + finalResult
    if '(-' in finalResult:
        finalResult = finalResult.replace('(-','('+str(U)+'-')
    evaSet = eval(finalResult) 
    evaSet = list(evaSet)
   
    evaSet.sort()
    for i in evaSet:
        sys.stdout.write(str(i))
        print('')
main()