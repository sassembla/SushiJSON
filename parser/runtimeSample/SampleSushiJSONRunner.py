import argparse

from ..SushiJSON import SushiJSONParser



# load args from shell input.
parser = argparse.ArgumentParser()
parser.add_argument('file')

args = parser.parse_args()

data = ""
with open(args.file) as f:
	data = f.read()


# define api.
def runAPI(command, params):

	# print "message" value
	if command == "helloWorld":
		assert "message" in params, "helloWorld requires 'message' param."
		
		print(params["message"])


	# print "message" then run selectors if "selectors" param is exist in param.
	elif command == "sequence":
		assert "message" in params, "sequence requires 'message' param."
		message = "the param of " + params["message"]

		print(message)

		SushiJSONParser.runSelectors(
			params,
			["message"],
			[message],
			runAPI
		)

	# run selectors simply.
	elif command == "run":
		SushiJSONParser.runSelectors(
			params,
			[],
			[],
			runAPI
		)

	else:
		print("undefined api.", command)

# run
[runAPI(command, params) for command, params in SushiJSONParser.parseFromFile(data)]



