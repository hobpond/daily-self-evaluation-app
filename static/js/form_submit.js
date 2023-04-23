function toJSONString(form) {
    const obj = {};
    const formData = new FormData(form);
    for (const [key, value] of formData) {
        if (key === 'date' && value === '') {
            const today = new Date();
            const dateStr = today.toISOString().slice(0, 10);
            obj[key] = dateStr;
        } else {
            obj[key] = value;
        }
    }
    return JSON.stringify(obj);
}

async function submitEvaluation(event) {
    if (event) {
        event.preventDefault();
    }
    
    const form = document.getElementById("evaluation-form");
    const formData = new FormData(form);

    const data = {};
    for (const [key, value] of formData.entries()) {
        data[key] = value;
    }

    const response = await fetch("/submit_evaluation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    if (response.ok) {
        alert("Evaluation submitted successfully!");
        form.reset();
    } else {
        alert("Error submitting evaluation. Please try again.");
    }
}

document.getElementById("evaluation-form").addEventListener("submit", submitEvaluation);


const inputElements = document.querySelectorAll("input, textarea");
let currentIndex = 0;

inputElements.forEach((element, index) => {
    if (index > 0) {
        element.style.display = "none";
    }

    element.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();

            if (currentIndex < inputElements.length - 1) {
                currentIndex++;
                inputElements[currentIndex].style.display = "block";
                inputElements[currentIndex].focus();
            }
        }
    });
});