require('dotenv').config()
var patchCall = require('./helpers')
var rulesHelper = require('./rules')
const fetch = require('node-fetch');

//Fetch header config
let getConfig = {
	"method": "GET",
	"headers": {
		"Content-Type": "application/json",
		"authorization": process.env.API_TOKEN,
		"LD-API-Version": "beta"
	}
}

//URI
const getResults = `https://app.launchdarkly.com/api/v2/flags/${process.env.PROJECT}/${process.env.FLAG}/experiments/${process.env.ENV}/${process.env.METRIC_KEY}`;
const targetFlag = `https://app.launchdarkly.com/api/v2/flags/${process.env.PROJECT}/${process.env.FLAG}?env=${process.env.ENV}`;

//Container Variables for MABs data retrieval
let metadata = []
let totals = []
let flagData = []

module.exports = {
	epsilonBandits: function epsilon(){
			//Fetch our targets' data
	return Promise.all([
				fetch(getResults, getConfig).then(response => response.json()),
				fetch(targetFlag, getConfig).then(response => response.json())
			])
			.then(json => {

			//Assign it to variables
				flagData = json[1]
				metadata = json[0].metadata
				totals = json[0].totals
				let on = flagData.environments[`${process.env.ENV}`].on
				let isExperimentActive = flagData.experiments.items[0].environments

			//Guard Clauses
				if(!on){  return console.error("\x1b[31m","Error: Switch the flag on") }
				if(Array.isArray(isExperimentActive) && isExperimentActive.length === 0) return console.error("\x1b[31m","Error: There is no experiment running.") 

			//Combining the Cumulative Treatment data with the metadata so we have a clear picture of optimal variant and the variants indices.
			let wholeMetadata = metadata.map((item, i) => Object.assign({}, item, totals[i]));
			let completeMetadata = wholeMetadata.map((item, idx) => ({idx, ...item}));

			//Your maximum conversion rate
			let maxConversion = Math.max.apply(Math, completeMetadata.map((variant) => { 
				if (variant.cumulativeConversionRate == null) return 0
				else return variant.cumulativeConversionRate.toFixed(3) * 100;
			}))

			//Output the best performer for 'now'
			let highestPerformer = completeMetadata.find((variant) => { return variant.cumulativeConversionRate.toFixed(3) * 100 == maxConversion })
			return highestPerformer

			})
			.then(bandit => {
			//Where is the Experiment running? Rules OR Fallthrough
				let rules = flagData.environments[`${process.env.ENV}`].rules
				let findExperiment = rulesHelper.rules(rules)
				//console.log(findExperiment)

			//Patch Logic.
				if(findExperiment !== undefined){
					patchCall.runRulesPatch(bandit.idx, findExperiment, bandit.key)
						console.log("Result: ")
						console.log(bandit)
				} else {
					patchCall.runFallthroughPatch(bandit.idx, bandit.key)
						console.log("Result: ")
						console.log(bandit)
				}
			})
			.catch(error => {
				console.warn(error);
			})
	}
}