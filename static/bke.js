let selectedFiles = [];
let outputFileHandle = null;

function browseInput() {
    document.getElementById("inputFiles").click();
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("inputFiles").addEventListener("change", function () {
        selectedFiles = Array.from(this.files);

        if (selectedFiles.length > 0) {
            document.getElementById("inputPath").value =
                selectedFiles.map(f => f.name).join(", ");
        }
    });
});

async function browseOutput() {
    if (!window.showSaveFilePicker) {
        return;
    }

    try {
        outputFileHandle = await window.showSaveFilePicker({
            suggestedName: "output.xlsx",
            types: [{
                description: "Excel File",
                accept: {
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"]
                }
            }]
        });

        document.getElementById("outputPath").value =
            outputFileHandle.name;
    } catch (e) {
    
    }
}

async function submitConversion() {
    if (selectedFiles.length === 0) {
        alert("Please select input files.");
        return;
    }

    const formData = new FormData();
    selectedFiles.forEach(f => formData.append("input_files", f));

    const response = await fetch("/convert", {
        method: "POST",
        body: formData
    });

    const blob = await response.blob();

    if (outputFileHandle) {
        const writable = await outputFileHandle.createWritable();
        await writable.write(blob);
        await writable.close();
    } else {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "output.xlsx";
        a.click();
    }

    alert(
        "✔ Conversion completed successfully.\n\n" +
        "Your Excel file has been generated.\n\n" +
        "Close this window."
    );
}
