module.exports = (robot) ->
  robot.respond /photo (.*)/i, (res) ->

    temp = res.match[1]
    if not isNaN(temp) or isNaN(Date.parse(temp))
      res.send "Error: Invaild timestamp"
      return

    date = new Date(res.match[1])
    time = date.getTime()/1000 + 0.01

    robot.http("http://172.20.10.2:8089/image/#{time}")
      .header('Accept', 'application/json')
      .get() (err, response, body) ->

        if response.statusCode is 416
          res.send "Reading data is error"
          return

        if response.statusCode isnt 200
          res.send "Request didn't come back HTTP 200"
          return

        res.send "https://raw.githubusercontent.com/vyychenyy/Cloud-Platform/master/#{body}"
