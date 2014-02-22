import re

import SushiJSON
from .SushiJSON import SushiJSONParser

SUSHIJSONTEST_BEFOREAFTER_DELIM			= "beforeafter>" #delimiter of the slectors of "befrore" and "after"
SUSHIJSONTEST_TESTCASE_DELIM			= "test>"	# test commands delim.
SUSHIJSONTEST_API_SETTESTBEFOREAFTER	= "setTestBeforeAfter"
SETTESTBEFOREAFTER_BEFORESELECTORS		= "beforeselectors"
SETTESTBEFOREAFTER_AFTERSELECTORS		= "afterselectors"



class SushiJSONTestParser():
	@classmethod
	def parseTestSuite(self, data):
		# remove comment line then remove \n from data, before parse. this sequence is need for generate testcases. it's not good...
		data = re.sub(r'//.*', r'', data)
		data = data.replace("\n", "")
		
		splitted = data.split(SUSHIJSONTEST_TESTCASE_DELIM)
		
		beforeAfterBase = splitted[0]

		command, params = SushiJSONParser.parseStraight(beforeAfterBase)[0]
		assert SUSHIJSONTEST_BEFOREAFTER_DELIM in command, "SushiJSONTests must start with " + SUSHIJSONTEST_BEFOREAFTER_DELIM + " statement."

		# extract selectors.
		beforeSelectors = params[SETTESTBEFOREAFTER_BEFORESELECTORS]
		afterSelectors = params[SETTESTBEFOREAFTER_AFTERSELECTORS]

		testCases = splitted[1:]

		def addBeforeAndAfter(testCase):
			parsedCommandsAndParams = SushiJSONParser.parseStraight(testCase)

			parsedCommandsAndParams.insert(0, (SETTESTBEFOREAFTER_BEFORESELECTORS, {SushiJSON.SUSHIJSON_KEYWORD_SELECTORS:beforeSelectors}))
			parsedCommandsAndParams.append((SETTESTBEFOREAFTER_AFTERSELECTORS, {SushiJSON.SUSHIJSON_KEYWORD_SELECTORS:afterSelectors}))
			
			return parsedCommandsAndParams
			
		return [addBeforeAndAfter(testCase) for testCase in testCases]

