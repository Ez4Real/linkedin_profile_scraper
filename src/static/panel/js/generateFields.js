document.addEventListener("DOMContentLoaded", function () {
    const csvFileInput = document.getElementById("csvFile");
    const mappingContainer = document.querySelector(".mapping-container");
    const priorityContainer = document.querySelector(".priority-container");


    csvFileInput.addEventListener("change", function () {
        mappingContainer.innerHTML = "";
        priorityContainer.innerHTML = "";

        const file = csvFileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (event) {
            const contents = event.target.result;
            const lines = contents.split("\n");
            const headers = lines[0].split(",");
            const numColumns = headers.length;

            let currentPriority = 1;

            for (let i = 0; i < numColumns; i++) {
                const header = headers[i];
                const mapColumnHTML = document.createElement("div");
                const priorColumnHTML = document.createElement("div");
                mapColumnHTML.className = "mapfield-container";
                priorColumnHTML.className = "mapfield-container";
                const readonlyField = `<p>${header}</p>`;
                mapColumnHTML.innerHTML = `
                    <div class="mapfield-wrapper">
                        <img class="map-icon" src=${imagePaths.chain}></img>
                        ${readonlyField}
                    </div>
                    <select>
                        <option value="" hidden selected>Select an option</option>
                        <option value="website">Website</option>
                        <option value="linkedin">LinkedIn</option>
                        <option value="facebook">Facebook</option>
                        <option value="angelco">Angel.co</option>
                    </select>
                `;
                priorColumnHTML.innerHTML = `
                <div class="mapfield-ineed">
                    ${readonlyField}
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
                mappingContainer.appendChild(mapColumnHTML);
                priorityContainer.appendChild(priorColumnHTML);

                currentPriority++; 
            }
        };
        reader.readAsText(file);
    });
});

function generatePriorityOptions(currentPriority, numColumns) {
    let options = '';
    for (let i = 1; i <= numColumns; i++) {
        options += `<option value="${i}" ${i === currentPriority ? 'selected' : ''}>${i}</option>`;
    }
    return options;
}

