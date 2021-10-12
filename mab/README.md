## Epsilon Greedy - Multi-Arm Bandits.

In the world of hypothesis testing there are many kinds of Bandits algorithms. The code in this repo demonstrates how you can run an **Epsilon Greedy** version of a Bandit with LaunchDarkly's experimentation product.

### Brief Synopsis

Bandits algorithms are used as a means to exploit particular situations where you don't want to wait for your experiments to complete before you can capitalise on their value. The idea is to focus on manipulating a specific variable in order to gain more of a specific outcome. 

Some good examples might be: 

* eCommerce offers that have a very small window of promotion.
* Experimentation on sites with very little traffic.
* Optimising for the best performing data stream.

> **NOTE**: Statistical concepts such as 'Significance' are less relevant with this style of bandit as we are looking to capitalise on an outcome in as near-term as possible.

### OK, so what are we actually doing?

In this instance we would we looking to do the following: 

1. Portion off a small subset of our audience (_whatever that audience may look like_) to experiment on. 
2. We divide that into our variations/treatments as we would do with any other experiment.
3. Assign our metrics, noting our Primary metric of focus. This is very important as this primary metric will be our barometer for changes.

For now, lets say we have an experiment comprised of three variations and each variation has 5% of our audience assigned too it.

- 85% of our total audience remains unexposed to our experiment. At this time they will be exposed to the same experience as our control group.

- 15% of our total audience is participating in our experiment.  
-- 5% to our **Control**.   
-- 5% to our **B Variation**.   
-- 5% to our **C Variation**.   

With this now setup our Bandit will periodically check-in on the conversion metric you defined.  

On every check-in the variation with the best performance at that point will be appointed the variation to be shown to "Everyone outside of the experiment".

-- 85% to **Everyone Else** [sees the **Control**].   
-- 5% to our **Control**.   
-- 5% to our **B Variation**.   
-- 5% to our **C Variation**.   

Check-in after an hour|day|week and the **B Variation** is performing best.

-- 85% to **Everyone Else** [sees the **B Variation**].   
-- 5% to our **Control**.   
-- 5% to our **B Variation**.   
-- 5% to our **C Variation**.   

...and then repeat at the same duration ad infinitum.

### How do I get setup?

```
$ git clone git@github.com:sih3rron/greedybandits.git
$ npm install

```

The repo uses `dotenv` for environment variables. 

The variables required are:

```
SDK_KEY= <<Your LaunchDarkly NODEJS Serverside SDK Key.>>
CLIENT_SDK_KEY= <<Your LaunchDarkly JS Client-side SDK Key.>>
API_TOKEN=  <<A LaunchDarkly API Key>>
FLAG=  <<The Flag Key for the Feature you are experimenting on.>> 
PROJECT=  <<The Project Key.>> 
ENV=   <<The Environment Key.>> 
METRIC_KEY= <<The Metric Key for your Primary Measure of Success.>>  
PORT= <<The localhost port you are running this demo on.>>  
```

After you have applied all of the Environment variables, you will need to setup and start your Experiment Recording data. 

To start your server use `$ node app`.



# Points to note.

* This script is only setup to look at Rate (%) metrics. Nothing has been built for Numerate measures.
* Likewise, nothing has been built to acknowledge whether success is More or Fewer than the baseline. It looks solely at which rate is the highest.