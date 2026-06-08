const metrics = {
  recall: {
    label: "Recall@10",
    values: [
      ["Two-stage", 0.0583816625],
      ["Hybrid blend", 0.0582711958],
      ["ItemKNN", 0.0579950290],
      ["Popularity", 0.0399337200],
      ["BPR", 0.0388842861],
      ["Content", 0.0149130075],
    ],
  },
  ndcg: {
    label: "NDCG@10",
    values: [
      ["ItemKNN", 0.0286756510],
      ["Two-stage", 0.0282948958],
      ["Hybrid blend", 0.0282572862],
      ["Popularity", 0.0188340037],
      ["BPR", 0.0177409376],
      ["Content", 0.0066181512],
    ],
  },
  coverage: {
    label: "Coverage@10",
    values: [
      ["Content", 0.7246973989],
      ["Two-stage", 0.2365009872],
      ["Hybrid blend", 0.2316078633],
      ["BPR", 0.2027641858],
      ["ItemKNN", 0.0901364924],
      ["Popularity", 0.0296162761],
    ],
  },
};

const recommendations = {
  1: [
    ["American Beauty (1999)", "Comedy | Drama", 0.7293],
    ["Shawshank Redemption, The (1994)", "Drama", 0.7209],
    ["Star Wars: Episode V - The Empire Strikes Back (1980)", "Action | Adventure | Drama | Sci-Fi | War", 0.7130],
    ["Babe (1995)", "Children's | Comedy | Drama", 0.6951],
    ["Silence of the Lambs, The (1991)", "Drama | Thriller", 0.6844],
    ["Stand by Me (1986)", "Adventure | Comedy | Drama", 0.6778],
  ],
  2: [
    ["Godfather, The (1972)", "Action | Crime | Drama", 0.7558],
    ["Schindler's List (1993)", "Drama | War", 0.7490],
    ["Good Will Hunting (1997)", "Drama", 0.7382],
    ["Fargo (1996)", "Crime | Drama | Thriller", 0.7363],
    ["Pulp Fiction (1994)", "Crime | Drama", 0.7249],
    ["Lethal Weapon (1987)", "Action | Comedy | Crime | Drama", 0.7086],
  ],
  3: [
    ["Men in Black (1997)", "Action | Adventure | Comedy | Sci-Fi", 0.7093],
    ["Lethal Weapon (1987)", "Action | Comedy | Crime | Drama", 0.6691],
    ["Romancing the Stone (1984)", "Action | Adventure | Comedy | Romance", 0.6673],
    ["Back to the Future (1985)", "Comedy | Sci-Fi", 0.6513],
    ["Terminator, The (1984)", "Action | Sci-Fi | Thriller", 0.6471],
    ["True Lies (1994)", "Action | Adventure | Comedy | Romance", 0.6443],
  ],
};

function formatMetric(value) {
  return value.toFixed(4);
}

function renderChart(metricKey) {
  const chart = document.querySelector("#chart");
  const active = metrics[metricKey];
  const max = Math.max(...active.values.map(([, value]) => value));

  chart.innerHTML = active.values
    .map(([name, value]) => {
      const width = Math.max(3, (value / max) * 100);
      return `
        <div class="bar-row">
          <div class="bar-label">${name}</div>
          <div class="bar-track" aria-hidden="true">
            <div class="bar-fill" style="width: ${width}%"></div>
          </div>
          <div class="bar-value">${formatMetric(value)}</div>
        </div>
      `;
    })
    .join("");
}

function renderRecommendations(userId) {
  const list = document.querySelector("#recommendation-list");
  const label = document.querySelector("#active-user-label");
  label.textContent = `User ${userId}`;
  list.innerHTML = recommendations[userId]
    .map(([title, genres, score], index) => {
      return `
        <li>
          <span class="rank">${String(index + 1).padStart(2, "0")}</span>
          <span>
            <span class="rec-title">${title}</span>
            <span class="rec-genres">${genres}</span>
          </span>
          <span class="rec-score">${score.toFixed(4)}</span>
        </li>
      `;
    })
    .join("");
}

function bindControls() {
  document.querySelectorAll(".tab").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("is-active"));
      button.classList.add("is-active");
      renderChart(button.dataset.metric);
    });
  });

  document.querySelectorAll(".user-button").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".user-button").forEach((item) => item.classList.remove("is-active"));
      button.classList.add("is-active");
      renderRecommendations(button.dataset.user);
    });
  });
}

function drawSignalCanvas() {
  const canvas = document.querySelector("#signal-canvas");
  const ctx = canvas.getContext("2d");
  const ratio = Math.max(1, window.devicePixelRatio || 1);
  const rect = canvas.getBoundingClientRect();
  canvas.width = Math.floor(rect.width * ratio);
  canvas.height = Math.floor(rect.height * ratio);
  ctx.scale(ratio, ratio);

  const width = rect.width;
  const height = rect.height;
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#fbfbfa";
  ctx.fillRect(0, 0, width, height);

  const columns = 38;
  const rows = 24;
  const cellW = width / columns;
  const cellH = height / rows;
  const colors = ["#2457d6", "#087f6f", "#c84b31", "#c18a00"];

  ctx.globalAlpha = 0.18;
  ctx.strokeStyle = "#171717";
  ctx.lineWidth = 1;
  for (let x = 0; x <= columns; x += 1) {
    ctx.beginPath();
    ctx.moveTo(x * cellW, 0);
    ctx.lineTo(x * cellW, height);
    ctx.stroke();
  }
  for (let y = 0; y <= rows; y += 1) {
    ctx.beginPath();
    ctx.moveTo(0, y * cellH);
    ctx.lineTo(width, y * cellH);
    ctx.stroke();
  }

  ctx.globalAlpha = 0.78;
  for (let i = 0; i < 210; i += 1) {
    const x = ((i * 37) % columns) * cellW + cellW * 0.5;
    const y = ((i * 53) % rows) * cellH + cellH * 0.5;
    const radius = 2 + ((i * 7) % 13);
    ctx.beginPath();
    ctx.fillStyle = colors[i % colors.length];
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.globalAlpha = 0.42;
  ctx.lineWidth = 1.4;
  for (let i = 0; i < 90; i += 1) {
    const sx = ((i * 17) % columns) * cellW + cellW * 0.5;
    const sy = ((i * 29) % rows) * cellH + cellH * 0.5;
    const ex = (((i * 17) + 8 + (i % 5)) % columns) * cellW + cellW * 0.5;
    const ey = (((i * 29) + 5 + (i % 7)) % rows) * cellH + cellH * 0.5;
    ctx.beginPath();
    ctx.strokeStyle = colors[(i + 1) % colors.length];
    ctx.moveTo(sx, sy);
    ctx.lineTo(ex, ey);
    ctx.stroke();
  }
}

window.addEventListener("resize", drawSignalCanvas);

renderChart("recall");
renderRecommendations("1");
bindControls();
drawSignalCanvas();
