document.addEventListener("DOMContentLoaded", function () {
    const csvFileInput = document.getElementById("csvFile");
    const mappingContainer = document.querySelector(".mapping-container");
    const priorityContainer = document.querySelector(".priorFieldContainer");

    // Show or hide Next button based on CSV upload
    csvFileInput.addEventListener("change", function () {
        // Get headers from the uploaded CSV
        const file = csvFileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (event) {
            const contents = event.target.result;
            const lines = contents.split("\n");
            const headers = lines[0].split(",");
            const numColumns = headers.length;

            let currentPriority = 1; // Initialize priority value

            // Draw HTML for each column header
            for (let i = 0; i < numColumns; i++) {
                const header = headers[i];
                const mapColumnHTML = document.createElement("div");
                const priorColumnHTML = document.createElement("div");
                mapColumnHTML.className = "mapfield-container";
                priorColumnHTML.className = "mapfield-container";
                const readonlyField = `<input type="text" value=${header} readonly>`
                mapColumnHTML.innerHTML = `
                    <img class="map-icon" src=${imagePaths.chain}></img>
                    ${readonlyField}
                    <select>
                        <option value="" hidden selected>Select an option</option>
                        <option value="website">Website</option>
                        <option value="linkedin">LinkedIn</option>
                        <option value="facebook">Facebook</option>
                        <option value="angelco">Angel.co</option>
                    </select>
                `;
                priorColumnHTML.innerHTML = `
                    ${readonlyField}
                    <select>
                        ${generatePriorityOptions(currentPriority, numColumns)}
                    </select>
                    <p>Need Scraping</p>
                    <input type="checkbox" checked>
                `;

                mappingContainer.appendChild(mapColumnHTML);
                priorityContainer.appendChild(priorColumnHTML);

                currentPriority++;
            }
        };
        reader.readAsText(file);
    });
});

// Function to generate priority options dynamically
function generatePriorityOptions(currentPriority, numColumns) {
    let options = '';
    for (let i = 1; i <= numColumns; i++) {
        options += `<option value="${i}" ${i === currentPriority ? 'selected' : ''}>${i}</option>`;
    }
    return options;
}