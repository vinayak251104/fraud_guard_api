const dotenv = require('dotenv');
dotenv.config({ path: './config.env' });

const dns = require("dns");
dns.setServers(["1.1.1.1", "8.8.8.8"]);

const mongoose = require('mongoose');
const app = require('./app');

const port = process.env.PORT || 3001;
const DB = process.env.DATABASE.replace('<PASSWORD>', process.env.DATABASE_PASSWORD);

mongoose.connect(DB)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));

app.listen(port, () => {
  console.log(`App running on port ${port}...`);
});