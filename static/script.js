document.addEventListener("DOMContentLoaded", function () {
    const storagePathDisplay = document.getElementById("storage-path");
    const changePathButton = document.getElementById("change-path");

    changePathButton.addEventListener("click", function () {
        fetch('/choose-directory', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                storagePathDisplay.textContent = data.new_path;
                alert("Storage path updated successfully!");
                location.reload();  // Reload to reflect changes
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});