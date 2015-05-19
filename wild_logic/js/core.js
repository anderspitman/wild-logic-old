var Rx = require('rx');


function Switch() {
  this.state = false;
  this.subject = new Rx.Subject();
}

Switch.prototype.setState = function(state) {
  this.state = state;
  this.subject.onNext(this.state);
}


function Probe() {
  this.state = false;
}

Probe.prototype.getState = function() {
  return this.state;
}

Probe.prototype.callback = function(state) {
  this.state = state;
}

function connectOutputToInput(output, input) {
  output.subject.subscribe(input.callback.bind(input));
}

module.exports.Switch = Switch;
module.exports.Probe = Probe;
module.exports.connectOutputToInput = connectOutputToInput;


