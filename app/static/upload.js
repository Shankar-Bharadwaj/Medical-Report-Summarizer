document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    const dropArea = document.getElementById("drop-area");
    const fileInput = document.getElementById("pdfFile");

    // Drag-and-drop styling + behavior
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, e => {
            e.preventDefault();
            e.stopPropagation();
            dropArea.classList.add("highlight");
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, e => {
            e.preventDefault();
            e.stopPropagation();
            dropArea.classList.remove("highlight");
        });
    });

    // Handle dropped file
    dropArea.addEventListener("drop", e => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files; // Assign dropped file to input
        }
    });

    // Handle submit
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const file = fileInput.files[0];
        if (!file) return alert("Please select a PDF file.");

        const MAX_SIZE_MB = 5;
        const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;
        
        if (file.size > MAX_SIZE_BYTES) {
            return alert(`File too large! Maximum allowed size is ${MAX_SIZE_MB} MB.`);
        }

        try {
            // Step 1: Get presigned URL
            const res = await fetch(`/get-presigned-url`);
            const { request_id, presigned_url, s3_key } = await res.json();

            // Update the DOM to show loading screen
            document.getElementById("uploadForm").style.display = "none";
            document.getElementById("loading-screen").style.display = "block";

            // Step 2: Upload to S3
            await fetch(presigned_url, {
                method: "PUT",
                headers: { "Content-Type": "application/pdf" },
                body: file
            }).catch(err => {
                console.log("Background upload failed:", err);
            });


            // // Step 3: Get the WS_URL
            // window.location.href = `/result/${request_id}`;
            const ws_res = await fetch(`loading/${request_id}`, { method: "POST" });
            const { ws_url } = await ws_res.json();


            const ws = new WebSocket(ws_url);
            ws.onopen = () => {
                ws.send(JSON.stringify({ action: "register", request_id}));
                console.log("Registered request_id:", request_id);
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log("Received message: ", data);

                if (data.status==="completed" && data.request_id===request_id){
                    console.log("Processing complete, redirecting to result...:", data);
                    ws.close();
                    window.location.href = `/result/${request_id}`;
                }
            };

            // Change how you handle this error (Do not send alerts)
            ws.onerror = (err) => {
                console.log("WebSocket connection error:", err);
                alert("WebSocket connection error. Please try again.");
            };

            ws.onclose = () => {
                console.log("WebSocket closed");
            };

        } catch (err) {
            console.log("Upload error:", err);
            alert("Something went wrong during upload. Please try again.");
            document.getElementById("uploadForm").style.display = "block";
            document.getElementById("loading-screen").style.display = "none";
        }
    });
});
