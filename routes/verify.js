const express = require('express');
const router = express.Router();
var config = undefined;

router.get('/:id', (req, res) => {
    if (req.params.id ==='hi') {
        res.send('Correct!');
    }
    else {
        res.send(`Your id is: ${req.params.id}`);
    }
})

const setConfig = function(cfg) {
    config = cfg;
}

module.exports = {
    router: router,
    setConfig: setConfig
};