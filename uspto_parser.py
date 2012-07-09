import BeautifulSoup, nltk, re, xlrd, xlwt

def title_ex(htmlString):
    regex = r'\<font size=\"\+1\"\>.+?</font>'
    a = re.findall(regex, htmlString, re.S)
    if len(a) == 1:
        ret = nltk.clean_html(a[0])
        ret = ret.replace("\n", "")
        ret = ret.strip()
    else:
        ret = "Title Error"

    return ret

def ab_ext(htmlString):
    a = htmlString.find("Abstract")
    b = htmlString.find("Inventors")
    ab = nltk.clean_html(htmlString[a:b])
    ab = ab.replace("\n", "")
    return ab

# this returns the text of the claims
def claim_ext(htmlString):
    a = htmlString.find("Claims")
    b = htmlString.find("Description")
    elem = nltk.clean_html(htmlString[a:b])
    return elem

# this returns the count of the claims
def claim_cnt2(htmlString):
    b = claim_ext(htmlString)
    regex = r"\d{1,4}"
    n = re.findall(regex, b)
    high = 0
    for elem in n:
        elem = int(elem)
        if elem > high:
            high = elem
        else:
            pass
    
    
    return high

def claim_cnt(htmlString):
    b = claim_ext(htmlString)
    regex = r"\n [0-9]+\."
    n = re.findall(regex, b)
    retval = len(n) + 1
    return retval
    

# we need asignees
def asig_ext(htmlString):
    a = htmlString.find("Assignee")
    b = htmlString.find("Appl. No.")

    if (a == -1) or (b == -1):
        # The there is no assignee
        elem = "No Seperate Assignee"

    else:
        elem = nltk.clean_html(htmlString[a:b])
        elem = elem.replace("\n", "")
        elem = elem.replace("Assignee:", "")
    return elem

# assignee counts
def asig_cnt(htmlString):
    b = asig_ext(htmlString)
    b = b.replace("\n", "")
    regex = r"\([\S]+[\s]+[\S]+[\s]+\)"
    n = re.findall(regex,b)
    return len(n), n

# we application year
def app_yr(htmlString):
    strIN = htmlString.replace("\n", "")
    a = re.findall(r'Filed:.+?(?:January|February|March|April|May|June|July|August|September|October|November|December)\W{1,4}\d{1,2},\W{1,5}\d{4}', strIN)
    b = re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\W{1,4}\d{1,2},\W{1,5}\d{4}', a[0])
    return b[0]
    

# we need grant year. It always appears before the Abstract
def grant_yr(htmlString):
    if "<b>Abstract</b>" in htmlString:
        b = htmlString.find("<b>Abstract</b>")
    else:
        b = htmlString.find("Inventors:")

    if b < 0:
        retval = "ERROR WITH FILE"
    else:
        slicer = htmlString[:b]
        dater = re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\W{1,4}\d{1,2},\W{1,5}\d{4}', slicer)
        retval = dater[0]

    return retval


def invent_ext(htmlString):
    start = htmlString.find("Inventors:")
    end = htmlString.find("Assignee:")
    end2 = htmlString.find("Appl. No.:")
    if start == -1:
        extract = "No Inventors Listed"
    else:
        if end == -1:
            extract = htmlString[start+11:end2]
            extract = nltk.clean_html(extract)
        else:
            extract = htmlString[start+11:end]
            extract = nltk.clean_html(extract)
    
    return extract

def invent_locList(htmlString):
    inventTTT = invent_ext(htmlString)
    a = re.findall(r'\(.+?,.+?\)', inventTTT)
    for ee in range(len(a)): a[ee] = a[ee].replace("(", "")
    for ee in range(len(a)): a[ee] = a[ee].replace(")", "")
    return a
    

# we need number of inventors
def invent_cnt(htmlString):
    #a = invent_ext(htmlString)
    b = invent_locList(htmlString)
    cnt = len(b)
    return cnt


# We need a function for government interests
def gov_int(htmlString):
    # Gov interest always comes after Primary Examiner but before claims sect
    a = htmlString.find("Primary Examiner")
    b = htmlString.find("<i>Claims</i>")

    if (a > -1) and (b > -1):
        slicer = htmlString[a:b]
    else:
        slicer = htmlString
    if "<i>Government Interests</i>" in slicer:
        return 1
    else:
        return 0

# We need to get cited patents
def pat_cit(htmlString):
    # There are two Sections of Patents: U.S. and foreign
    # Then there might be an Other References section
    # Primary Examiner is always the last element after the references
    # This function will determine which of these are present and the take a slice

    # first, figure out if other references is present
    
    if "<b>Other References</b>" in htmlString:
        b = htmlString.find("<b>Other References</b>")
    else:
        b = htmlString.find("<i>Primary Examiner:</i>")
    if "<b>U.S. Patent Documents</b>" in htmlString:
        a = htmlString.find("<b>U.S. Patent Documents</b>")
        c = 2
        if "<b>Foreign Patent Documents</b>" in htmlString:
            c = 4
        else:
            pass

        
    else:
        a = htmlString.find("<b>Foreign Patent Documents</b>")
        c = 2
    if (a < 0) or (b < 0) or (a > b):
        #print "I'm in here"
        #print a
        #print b
        retval = 0
    else:
        slicer = htmlString[a:b]
        totaler = re.findall("<tr>", slicer)
        retval = len(totaler) - c

    return retval


# now we need a function for non-patent references
def nonpat_cit(htmlString):
    if "<b>Other References</b>" in htmlString:
        # set a
        a = htmlString.find("<b>Other References</b>")
        if "<i>Primary Examiner:</i>" in htmlString:
            b = htmlString.find("<i>Primary Examiner:</i>")
            slicer = htmlString[a:b]
            #print a
            #print b
            #print slicer
            totaler = re.findall("<br />", slicer)

            if len(totaler) == 0:
                totaler = re.findall("<br>", slicer)
                retval = len(totaler)-1
            else:
                retval = len(totaler)-1
                        
            
            
        else:
            retval = "ERROR: Improper HTML"
    else:
        
        retval = 0

    return retval


def pos_dis(strIn):
    """
    The purpose of this function is to remove all the words in the abstract that are not either adjectives or nouns
    """
    tok = nltk.word_tokenize(strIn)
    pos = nltk.pos_tag(tok)
    out = []
    for ee in pos:
        if (ee[1][:1] == "N") or (ee[1][:1] == "J"):
            out.append(ee[0])
        else:
            pass

    return out


def commonList():
    
    # before the matcher, I need to have a list of common words
    commonList1 = ["the", "of", "and", "a", "an", "to", "in", "he", "have", "it", "that", "for", "they", "I", "with", "as", "not", "on", "she", "at", "by", "this", "we", "you", "do", "but", "from", "or", "which", "one", "would", "all", "will", "there", "say", "who", "make", "when", "can", "more", "if", "no", "man", "out", "other", "so", "what", "time", "up", "go", "about", "than", "into", "could", "state", "only", "new", "year", "some", "take", "come", "these", "know", "see", "use", "get", "like", "then", "first", "any", "work", "now", "may", "such", "give", "over", "think", "most", "even", "find", "day", "also", "after", "way", "many", "must", "look", "before", "great", "back", "through", "long", "where", "much", "should", "well", "people", "down", "own", "just", "because", "good", "each", "those", "feel", "seem", "how", "high", "too", "place", "little", "world", "very", "still", "nation", "hand", "old", "life", "tell", "write", "become", "here", "show", "house", "both", "between", "need", "mean", "call", "develop", "under", "last", "right", "move", "thing", "general", "school", "never", "same", "another", "begin", "while", "number", "part", "turn", "real", "leave", "might", "want", "point", "form", "off", "child", "few", "small", "since", "against", "ask", "late", "home", "interest", "large", "person", "end", "open", "public", "follow", "during", "present", "without", "again", "hold", "govern", "around", "possible", "head", "consider", "word", "program", "problem", "however", "lead", "system", "set", "order", "eye", "plan", "run", "keep", "face", "fact", "group", "play", "stand", "increase", "early", "course", "change", "help", "line", "method", "materials", "(", ")", "approach", "results", "system", "properties", "growth", "activity", "different", "specific", "large", "potential", "control", "analysis", "applications", "single", "structure", "important"]

    return commonList1



def matcher2(list,strComp):
    n = 0
    matches = []

    commonList2 = commonList()
    
    for elem in list:
        if elem in strComp:
            if elem in commonList2:
                pass
            else:
                matches.append(elem)
        else:
            pass

    return len(matches), matches
            

def matcher(list,strComp):
    n = 0
    matches = []
    
    for elem in list:
        if elem in strComp:
            matches.append(elem)
        else:
            pass

    return len(matches), matches
            


        
        

