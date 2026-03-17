document
  .getElementById("predict-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault(); // mencegah reload halaman

    const g1 = document.getElementById("g1").value;
    const g2 = document.getElementById("g2").value;
    const school = document.getElementById("school").value;
    const reason = document.getElementById("reason").value;
    const higher = document.getElementById("higher").value;
    const internet = document.getElementById("internet").value;
    const romantic = document.getElementById("romantic").value;

    const data = {
      g1: Number(g1),
      g2: Number(g2),
      school: school,
      reason: reason,
      higher: higher,
      internet: internet,
      romantic: romantic,
    };

    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    document.querySelector(".student-grade").innerText = result.prediction;
    document.querySelector(".output").style.display = "flex";
  });
