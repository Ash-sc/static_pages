var express = require('express')
var router = express.Router()
var path = require('path')
var fs = require('fs')
var execa = require('execa')

router.post('/gen', function(req, res) {
  const { data } = req.body
  console.log(data)
  const names = data.join(' ')
  const cmd = `python3 /root/static_pages/download/spider.py ${names}`

  try {
    execa.shellSync(cmd)
  } catch (e) {
    console.log(e)
  }

  res.status(200).json({
    result: 0,
    data: []
  })
})

router.post('/check', function(req, res) {
  setTimeout(() => {
    const resp = {
      result: 0,
      data: {
        end: false
      }
    }
    if (!fs.existsSync(path.join(__dirname, './dist/result.csv'))) {
      res.status(200).json()
    } else {
      const fileSize = execa.shellSync(`wc -c ${path.join(__dirname, './dist/result.csv')}`).stdout
      console.log(fileSize.split(' ').filter(i => i)[0], 222)

    }
    res.status(200).json()
  }, 4000)
})

// '/usr/local/opt/python@3.9/bin/python3.9 /Users/shenchuang/Documents/qichacha_spider/spider.py'

module.exports = router