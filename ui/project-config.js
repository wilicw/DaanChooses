let path = process.env.NODE_ENV == "development" ? "http://127.0.0.1:5000/api" : "/api"
module.exports = {
  apiPath: path
}
