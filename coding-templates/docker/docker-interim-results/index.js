const fs = require('fs');

function readJSONFile(filepath, defaultValue = null) {
  try {
    fs.accessSync(filepath);
    return JSON.parse(fs.readFileSync(filepath));
  } catch {
    return defaultValue;
  }
}

function delay(time) {
  return new Promise(resolve => setTimeout(resolve, time));
}

async function run() {
  // Read the input files
  console.info('Reading input files...');
  const inputData = readJSONFile('/var/input/data.json') || readJSONFile('./input/data.json');
  const inputParams = readJSONFile('/var/input/params.json') || readJSONFile('./input/params.json', { round_up: false });

  if (!inputData) {
    console.error('Error: data.json file not found');
    process.exit(1);
  }
  console.debug('Input data:', inputData);
  console.debug('Input params:', inputParams);

  await delay(1000)

  console.info('Calculating sum...');

  // Sum the values in the "values" property
  const sum = await inputData.values.reduce(async (acc, val) => {
    const s = await acc + val;
    console.info('PlanQK:Job:InterimResult:', JSON.stringify({ sum: s }))
    await delay(5000)
    return s;
  }, 0);

  console.info('Calculation finished:', sum);

  // Round up the sum if "round_up" is true
  console.debug('Rounding up?', inputParams.round_up)
  const result = {
    sum: inputParams.round_up ? Math.ceil(sum) : sum
  };

  await delay(10000)

  // Return the result as a JSON object
  console.info('PlanQK:Job:Result:', JSON.stringify(result));

  console.log('Done!')
}

run();
