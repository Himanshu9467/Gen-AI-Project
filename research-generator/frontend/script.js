const theme = localStorage.getItem("theme");

fetch("http://127.0.0.1:5000/generate-titles", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ theme })
})
.then(res => res.json())
.then(data => {
  const dropdown = document.getElementById("titleDropdown");
  data.titles.forEach(title => {
    const option = document.createElement("option");
    option.text = title;
    dropdown.add(option);
  });
})
.catch(err => alert("Backend not reachable"));

function generateAbstract() {
  document.getElementById("loader").style.display = "block";

  fetch("http://127.0.0.1:5000/generate-abstract", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: document.getElementById("titleDropdown").value
    })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("loader").style.display = "none";

    if (!data.abstract) {
      alert("Abstract generation failed");
      return;
    }

    document.getElementById("abstractText").innerText = data.abstract;
    document.getElementById("humanText").innerText = data.comparison.human;
    document.getElementById("llmText").innerText = data.comparison.llm;
  })
  .catch(err => {
    document.getElementById("loader").style.display = "none";
    alert("Flask or LLaMA not running");
  });
}
