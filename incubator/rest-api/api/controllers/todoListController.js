'use strict';


var mongoose = require('mongoose'),
    Task = mongoose.model('Tasks');

exports.list_all_tasks = function () {
    return new Promise((resolve, reject) => {
        Task.find({}, function (err, task) {
            if (err) {
                reject(err);
            }
            resolve(task);
        });
    })
};

exports.create_a_task = function (event) {
    var new_task = new Task(event.data);
    return new Promise((resolve, reject) => {
        new_task.save(function (err, task) {
            if (err) {
                reject(err);
            }
            resolve(task);
        });
    });
};

exports.update_a_task = function (event) {
    return new Promise((resolve, reject) => {
        Task.findOneAndUpdate({ name: event.data.name }, event.data, { new: true }, function (err, task) {
            if (err) {
                reject(err);
            }
            resolve(task);
        });
    });
};

exports.delete_a_task = function (event) {
    return new Promise((resolve, reject) => {
        Task.remove({
            name: event.data.name
        }, function (err, task) {
            if (err) {
                reject(err);
            }
            resolve({ message: 'Task successfully deleted' });
        });
    });
};
