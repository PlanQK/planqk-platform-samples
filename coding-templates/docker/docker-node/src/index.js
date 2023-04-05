const fs = require('fs');

function readJSONFile(filepath, defaultValue = null) {
    try {
        fs.accessSync(filepath);
        return JSON.parse(fs.readFileSync(filepath));
    } catch {
        return defaultValue;
    }
}

// Read the input files
const inputData = readJSONFile('/var/input/data.json') || readJSONFile('./input/data.json');
const inputParams = readJSONFile('/var/input/params.json') || readJSONFile('./input/params.json', {round_up: false});

if (!inputData) {
    console.error('Error: data.json file not found');
    process.exit(1);
}

// Sum the values in the "values" property
const sum = inputData.values.reduce((acc, val) => acc + val, 0);

// Round up the sum if "round_up" is true
const result = {
    sum: inputParams.round_up ? Math.ceil(sum) : sum
};

// Return the result as a JSON object
console.log("PlanQK:Job:Result:", JSON.stringify(result));
