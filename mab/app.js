//Package imports
require('dotenv').config()
const express = require('express')
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const LaunchDarkly = require('launchdarkly-node-server-sdk');
var app = express();
const port = process.env.PORT || 8080
var mabs = require('./functions/mabs')

// User Context for Experiment.
var context = {
	key: uuidv4(),
	country: "UK",
	city: "London",
	ip: "127.0.0.1",
	privateAttributeNames: ["ip", "LTV"],
	custom: {
	  groups: ["Beta", "Internal", "High Volume"],
	  loyaltyMember: false,
	  requestTime: Math.round(new Date().getTime() / 1000),
	  LTV: "Z142456",
	  platformBrand: "Samsung",
	  platform: "Roku",
	  version: "4.3.8"
	}
  }

//console.log(context.key)

//LD Flag Logic and experiment 'stuff - this is so I had an active experiment to work with.
const ldClient = LaunchDarkly.init(process.env.SDK_KEY);
ldClient.once('ready', () => {
ldClient.variation(process.env.FLAG, context, ", something is wrong?!?", 
	(err, feature) => {
			app.set('view engine', 'pug');
			app.set('views', path.join(__dirname, `views`));
			app.get('/', (req, res) => {
				console.log(feature)
				res.render('index', {
					feature: feature,
					context: JSON.stringify(context)
				});
			})
			app.listen(port, () => {
				console.log(`${feature} is available on port ${port}!`)
			})
		ldClient.flush()
		})
	})

mabs.epsilonBandits();

ldClient.close();