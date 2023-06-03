#!pip install CodeforcesApiPy

import requests
import time
import datetime
import codeforces_api
import json

keywordList = [] # A LIST CONTAINING THE KEYWORDS YOUR LOOKING FOR FOR EXAMPLE ['par[N][LG]', trie] 
apiKey='YOUR CODEFORCES API KEY'
secret='YOUR CODEFORCES API SECRET'
handle='YOUR CODEFORCES HANDLE'
print(keywordList)

cf_api = codeforces_api.CodeforcesApi(apiKey, secret)

def getAPIresponse(apiRequest, *args, **kwargs):
    response = None
    for i in range(15):
        try:
            response = apiRequest(*args, **kwargs)
        except:
            pass
        else:
            return response
    return response

def hasKeyword(solution, keywordList):
    for keyword in keywordList:
        if solution.find(keyword) != -1:
            return True
    return False

good_problem_urls = open('urls.txt', 'w')
number_of_checked_solutions = 0

contest_list = cf_api._make_request(method='contest.list')
contest_list.reverse()

#problems = cf_api.problemset_problems()
#problems = problems['problems']


for contest in contest_list:
    print(contest['id'])
    if contest['phase'] == 'FINISHED':
        print('looking through ' + str(contest['id']))
        mysubs = getAPIresponse(cf_api.contest_status, contest['id'], handle=handle)
        if mysubs is None:
          continue
        for sub in mysubs:
            if sub.verdict == 'OK':
                number_of_checked_solutions += 1
                print('getting solution for problem ' + str(sub.problem.index))
                solution = getAPIresponse(codeforces_api.CodeforcesParser.get_solution, cf_api, contest_id=contest['id'], submit_id=sub.id)
                if solution is None:
                  continue
                number_of_checked_solutions += (solution != None)
                if hasKeyword(solution, keywordList):
                    problem_url = 'codeforces.com/contest/' + str(contest['id']) + '/problem/' + str(sub.problem.index)
                    print('problem found with url ' + problem_url)
                    good_problem_urls.write(problem_url + '\n')
               
print('checked ' + str(number_of_checked_solutions) + ' different accepted submissions')
