module.exports = (robot) ->
	robot.respond /cpu/i, (res) ->
		robot.http("http://172.20.10.2:8089/cpu")
			.header('Accept', 'application/json')
			.get() (err, response, body) ->

				if response.statusCode isnt 200
					res.send "Request didn't come back HTTP 200"
					return

				# data = JSON.parse body
				res.send "#{body}"
