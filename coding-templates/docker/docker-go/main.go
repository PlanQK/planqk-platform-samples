package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
)

type InputData struct {
	Values []float64 `json:"values"`
}

type InputParams struct {
	RoundUp bool `json:"round_up"`
}

type Result struct {
	Sum float64 `json:"sum"`
}

func readInputData(defaultValue InputData) InputData {
    var inputData InputData
    data, err := ioutil.ReadFile("/var/input/data.json")
     if err != nil {
        fmt.Println("Error reading input data:", err)
        return defaultValue
    }
    if err := json.Unmarshal(data, &inputData); err != nil {
        fmt.Println("Error unmarshalling input data:", err)
        return defaultValue
    }
    return inputData
}

func readInputParams(defaultValue InputParams) InputParams {
    var inputParams InputParams
    data, err := ioutil.ReadFile("/var/input/params.json")
    if err != nil {
        fmt.Println("Error reading input params:", err)
        return defaultValue
    }
    if err := json.Unmarshal(data, &inputParams); err != nil {
        fmt.Println("Error unmarshalling input params:", err)
        return defaultValue
    }
    return inputParams
}

func toJson(result Result) string {
	jsonBytes, err := json.Marshal(result)
	if err != nil {
		return "{ \"error\": \"Error converting result to JSON\" }"
	}
	return string(jsonBytes)
}

func main() {
	// Read the input files
	inputData := readInputData(InputData{Values: []float64{1, 2, 3, 4, 5}})
	inputParams := readInputParams(InputParams{RoundUp: false})

	// Sum the values in the "values" property
    sum := 0.0
    for _, value := range inputData.Values {
        sum += value
    }

	// Round up the sum if "round_up" is true
	result := Result{Sum: float64(sum)}
	if inputParams.RoundUp {
		result.Sum = math.Ceil(sum)
	}

	// Return the result as a JSON object
	fmt.Println("PlanQK:Job:Result:", toJson(result))
}
