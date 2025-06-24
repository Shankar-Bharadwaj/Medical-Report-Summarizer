document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const file = document.getElementById("pdfFile").files[0];
        if (!file) return alert("Please select a PDF file.");

        const MAX_SIZE_MB = 5;
        const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;
        
        if (file.size > MAX_SIZE_BYTES) {
            return alert(`File too large! Maximum allowed size is ${MAX_SIZE_MB} MB.`);
        }

        // Uniquely identifies the client
        const request_id = crypto.randomUUID();

        // Step 1: Get pre-signed S3 URL
        const res = await fetch(`/get-presigned-url?request_id=${request_id}`);
        const {presigned_url, s3_key} = await res.json();

        // Step 2: Upload to S3
        await fetch(presigned_url, {
            method: "PUT",
            headers: {"Content-Type": "application/pdf"},
            body: file
        })

        // Step 3: Redirect to loading screen (WebSocket handled there)
        window.location.href = `/loading/${request_id}`;
    });
});