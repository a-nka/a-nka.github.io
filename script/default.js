const path = "https://a-nka.github.io/data/variables.json";
// Get data from variables.json
fetch(path).then(response => response.json()).then(json => document.title = json.sitename);