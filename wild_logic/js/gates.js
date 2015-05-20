var core = require('./core');
var Rx = require('rx');

function Not() {
  this.state = false;
  this.subject = new Rx.Subject();
}

Not.prototype.callback = function(state) {
  this.state = !state;
  this.subject.onNext(this.state);
}


function And() {
  this.state = false;
  this.inputs = [];
  this.subject = new Rx.Subject();
}

And.prototype.addInput = function(input) {
  this.inputs.push(input);
  var callback = this.callback.bind(this);
  input.subject.subscribe(callback);
  callback(input.state);
}

And.prototype.callback = function(state) {
  this.state = this.evaluate();
  this.subject.onNext(this.state);
}

And.prototype.evaluate = function() {
  var value = true;
  this.inputs.forEach(function(input) {
    if (!input.state) {
      value = false;
    }
  });
  return value;
}


function Or() {
  this.state = false;
  this.inputs = [];
  this.subject = new Rx.Subject();
}

Or.prototype.addInput = function(input) {
  this.inputs.push(input);
  var callback = this.callback.bind(this);
  input.subject.subscribe(callback);
  callback(input.state);
}

Or.prototype.callback = function(state) {
  this.state = this.evaluate();
  this.subject.onNext(this.state);
}

Or.prototype.evaluate = function() {
  var value = false;
  this.inputs.forEach(function(input) {
    if (input.state) {
      value = true;
    }
  });
  return value;
}

module.exports.Not = Not;
module.exports.And = And;
module.exports.Or = Or;
