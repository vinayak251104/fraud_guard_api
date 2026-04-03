const express = require("express");
const app = express();

// middleware
app.use(express.json());

// routes
const userRouter = require("./routers/userRouter");
app.use("/api/v1", userRouter);

// To check if the API is running or not
app.get("/", (req, res) => {
  res.status(200).json({
    status: "success",
    message: "API is running"
  });
});

// global error fallback for undefined routes
app.use((req, res) => {
  res.status(404).json({
    status: "fail",
    message: `Route ${req.originalUrl} not found`
  });
});

module.exports = app;