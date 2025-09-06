// backend/server.js
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
app.use(cors());
app.use(bodyParser.json());

// In-memory "database"
const users = {};
const FAKE_TOKEN = "mock-jwt-token";

// --- Auth Routes ---
app.post("/auth/register", (req, res) => {
  const { email, password } = req.body;
  if (users[email]) return res.status(400).json({ error: "User already exists" });
  users[email] = { email, password };
  return res.json({ verify_link: "http://localhost:8080/verify?token=123" });
});

app.post("/auth/login", (req, res) => {
  const { email, password } = req.body;
  if (!users[email] || users[email].password !== password) {
    return res.status(401).json({ error: "Invalid credentials" });
  }
  return res.json({ token: FAKE_TOKEN });
});

app.post("/auth/oauth/dev", (req, res) => {
  const { email } = req.body;
  return res.json({ token: "dev-token", email });
});

app.post("/auth/google", (req, res) => {
  const { id_token } = req.body;
  return res.json({ token: "google-token", email: "googleuser@example.com" });
});

// --- Chat Route ---
app.post("/chat", (req, res) => {
  const { question, language } = req.body;
  return res.json({ answer: `(${language}) You asked: ${question}` });
});

// --- Form Routes ---
app.post("/generate_form", (req, res) => {
  const { form_type, responses } = req.body;
  return res.json({ form: `Generated ${form_type} form with data: ${JSON.stringify(responses)}` });
});

app.post("/generate_form_pdf", (req, res) => {
  res.setHeader("Content-Type", "application/pdf");
  res.setHeader("Content-Disposition", "attachment; filename=form.pdf");
  res.send(Buffer.from("%PDF-1.4\n% Mock PDF\n", "utf-8"));
});

// --- Start Server ---
const PORT = 8080;
app.listen(PORT, () => console.log(`✅ API running at http://127.0.0.1:${PORT}`));
// --------------------