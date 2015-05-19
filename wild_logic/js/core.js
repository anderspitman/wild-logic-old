var Rx = require('rx');


function Switch() {
  this.state = false;
  this.subject = new Rx.Subject();
}

Switch.prototype.getState = function() {
  return this.state;
};

Switch.prototype.set_state = function(state) {
  this.state = state;
  this.subject.onNext();
};

Switch.prototype.toggle = function() {
  this.state = !this.state;
  this.subject.onNext();
}


function Probe() {
  this.state = false;
}

Probe.prototype.getState = function() {
  return this.state;
}

Probe.prototype.callback = function(data) {
  this.state = true;
}

function connectOutputToInput(output, input) {
  output.subject.subscribe(input.callback.bind(input));
}

module.exports.Switch = Switch;
module.exports.Probe = Probe;
module.exports.connectOutputToInput = connectOutputToInput;


