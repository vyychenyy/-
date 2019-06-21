module.exports = (robot) ->
	robot.catchAll (res) ->
		res.send "Error: Undefined Instruction"
