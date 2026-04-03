const axios = require("axios");
const { v4: uuidv4 } = require("uuid");
const Model = require("./../models/userModel");

const ML_URL = process.env.ML_URL || "http://127.0.0.1:8000";

exports.logs = async (req, res) => {
  try {
    const { page = 1, limit = 10, sort = "-createdAt" } = req.query;

    const filters = {};
    if (req.query.decision) {
      filters["output.decision"] = req.query.decision;
    }

    const pageNum = Number(page);
    const limitNum = Math.min(Number(limit), 100);
    const skip = (pageNum - 1) * limitNum;

    const logs = await Model.find(filters)
      .select("request_id input output createdAt")
      .sort(sort)
      .skip(skip)
      .limit(limitNum);

    const total = await Model.countDocuments(filters);

    res.status(200).json({
      status: "success",
      results: logs.length,
      total,
      page: Number(page),
      data: logs
    });

  } catch (err) {
    res.status(500).json({
      status: "error",
      message: err.message
    });
  }
};

exports.getLogById = async (req, res) => {
  try {
    const logById = await Model.findById(req.params.id);
    if (!logById) {
      return res.status(404).json({
        status: "fail",
        message: "Log not found"
      });
    }
    res.status(200).json({
      status: "success",
      data: { logById }
    });
  } catch (err) {
    res.status(404).json({
      status: "fail",
      message: err.message
    });
  }
};

exports.predict = async (req, res) => {
  try {
    if (!req.body || Object.keys(req.body).length === 0) {
      return res.status(400).json({
        status: "fail",
        message: "Input data is required"
      });
    }

    const inputData = req.body;
    const response = await axios.post(`${ML_URL}/predict`, inputData);
    const output = response.data;
    const requestId = uuidv4();

    if (output.error) {
      return res.status(400).json({
        status: "error",
        message: output.error
      });
    }

    const prediction = new Model({
      request_id: requestId,
      input: inputData,
      output: output
    });

    await prediction.save();

    res.status(200).json({
      status: "success",
      data: {
        request_id: requestId,
        input: inputData,
        risk_score: output.risk_score,
        decision: output.decision,
        threshold: output.threshold
      }
    });
  } catch (err) {
    if (err.response) {
      return res.status(500).json({
        status: "error",
        message: "ML service error",
        details: err.response.data
      });
    }
    res.status(500).json({
      status: "error",
      message: err.message
    });
  }
};

exports.updateData = async (req, res) => {
  try {
    const updatedData = await Model.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true
    });
    res.status(200).json({
      status: "success",
      data: { updatedData }
    });
  } catch (err) {
    res.status(400).json({
      status: "fail",
      message: err
    });
  }
};

exports.deleteData = async (req, res) => {
  try {
    await Model.findByIdAndDelete(req.params.id);
    res.status(204).json({
      status: "success",
      data: null
    });
  } catch (err) {
    res.status(404).json({
      status: "fail",
      message: err
    });
  }
};