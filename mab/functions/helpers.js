require('dotenv').config()
const fetch = require('node-fetch');

module.exports = {
	runFallthroughPatch: function runFallThroughPatch(index, treatmentName){
		const target = `https://app.launchdarkly.com/api/v2/flags/${process.env.PROJECT}/${process.env.FLAG}`;
		let patchConfig = {
			"method": "PATCH",
			"headers": {
				"Content-Type": "application/json",
				"authorization": process.env.API_TOKEN,
				"LD-API-Version": "beta"
			},
			"body": JSON.stringify({
				"comment": `This is an Automated MABs allocation. Treatment: ${treatmentName} assigned.`,
				"patch": [{ 
					"op": "replace",
					"path": `/environments/${process.env.ENV}/fallthrough/rollout/experimentAllocation/defaultVariation`,
					"value": index
				}]
			})
		}
		fetch(target, patchConfig)
		.then(response => {response.status === 200 ? console.log("\x1b[32m","FT: Fine.") : console.log("\x1b[31m",`FT: We have a ${response.status}`)})
		.catch((error) => {console.log(error)})
	
	},
	runRulesPatch: function runRulesPatch(index, findExperiment, treatmentName){
		const target = `https://app.launchdarkly.com/api/v2/flags/${process.env.PROJECT}/${process.env.FLAG}`;
		let config = {
			"method": "PATCH",
			"headers": {
				"Content-Type": "application/json",
				"authorization": process.env.API_TOKEN,
				"LD-API-Version": "beta"
			},
			"body": JSON.stringify({
				"comment": `This is an Automated MABs allocation. Treatment: ${treatmentName} assigned.`,
				"patch": [{ 
						"op": "replace",
						"path": `/environments/${process.env.ENV}/rules/`+findExperiment+"/rollout/experimentAllocation/defaultVariation",
						"value": index
					}]
			})
		}
		fetch(target, config)
		.then(response => {response.status === 200 ? console.log("\x1b[32m","R: Fine.") : console.error("\x1b[31m",`R: We have a ${response.status}`)})
		.catch((error) => {console.log(error)})
	}
}