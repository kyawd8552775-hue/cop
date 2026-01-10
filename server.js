const express = require("express");
const path = require("path");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.static(path.join(__dirname, "web")));
app.use("/data", express.static(path.join(__dirname, "data")));

app.get("/", (_, res) => res.sendFile(path.join(__dirname, "web", "index.html")));

const port = 3000;
app.listen(port, () => {
  console.log(`Server http://version2.com:${port} (set 127.0.0.1 version2.com in /etc/hosts)`);
});
