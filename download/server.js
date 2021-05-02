var express = require('express')
var bodyParser = require('body-parser')
var cookieParser = require('cookie-parser')
var path = require('path')

var app = express()

app.use(bodyParser.json())
app.use(cookieParser())
app.use(bodyParser.urlencoded({ extended: false }))

// set json header
app.use(function(req, res, next) {
  res.contentType('application/json')
  next()
})

app.use(function (req, res, next) {
  console.info('[Logger]', req.method, req.originalUrl)
  next()
})

const downloadController = require('./downloadController')

app.use('/api/qichacha/', downloadController)

app.use('/', express.static(path.resolve(__dirname, './dist/'), {
  setHeaders: function (res, p, stat) {
    if (p.endsWith('index.html')) {
      res.set('Content-type', 'text/html')
    }
  }
}))

app.use(function (req, res) {
  res.status(404).send('')
})

app.listen(9912)

module.exports = app