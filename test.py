import os
import json

html = """
<!DOCTYPE html>
<html>
<head>
  <title>Embedding Vega-Lite</title>
  <script src="https://cdn.jsdelivr.net/npm/vega@5.9.2"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-lite@4.0.2"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-embed@6.2.2"></script>
</head>
<body>
  <div id="vis"></div>
</body>
</html>
"""

code = """
const spec = arguments[0];
const done = arguments[1];
done(vegaLite.compile(spec).spec);
"""

vegalite_spec = {
    "data": {
        "values": [
            {"a": "A", "b": 28},
            {"a": "B", "b": 55},
            {"a": "C", "b": 43},
            {"a": "D", "b": 91},
            {"a": "E", "b": 81},
            {"a": "F", "b": 53},
            {"a": "G", "b": 19},
            {"a": "H", "b": 87},
            {"a": "I", "b": 52},
        ]
    },
    "mark": "bar",
    "encoding": {
        "x": {"field": "a", "type": "ordinal"},
        "y": {"field": "b", "type": "quantitative"},
    },
}

html_file = os.path.abspath("index.html")
with open(html_file, "w") as f:
    f.write(html)
url = f"file://{html_file}"

results = {}

for driver_name in ["chrome", "firefox"]:
    if driver_name == "firefox":
        from selenium.webdriver import Firefox as Driver
        from selenium.webdriver.firefox.options import Options
    else:
        from selenium.webdriver import Chrome as Driver
        from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless")
    driver = Driver(options=options)
    try:
        driver.get(url)
        vega_spec = driver.execute_async_script(code, vegalite_spec)
    finally:
        driver.close()

    print("-------------------------------")
    print(f"Full output for {driver_name}")
    print(json.dumps(vega_spec, indent=2))
    results[driver_name] = vega_spec

print("----------------------------")
for driver_name, vega_spec in results.items():
    print(f'{driver_name}: spec.scales[1].range = {vega_spec["scales"][1]["range"]}')
