import json
import sys
import csv
import unicodedata
import string
def checkId(data):
  '''
  Function: 
    Check each document has a doc_id, check no two document have the same id, check doc_id must be an integer
  Arguments: 
    data: json object
  Return: 
    Boolean: return true if all the checks pass, otherwise, print stderr message and exit the program
  '''
  key_list = []
  for doc in data:
    if "doc_id" not in doc.keys():
      sys.stderr.write("Document does not have a doc_id, try again\n")
      sys.exit()
    else:
      try:
        doc_id = doc['doc_id']
        doc_id = int(doc_id)
      except:
        sys.stderr.write("not a valid id,try again\n")
        sys.exit()
      if doc_id not in key_list:
        key_list.append(int(doc['doc_id']))
      else:
        sys.stderr.write("repeated doc_id\n")
        sys.exit()
  return True

def checkZone(data):
  ''' 
  Function: 
    Check each zone name in each document must be a single token_df_postings_dict, 
    check each document must have at least one zone ,check each zone has some text
  Arguments:
    data: json object
  Return:
    Boolean: return true if all the checks pass, otherwise, print to stderr and exit the program
  '''
  punctuations = string.punctuation
  for doc in data:
    keys = doc.keys()
    if len(keys) <= 1:
      sys.stderr.write("At least one document doesn't have zones!\n")
      sys.exit()
    for zone in keys:
      if zone != 'doc_id':
        if doc[zone] == "":
          sys.stderr.write("no text")
          sys.exit()
        token_list = zone.split(" ")
        if len(token_list) > 1:
          sys.stderr.write("Zone name must be a single token! Cannot have spaces.\n")
          sys.exit()
        for char in zone:
          if char in punctuations:
            sys.stderr.write("Zone name must be a single token! Cannot have punctuations.\n")
            sys.exit()
  return True

def checkAll(data):
  '''
  Function: 
    Combine function checkZone and checkId 
  Arguments:
    data: json object
  Return:
    Boolean: return true if both functions return true
  '''
  checkId(data) & checkZone(data)

def removeAccentMarks(input_list):
  output_list = []
  for input_str in input_list:
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    output_list.append(u"".join([c for c in nfkd_form if not unicodedata.combining(c)])) 
  return output_list

def wordListCaseSensitive(word_list):
  '''
  Function: 
    Convert every word in a list to lowercase
  Arguments:
    word_List: list
  Return: 
    result_list: list 
  '''
  result_list = []
  for word in word_list:
    result_list.append(word.lower())
  return result_list

def createToken(zone,data):
  '''
  Function: 
    Create tokens for each zone, store tokens and their corrsponding postings to a dictionary,
    and sort them into a list by term name.
  Arguments:
    zone: name of the zone, type: str
    data: json object
  Return:
    merged_list: a list of tuples, where the first element in the tuple is the term name, 
    and the secound element is the postings list containing doc_ids
  '''
  term_list = []
  for doc in data:
    terms = doc[zone].split(" ")
    terms = wordListCaseSensitive(terms)
    terms = removePunctuation(terms)
    terms = removeAccentMarks(terms)
    terms = list(set(terms))
    
    terms.sort()
    for term in terms:
      temp_dict = {}
      temp_dict[term] = doc['doc_id']
      term_list.append(temp_dict)
  merged_dict = {}
  for dic in term_list:
    for k,v in dic.items():
      if k not in merged_dict:
        merged_dict[k] = [v]
      else:
        merged_dict[k].append(v)
  for i in merged_dict:
    merged_dict[i].sort()
  merged_list = sorted(merged_dict.items())
  return merged_list

def removePunctuation(input_list):
  '''
  Function: 
    Remove punctuations in every word in a list
  Arguments: 
    input_list: a list of strings
  Return:
    output_list: a list of strings with no punctuations
  '''
  punctuations = string.punctuation
  translator = str.maketrans("", "", punctuations)
  output_list = [s.translate(translator) for s in input_list]
  return output_list

def createTokenDfPostings(zone,data):
  '''
  Function:
    Create a dictionary that contains tokens, document frequency, and postings,
    with token as the key, and a tuple of df and postings as the value.
  Arguments:
    zone: name of the zone, type: str
    data: json object
  Return:
    token_df_postings_dict, 
      type - dictionary
      key - token
      value - tuple of df and postings list
  '''
  token_df_postings_dict = {}
  token_dict = createToken(zone, data)
  for i in token_dict:
    old_v = i[1]
    freq = len(old_v)
    token_df_postings_dict[i[0]] = (old_v,freq)
  return token_df_postings_dict

def getAllDocId(data):
  '''
  Function:
    get all the document ids in a json object
  Arguments:
    data: json object
  Return:
    doc_ids: a list of doc_id with type string
  '''
  doc_ids = []
  for doc in data:
    doc_ids.append(doc['doc_id'])
  doc_ids.sort()
  return doc_ids

def writeToTSV(fileName,token_df_postings_dict,data):
  '''
  Function: 
    write data into the tsv file. Here, data is three columns, with
      first column: token,
      second column: document frequency,
      third column: postings
  Arguments:
    filename: the name of the file to write to
    token_df_postings_dict: a dictionary that contains token, df, postings
    data: json object
  Return:
    no return
  '''
  all_docids = getAllDocId(data)
  # sys.argv[2]: path to the directory where the index files will be stored
  with open( fileName, 'wt', encoding='utf-8') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(['token','DF','postings'])
    tsv_writer.writerow(['',len(all_docids),'[' +','.join(all_docids) + ']'])
    for token, value in token_df_postings_dict.items():
      df = value[1]
      docIDs = value[0]
      tsv_writer.writerow([token,df,'[' + ','.join(docIDs) + ']'])

def getData():
  '''
  Function:
    Load json data from a json file.
  Arguments:
    None
  Return:
    data: a json object
  '''
  try:
    with open(sys.argv[1], "r") as f:
      data = json.load(f)
  except Exception:
    sys.stderr.write("inappropriate arguments, try again\n")
    sys.exit()
  return data

# return a list with all zones in data
def getAllZones(data):
  '''
  Function:
    get all the zones in the json object
  Arguments:
    data: json object
  Return:
    zones: a list of all the zones in the data
  '''
  zones = []
  for doc in data:
    keys = doc.keys()
    for zone in keys:
      if zone != 'doc_id':
        zones.append(zone)
  zones = list(set(zones))
  return zones

def createIndex():
  '''
  Function:
    create the index files by calling writeToTSV function
  Arguments:
    None
  Return:
    None
  '''
  data = getData()
  checkAll(data)
  zones = getAllZones(data)
  for zone in zones:
    token_df_postings_dict = createTokenDfPostings(zone,data)
    try:
      writeToTSV(sys.argv[2] + '/{}.tsv'.format(zone.lower()),token_df_postings_dict,data)
    except Exception:
      sys.stderr.write('storage path error or lack of command line argument\n')
      sys.exit()

if __name__ == "__main__":
  createIndex()