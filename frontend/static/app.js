const button = document.getElementById("load-button");
const result = document.getElementById("result");

async function loadBackendResponse() {
  result.textContent = "Loading...";

  try {
    const response = await fetch("/api/");
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    result.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    result.textContent = `Error: ${error.message}`;
  }
}

button.addEventListener("click", loadBackendResponse);
