const userController = require("../controllers/userController");
const express = require("express");
const router = express.Router();

router.route("/logs")
  .get(userController.logs);

router.route("/logs/:id")
  .get(userController.getLogById)
  .patch(userController.updateData)
  .delete(userController.deleteData);

router.post("/predict", userController.predict);

module.exports = router;