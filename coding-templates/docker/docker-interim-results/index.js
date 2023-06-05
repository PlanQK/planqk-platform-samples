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
  console.time("run");

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
  console.info('PlanQK:Job:InterimResult:', JSON.stringify({ sum: 0 }))

  // Sum the values in the "values" property
  const sum = await inputData.values.reduce(async (acc, val) => {
    const s = await acc + val;
    await delay(10000)
    console.info('PlanQK:Job:InterimResult:', JSON.stringify({ sum: s }))
    return s;
  }, 0);

  console.info('Calculation finished:', sum);

  await delay(10000)

  // Round up the sum if "round_up" is true
  console.debug('Rounding up?', inputParams.round_up)
  const result = {
    sum: inputParams.round_up ? Math.ceil(sum) : sum
  };

  // Return the result as a JSON object
  console.info('PlanQK:Job:MultilineResult');
  console.info(JSON.stringify(result, null, 2));
  console.info('PlanQK:Job:MultilineResult')

  console.log('Done!')
  console.timeEnd("run");
}

run();
