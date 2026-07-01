const babel = require("@babel/core");
const fs = require("fs");
const src = fs.readFileSync("build/app_src.jsx", "utf8");
const out = babel.transformSync(src, {
  presets: [["@babel/preset-react", { runtime: "classic" }]],
  compact: false,
}).code;
fs.writeFileSync("build/app.js", out);
console.log("app.js:", out.length, "chars");
console.log("¿contiene import/export?:", /\b(import|export)\b/.test(out) ? "SÍ (mal)" : "no (bien)");
