'use strict';

const rq = require('request-promise-native');

module.exports = {
    weather: async function (req, res) {
        const location = req.body.location;

        if (!location) {
            throw new Error('You must provide a location.');
        }
        try {
            const response = await rq(`https://query.yahooapis.com/v1/public/yql?q=select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="${location}") and u="c"&format=json`);
            const condition = JSON.parse(response).query.results.channel.item.condition;
            const text = condition.text;
            const temperature = condition.temp;
            res.end(`It is ${temperature} celsius degrees in ${location} and ${text}`)
        } catch (e) {
            throw e;
        }
    }
}