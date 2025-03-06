document.getElementById("manual-path-form").addEventListener("submit", function(event) {
    event.preventDefault();

    let manualPath = document.getElementById("manual-path").value;

    fetch("/set-storage-path", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path: manualPath })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("current-path").innerText = data.new_path;
            alert("Storage path updated successfully!");
            location.reload();
        } else {
            alert("Invalid path.");
        }
    });
});