"""
Build script to generate a self-contained Vercel-ready Stlite index.html
and clean vercel.json configuration.
"""
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

FILES_TO_EMBED = [
    "app.py",
    "core/__init__.py",
    "core/models.py",
    "core/sorting.py",
    "core/knapsack.py",
    "core/graph.py",
    "core/router.py",
    "core/pipeline.py",
    "core/developer_view.py",
    "core/dev_img_data.py",
    "pages/1_Know_About_Developer.py",
    "data/small_dataset.json",
    "data/medium_dataset.json",
    "data/large_dataset.json"
]

embedded_files = {}

for rel_path in FILES_TO_EMBED:
    full_path = os.path.join(PROJECT_ROOT, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            embedded_files[rel_path] = f.read()
    else:
        print(f"Warning: {rel_path} not found")

files_json = json.dumps(embedded_files)

# Generate index.html
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <title>Intelligent Courier Planning System | DAA Capstone</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📦</text></svg>">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/browser@0.83.0/build/stlite.css" />
  <style>
    body {{
      margin: 0;
      padding: 0;
      background-color: #F8F9FA;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    #loading-overlay {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: #FFFFFF;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 9999;
      transition: opacity 0.4s ease;
    }}
    .spinner {{
      width: 44px;
      height: 44px;
      border: 4px solid #E2E8F0;
      border-top-color: #1B365D;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin-bottom: 16px;
    }}
    @keyframes spin {{
      to {{ transform: rotate(360deg); }}
    }}
    .loading-title {{
      font-family: Georgia, serif;
      font-size: 19px;
      font-weight: 700;
      color: #1B365D;
      margin-bottom: 6px;
    }}
    .loading-sub {{
      font-size: 13px;
      color: #718096;
    }}
  </style>
</head>
<body>
  <div id="loading-overlay">
    <div class="spinner"></div>
    <div class="loading-title">Intelligent Courier Planning System</div>
    <div class="loading-sub">Loading Pyodide runtime & DAA Algorithmic Engine...</div>
  </div>
  <div id="root"></div>

  <script type="module">
    import {{ mount }} from "https://cdn.jsdelivr.net/npm/@stlite/browser@0.83.0/build/stlite.js";

    const embeddedFiles = {files_json};

    mount({{
      entrypoint: "app.py",
      requirements: ["pandas", "numpy", "matplotlib"],
      files: embeddedFiles,
      onProgress: (status) => {{
        const sub = document.querySelector('.loading-sub');
        if (sub && status) {{
          sub.innerText = status;
        }}
      }},
      onLoad: () => {{
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {{
          overlay.style.opacity = '0';
          setTimeout(() => overlay.remove(), 400);
        }}
      }}
    }}, document.getElementById("root"));
  </script>
</body>
</html>
"""

with open(os.path.join(PROJECT_ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_template)

# Generate vercel.json
vercel_config = {
    "version": 2,
    "builds": [
        {
            "src": "index.html",
            "use": "@vercel/static"
        },
        {
            "src": "assets/**",
            "use": "@vercel/static"
        }
    ],
    "routes": [
        {
            "src": "/assets/(.*)",
            "dest": "/assets/$1"
        },
        {
            "src": "/(.*)",
            "dest": "/index.html"
        }
    ]
}

with open(os.path.join(PROJECT_ROOT, "vercel.json"), "w", encoding="utf-8") as f:
    json.dump(vercel_config, f, indent=2)

print("Successfully generated index.html and vercel.json")
