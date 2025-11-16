
// script.js
const API_BASE = "http://127.0.0.1:8000";

function uploadFile() {
    const fi = document.getElementById('fileInput');
    if (!fi.files || fi.files.length === 0) {
        alert("Select a .py file first");
        return;
    }
    const file = fi.files[0];
    const fd = new FormData();
    fd.append("file", file);

    fetch(API_BASE + "/upload-code/", { method: "POST", body: fd })
    .then(r => r.json())
    .then(data => {
        console.log("upload response", data);
        if (data.status === "success") {
            // render markdown
            const md = data.documentation || "No documentation returned.";
            const html = marked.parse(md);
            document.getElementById("response").innerHTML = html;

            // store latest documentation in window for PDF step
            window.latestDocumentation = md;
            window.latestParsed = data.parsed_structure || {};

            document.getElementById("downloadBtn").style.display = "inline-block";
        } else {
            document.getElementById("response").innerText = "Error: " + (data.message || "Unknown error");
        }
    })
    .catch(err => {
        console.error(err);
        document.getElementById("response").innerText = "Upload failed: " + err;
    });
}

function requestPdf() {
    if (!window.latestDocumentation) {
        alert("No documentation to download. Upload first.");
        return;
    }

    const payload = {
        documentation: window.latestDocumentation,
        parsed_structure: window.latestParsed
    };

    document.getElementById("downloadBtn").innerText = "Preparing PDF...";
    fetch(API_BASE + "/generate-pdf/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(async res => {
        if (!res.ok) {
            const txt = await res.text();
            throw new Error("PDF generation failed: " + txt);
        }
        return res.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "AutoDoc_documentation.pdf";
        a.click();
        document.getElementById("downloadBtn").innerText = "Download PDF";
    })
    .catch(err => {
        console.error(err);
        alert("PDF creation error: " + err.message);
        document.getElementById("downloadBtn").innerText = "Download PDF";
    });
}
// THEME TOGGLE
function toggleTheme() {
    const body = document.body;

    // Toggle class
    body.classList.toggle("dark-theme");

    // Save choice
    const isDark = body.classList.contains("dark-theme");
    localStorage.setItem("theme", isDark ? "dark" : "light");

    // Change button text
    document.getElementById("themeToggle").innerText =
        isDark ? "☀️ Light Mode" : "🌙 Dark Mode";
}

// Load saved theme
window.onload = () => {
    const saved = localStorage.getItem("theme");

    if (saved === "dark") {
        document.body.classList.add("dark-theme");
        document.getElementById("themeToggle").innerText = "☀️ Light Mode";
    }
};


// function uploadFile() {
//     const fileInput = document.getElementById("fileInput");
//     const file = fileInput.files[0];

//     if (!file) {
//         alert("Please select a file!");
//         return;
//     }

//     let formData = new FormData();
//     formData.append("file", file);

//     fetch("http://127.0.0.1:8000/upload-code/", {
//         method: "POST",
//         body: formData,
//     })
//         .then((res) => res.json())
//         .then((data) => {
//             console.log("Backend response:", data);

//             if (data.status === "success") {
//                 // Convert Markdown → HTML
//                 const html = marked.parse(data.documentation);
//                 document.getElementById("response").innerHTML = html;
//             } else {
//                 document.getElementById("response").innerText = "Error generating documentation!";
//             }
//         })
//         .catch((err) => {
//             console.error("Error:", err);
//             document.getElementById("response").innerText = "Upload failed.";
//         });
// }


// function downloadPDF() {
//     const content = document.getElementById("response").innerText;

//     fetch("http://localhost:8000/download-pdf/", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ text: content })
//     })
//     .then(res => res.blob())
//     .then(blob => {
//         const url = window.URL.createObjectURL(blob);
//         const a = document.createElement("a");
//         a.href = url;
//         a.download = "documentation.pdf";
//         a.click();
//     });
// }
