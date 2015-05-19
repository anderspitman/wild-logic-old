var Rx = require('rx');

function Observable() {
  this.state = false;
  this.listeners = [];
}

Observable.prototype.get_state = function() {
  return this.state;
};

Observable.prototype.set_state = function(state) {
  this.state = state;
  this.notify_listeners();
};

Observable.prototype.add_listener = function(listener) {
  this.listeners.push(listener);
};

Observable.prototype.notify_listeners = function() {
  this.listeners.forEach(function(listener) {
    listener();
  });
};


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

module.exports.Observable = Observable;
module.exports.Switch = Switch;
module.exports.Probe = Probe;
module.exports.connectOutputToInput = connectOutputToInput;


