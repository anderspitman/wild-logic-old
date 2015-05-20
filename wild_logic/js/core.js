var Rx = require('rx');
var _ = require('lodash');

var WithOutputsMixin = {
  addOutput: function(output) {
    this.outputs.push(output);
    var callback = output.callback.bind(output);
    this.subject.subscribe(callback);
    callback(this.state);
  }
};


function Switch() {
  this.outputs = [];
  this.state = false;
  this.subject = new Rx.Subject();
}

Switch.prototype.setState = function(state) {
  this.state = state;
  this.subject.onNext(this.state);
}

_.extend(Switch.prototype, WithOutputsMixin);


function Probe() {
  this.state = false;
}

Probe.prototype.getState = function() {
  return this.state;
}

Probe.prototype.callback = function(state) {
  this.state = state;
}

module.exports.Switch = Switch;
module.exports.Probe = Probe;
module.exports.WithOutputsMixin = WithOutputsMixin;
