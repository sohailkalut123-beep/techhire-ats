const resumeInput = document.getElementById("resumeUpload");
const fileList = document.getElementById("fileList");

if (resumeInput) {
    resumeInput.addEventListener("change", function () {

        fileList.innerHTML = "";

        for (let i = 0; i < resumeInput.files.length; i++) {

            const fileItem = document.createElement("div");

            const fileName = document.createElement("p");
            fileName.textContent = resumeInput.files[i].name;

            const removeBtn = document.createElement("button");
            removeBtn.textContent = "x";

            removeBtn.addEventListener("click", function () {

                const dt = new DataTransfer();

                for (let j = 0; j < resumeInput.files.length; j++) {
                    if (j !== i) {
                        dt.items.add(resumeInput.files[j]);
                    }
                }

                resumeInput.files = dt.files;
                fileItem.remove();
            });

            fileItem.appendChild(fileName);
            fileItem.appendChild(removeBtn);
            fileList.appendChild(fileItem);
        }
    });
}

const analyzeBtn = document.getElementById("analyzeBtn");
const statusMessage = document.getElementById("statusMessage");

if (analyzeBtn && statusMessage) {
    analyzeBtn.addEventListener("click", function () {
        statusMessage.textContent = "Analysing Candidates...";
    });
}

const degreeFilter = document.getElementById("degreeFilter");
const rows = document.querySelectorAll(".candidate-row");
const searchInput = document.getElementById("searchInput");

if (searchInput) {
    searchInput.addEventListener("keyup", function () {

        const searchText = searchInput.value.toLowerCase();

        rows.forEach(function (row) {

            const nameText = row.children[0].innerText.toLowerCase();

            if (nameText.includes(searchText)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
}

if (degreeFilter) {
    degreeFilter.addEventListener("change", function () {

        const selectedDegree = degreeFilter.value;

        rows.forEach(function (row) {

            const degreeText = row.children[3].innerText.trim();

            if (selectedDegree === "All") {
                row.style.display = "";
            } else if (
                degreeText.toLowerCase().includes(
                    selectedDegree.toLowerCase()
                )
            ) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
}

const statusFilter = document.getElementById("statusFilter");

if (statusFilter) {
    statusFilter.addEventListener("change", function () {

        const selectedStatus = statusFilter.value;

        rows.forEach(function (row) {

            const statusText = row.children[8].innerText.trim();

            if (selectedStatus === "All") {
                row.style.display = "";
            } else if (
                statusText.toLowerCase() ===
                selectedStatus.toLowerCase()
            ) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
}