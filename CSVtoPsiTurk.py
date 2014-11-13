import csv
import random

######PARSERS#######
def parseCSV (path):
    """Parses .csv experiment file (see documentation for .csv file formatting instructions.)
       It currently has the following columns: (int) "ITEM", (string) "CONDITION",
       (string) "FORM TEXT", (string) "QUESTION", (string) "TYPE", (string) "ANSWERS"
    """
    tasklist = []
    with open(path, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            tasklist.append(row)
    tasklist.remove(tasklist[0])
    return tasklist

def parseAns (answerRow):
    """parse answerRow to answerList[] by looking up the #'s"""
    answerList = answerRow.split("#")
    print answerList
    return answerList

######CHOOSING TASKS#######
def getRandomItem (tasks):
    """Tasks is a list of lines from the CSV file. We assume that all of the elements
       have the same item number.
       Currently, we assume that there is one condition per item.
       Be careful here^. In the future we'd like to select by Condition, not by Item.
       How to do that:
           1. We could separate tasks by (item,condition) and select a random condition, or
           2. We could select a random item and execute all the items that have the same condition as it.
    """
    return random.choice(tasks)
    
def ChooseRandomTasks (tasks):
    """Tasks is a list of lines from the CSV file. We shuffle all the tasks which
       have the same item number, and pass that to getRandomItem(), so that we get
       a randomly chosen task every time.
       At the end we have a set of N tasks, one which has ITEM=1, one which has ITEM=2
       and so on, the last task has ITEM=N.
       These tasks are the 'stuffing' for our HTML and JS templates.
    """
    sameItem = []
    HTMLstuffing = []
    for row in tasks:
        if not sameItem:
            sameItem.append(row)
        elif row[0]==sameItem[len(sameItem)-1][0]:
            sameItem.append(row)
        else:
            HTMLstuffing.append(getRandomItem(sameItem))
            sameItem = []
    if sameItem:
        HTMLstuffing.append(getRandomItem(sameItem))
    return HTMLstuffing
    
######FILL IN THE GAPS######
def JSgenForPsiTurk(stuffing, path):
    """Provides similar functionality to JSgen(). However, it works with
       NYU's PsiTurk software.
    """
    jsfile = open(path, 'w')
    jsfile.write('var Experiment = function() {\n\n')
    jsfile.write('\tvar trials = [\n')
    # Load the array of trials
    for trial in stuffing:
        jsfile.write('\t\t["%s", "%s", "%s", "%s", %s],\n'%(trial[0], trial[2], trial[3], trial[4], parseAns(trial[5])))
    jsfile.write('\t];')
    
    #what do we do at every question
    
    #how to handle responses
    
    #what to do at last question
    
    #other functionality
    
    jsfile.write('};')
    
######THIS RUNS EVERYTHING######
tasklist = parseCSV("/Users/val/Documents/UROP-Fall2015/urop/small_example.csv")
HTMLfilepath = "/Users/val/Documents/UROP-Fall2015/urop/psiturk-urop/"
HTMLstuffing = ChooseRandomTasks(tasklist)
JSgenForPsiTurk(HTMLstuffing, HTMLfilepath+"psiturkexp.js")

