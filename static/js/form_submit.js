function toJSONString(form) {
    const obj = {};
    const formData = new FormData(form);
    for (const [key, value] of formData) {
        obj[key] = value;
    }
    return JSON.stringify(obj);
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("evaluation-form");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const json = toJSONString(form);
        const response = await fetch("/submit-evaluation", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: json,
        });

        if (response.ok) {
            alert("Thank you for submitting your evaluation.");
            form.reset();
        } else {
            alert("An error occurred while submitting the evaluation.");
        }
    });
});