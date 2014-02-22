import argparse

from ..SushiJSON import SushiJSONParser
from ..SushiJSONTest import SushiJSONTestParser



# load args from shell input.
parser = argparse.ArgumentParser()
parser.add_argument('file')

args = parser.parse_args()

data = ""
with open(args.file) as f:
	data = f.read()


testSuitesIdentity = "test:"
globalResults = {}

def addTestResult(sourceIdentity, result):
	globalResults[testSuitesIdentity].append({sourceIdentity:result})



# define api.
def runAPI(command, params):

	# print "message" value
	if command == "helloWorld":
		assert "message" in params, "helloWorld requires 'message' param."
		
		print(params["message"])

		addTestResult("helloWorld", {"output":params["message"]})


	# before and after 
	elif command == "beforeselectors":
		SushiJSONParser.runSelectors(
			params,
			[],
			[],
			runAPI
		)

	elif command == "afterselectors":
		SushiJSONParser.runSelectors(
			params,
			[],
			[],
			runAPI
		)

	elif command == "assertResult":
		assertResult(params)
		
	# elif command == 

	else:
		print("undefined api.", command)

testCases = SushiJSONTestParser.parseTestSuite(data)






# define test assertions
def assertResult(params):
	assert "id" in params, "assertResult requires 'id' param."
	
	assertionIdentity = params["id"]
	
	results = globalResults[testSuitesIdentity]
	
	if "contains" in params:
		containsDict = params["contains"]


		if containsDict in results:
			addTestResult(assertResult.__name__, {"result":"passed", "id":assertionIdentity})
			print("id:",assertionIdentity, "passed.")

		else:
			addTestResult(assertResult.__name__, {"result":"failed", "id":assertionIdentity})
			print("id:",assertionIdentity, "failed.")


# define testRunner
def runTestCase(testCase):
	globalResults[testSuitesIdentity] = []

	for testCommand, testParams in testCase:
		command, params = SushiJSONParser.composeParams(testCommand, testParams, None)
		runAPI(command, params)

	

[runTestCase(testCase) for testCase in testCases]

# use result if you wanna display it.
# print("test result", globalResults)


