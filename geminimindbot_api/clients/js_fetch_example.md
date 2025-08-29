# JavaScript (Node) streaming example with fetch

```js
import fetch from "node-fetch";

const API_URL = "http://localhost:8000/chat/stream";
const API_KEY = "change-me";

async function streamChat(message) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
    body: JSON.stringify({ message, history: [] }),
  });

  if (!res.ok) {
    console.error("HTTP", res.status, await res.text());
    return;
  }

  for await (const chunk of res.body) {
    process.stdout.write(chunk.toString());
  }
}

streamChat("Hello from Node streaming!");
```

> ملاحظة: لو عايز SSE حقيقي (EventSource) مع هيدر مخصص، استخدم Proxy صغير أو WebSocket.
