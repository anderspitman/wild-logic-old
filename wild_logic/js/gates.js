var core = require('./core');
var Rx = require('rx');
var _ = require('lodash');

WithOutputsMixin = core.WithOutputsMixin;

function Not() {
  this.outputs = [];
  this.state = false;
  this.subject = new Rx.Subject();
}

_.extend(Not.prototype, WithOutputsMixin);

Not.prototype.callback = function(state) {
  this.state = !state;
  this.subject.onNext(this.state);
};


function Gate() {
  this.inputs = [];
  this.outputs = [];
  this.state = false;
  this.subject = new Rx.Subject();
}

Gate.prototype.addInput = function(input) {
  this.inputs.push(input);
  var callback = this.callback.bind(this);
  input.subject.subscribe(callback);
  callback(input.state);
};

_.extend(Gate.prototype, WithOutputsMixin);

Gate.prototype.callback = function(state) {
  this.state = this.evaluate();
  this.subject.onNext(this.state);
};

Gate.prototype.evaluate = function() {
  throw "Abstract method evaluate not implemented";
};


function And() {
  Gate.call(this);
}

And.prototype = Object.create(Gate.prototype);

And.prototype.constructor = And;

And.prototype.evaluate = function() {
  var value = true;
  this.inputs.forEach(function(input) {
    if (!input.state) {
      value = false;
    }
  });
  return value;
};


function Or() {
  Gate.call(this);
}

Or.prototype = Object.create(Gate.prototype);

Or.prototype.constructor = Or;

Or.prototype.evaluate = function() {
  var value = false;
  this.inputs.forEach(function(input) {
    if (input.state) {
      value = true;
    }
  });
  return value;
};


module.exports.Not = Not;
module.exports.And = And;
module.exports.Or = Or;
