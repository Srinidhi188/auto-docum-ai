function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file first!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    fetch("http://localhost:8000/upload-code/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Backend response:", data);
        document.getElementById("response").innerText = JSON.stringify(data, null, 2);
    })
    .catch(err => {
        console.error("Error:", err);
        document.getElementById("response").innerText = "Upload failed.";
    });
}
