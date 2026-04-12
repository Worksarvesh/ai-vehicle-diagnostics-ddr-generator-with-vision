const form = document.getElementById("diagnostic-form");
const resultSection = document.getElementById("result");
const statusBox = document.getElementById("status-box");
const resultBody = document.getElementById("result-body");

const API_BASE = "http://localhost:8000";

function buildPayload(formData) {
  return {
    engine_temp: parseFloat(formData.get("engine_temp")),
    brake_wear_pct: parseFloat(formData.get("brake_wear_pct")),
    battery_voltage: parseFloat(formData.get("battery_voltage")),
    tire_pressure: parseFloat(formData.get("tire_pressure")),
    chain_tension: parseFloat(formData.get("chain_tension")),
    ambient_temp: parseFloat(formData.get("ambient_temp")),
    smoke_detected: formData.get("smoke_detected") === "on",
    abnormal_noise: formData.get("abnormal_noise") === "on",
  };
}

function showResult(success, html, theme = "success") {
  resultSection.classList.remove("hidden");
  statusBox.innerHTML = html;
  statusBox.className = `status-box ${theme}`;
}

async function submitHandler(event) {
  event.preventDefault();
  resultSection.classList.add("hidden");
  statusBox.className = "status-box loading";
  statusBox.innerHTML = "Predicting vehicle diagnostics...";
  resultSection.classList.remove("hidden");

  const formData = new FormData(form);
  const apiKey = formData.get("api_key");
  const imageInput = document.getElementById("inspection_image");

  formData.set("smoke_detected", formData.get("smoke_detected") === "on");
  formData.set("abnormal_noise", formData.get("abnormal_noise") === "on");

  if (imageInput.files.length > 0) {
    formData.set("image", imageInput.files[0]);
  }

  try {
    const response = await fetch(`${API_BASE}/predict-image`, {
      method: "POST",
      headers: {
        "X-API-KEY": apiKey,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorPayload = await response.json();
      throw new Error(errorPayload.detail || "Prediction request failed.");
    }

    const data = await response.json();
    statusBox.innerHTML = "Prediction complete";
    statusBox.className = "status-box success";
    resultBody.innerHTML = `
      <div class="result-card">
        <h2>Severity: ${data.predicted_severity}</h2>
        <p><strong>Confidence:</strong> ${Math.round(data.confidence * 100)}%</p>
        <h3>Probability distribution</h3>
        <ul>
          ${Object.entries(data.probabilities)
            .map(
              ([level, score]) =>
                `<li>${level}: ${Math.round(score * 100)}%</li>`
            )
            .join("")}
        </ul>
        ${data.image_features ? `<h3>Image feature summary</h3><ul>${Object.entries(data.image_features).map(([name, value]) => `<li>${name}: ${value}</li>`).join("")}</ul>` : ""}
        <p class="note">${data.message}</p>
      </div>
    `;
  } catch (error) {
    showResult(false, `<strong>Error:</strong> ${error.message}`, "error");
    resultBody.innerHTML = "";
  }
}

form.addEventListener("submit", submitHandler);
