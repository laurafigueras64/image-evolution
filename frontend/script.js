const btn = document.getElementById("generate-btn");
const promptInput = document.getElementById("prompt");

const MODEL_ORDER = ["sd-tiny", "sd-small", "sd-turbo"];

function getCard(modelKey) {
  return document.getElementById(`card-${modelKey}`);
}

function setCardLoading(modelKey) {
  const card = getCard(modelKey);
  card.classList.add("active");
  card.querySelector(".placeholder").classList.add("hidden");
  card.querySelector(".result-img").classList.add("hidden");
  card.querySelector(".spinner").classList.remove("hidden");
}

function setCardResult(modelKey, base64) {
  const card = getCard(modelKey);
  const img = card.querySelector(".result-img");
  img.src = `data:image/png;base64,${base64}`;
  img.classList.remove("hidden");
  card.querySelector(".spinner").classList.add("hidden");
  card.classList.remove("active");
}

function resetCards() {
  MODEL_ORDER.forEach((key) => {
    const card = getCard(key);
    card.classList.remove("active");
    card.querySelector(".placeholder").classList.remove("hidden");
    card.querySelector(".spinner").classList.add("hidden");
    card.querySelector(".result-img").classList.add("hidden");
  });
}

btn.addEventListener("click", async () => {
  const prompt = promptInput.value.trim();
  if (!prompt) return;

  btn.disabled = true;
  resetCards();

  // Show all spinners immediately so the user knows all three are queued
  MODEL_ORDER.forEach(setCardLoading);

  try {
    const response = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) throw new Error(`Server error: ${response.status}`);

    const data = await response.json();

    data.results.forEach(({ model, image_base64 }) => {
      setCardResult(model, image_base64);
    });
  } catch (err) {
    console.error("Generation failed:", err);
    MODEL_ORDER.forEach((key) => {
      const card = getCard(key);
      card.querySelector(".spinner").classList.add("hidden");
      card.querySelector(".placeholder").classList.remove("hidden");
      card.classList.remove("active");
    });
  } finally {
    btn.disabled = false;
  }
});

promptInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") btn.click();
});
