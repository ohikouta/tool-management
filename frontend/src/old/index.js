import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

console.log("index.jsが読み込まれました");

const container = document.getElementById("root");
console.log("container: ", container);
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);