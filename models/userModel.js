const mongoose = require("mongoose");

const predictionSchema = new mongoose.Schema({
  request_id: {
    type: String,
    required: true
  },

  input: {
    Time: { type: Number, required: true },
    V1: { type: Number, required: true },
    V2: { type: Number, required: true },
    V3: { type: Number, required: true },
    V4: { type: Number, required: true },
    V5: { type: Number, required: true },
    V6: { type: Number, required: true },
    V7: { type: Number, required: true },
    V8: { type: Number, required: true },
    V9: { type: Number, required: true },
    V10: { type: Number, required: true },
    V11: { type: Number, required: true },
    V12: { type: Number, required: true },
    V13: { type: Number, required: true },
    V14: { type: Number, required: true },
    V15: { type: Number, required: true },
    V16: { type: Number, required: true },
    V17: { type: Number, required: true },
    V18: { type: Number, required: true },
    V19: { type: Number, required: true },
    V20: { type: Number, required: true },
    V21: { type: Number, required: true },
    V22: { type: Number, required: true },
    V23: { type: Number, required: true },
    V24: { type: Number, required: true },
    V25: { type: Number, required: true },
    V26: { type: Number, required: true },
    V27: { type: Number, required: true },
    V28: { type: Number, required: true },
    Amount: { type: Number, required: true }
  },

  output: {
    risk_score: { type: Number, required: true },
    decision: { type: String, required: true },
    threshold: { type: Number, required: true }
  },

  createdAt: {
    type: Date,
    default: Date.now
  }
});

predictionSchema.index({ createdAt: -1 });

module.exports = mongoose.model("Prediction", predictionSchema);