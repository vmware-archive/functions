var mongoose = require('mongoose'),
    Task = require('./api/models/todoListModel'), //created model loading here
    bodyParser = require('body-parser');

// mongoose instance connection url connection
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://mongodb.default/Tododb'); 

var controller = require('./api/controllers/todoListController'); //importing route

module.exports = {
    add: function (event, data) { return controller.create_a_task(event, data) },
    delete: function (event, data) { return controller.delete_a_task(event, data) },
    list: function (event, data) { return controller.list_all_tasks(event, data) },
    update: function (event, data) { return controller.update_a_task(event, data) },
}
