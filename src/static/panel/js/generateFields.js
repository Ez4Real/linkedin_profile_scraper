const formData = {
    file: null,
    allOptionsSelected: false
};

document.addEventListener("DOMContentLoaded", function () {
    const csvFileInput = document.getElementById("csvFile");
    const mappingContainer = document.querySelector(".mapping-container");
    const priorityContainer = document.querySelector(".priority-container");
    const nextButton = document.getElementById("next-button");
    const submitButton = document.getElementById("submit-button");

    csvFileInput.addEventListener("change", function () {
        mappingContainer.innerHTML = "";
        priorityContainer.innerHTML = "";

        formData.file = csvFileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (event) {
            const contents = event.target.result.split("\n");
            const headers = contents[0].split(",");
            const numColumns = headers.length;

            let currentPriority = 1;

            for (let i = 0; i < numColumns; i++) {
                const header = headers[i];
                const mapFieldHTML = document.createElement("div");
                const priorFieldHTML = document.createElement("div");
                mapFieldHTML.className = "mapfield-container";
                priorFieldHTML.className = "mapfield-container";
                const columnNameHTML = `<p>${header}</p>`;
                mapFieldHTML.innerHTML = `
                    <div class="mapfield-wrapper">
                        <img class="map-icon" src=${imagePaths.chain}></img>
                        ${columnNameHTML}
                    </div>
                    <select>
                        <option value="" hidden selected>Select an option</option>
                        <option value="website">Website</option>
                        <option value="linkedin">LinkedIn</option>
                        <option value="facebook">Facebook</option>
                        <option value="angelco">Angel.co</option>
                    </select>
                `;
                priorFieldHTML.innerHTML = `
                    <div class="mapfield-ineed">
                        ${columnNameHTML}
                        <div class="mapfield-ineed__controller">
                            <p>Priority:</p>
                            <select data-priority=${currentPriority}>
                                ${generatePriorityOptions(currentPriority, numColumns)}
                            </select>
                        </div>
                    </div>
                    <div class="needer">
                        <p>Need Scraping:</p>
                        <input type="checkbox" checked>
                    </div>
                `;

                const mapSelect = mapFieldHTML.querySelector("select");
                mapSelect.addEventListener("change", () => {
                    formData.allOptionsSelected = Array.from(
                        mappingContainer.querySelectorAll("select")
                    ).every(select => select.value !== "");
                    nextButton.style.display = formData.allOptionsSelected ? "block" : "none";
                });

                const priorSelect = priorFieldHTML.querySelector("select");
                priorSelect.addEventListener("change", () => {
                    const selectsValues = Array.from(
                        priorityContainer.querySelectorAll("select")
                    ).map(select => select.value);
                    const hasDuplicates = selectsValues.length !== new Set(selectsValues).size;
                    submitButton.style.display = hasDuplicates ? "none" : "block"
                })

                mappingContainer.appendChild(mapFieldHTML);
                priorityContainer.appendChild(priorFieldHTML);

                currentPriority++; 
            }
            nextButton.style.display = formData.file ? "block" : "none";
        };
        reader.readAsText(formData.file);
    });

    
});

function generatePriorityOptions(currentPriority, numColumns) {
    let options = '';
    for (let i = 1; i <= numColumns; i++) {
        options += `<option value=${i} ${i === currentPriority ? 'selected' : ''}>${i}</option>`;
    }
    return options;
}

