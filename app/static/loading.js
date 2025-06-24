document.addEventListener("DOMContentLoaded", () => {
    // Handle this in a better way
    if (!window.request_id || !window.ws_url) {
        console.error("Missing requeest_id or ws_url on landing page.");
        return;
    }

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
        alert("Websocket connection error: ", err);
    };

    ws.onclose = () => {
        console.log("WebSocket closed");
    };
});