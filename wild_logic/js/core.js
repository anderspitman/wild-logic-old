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
}

Switch.prototype.get_state = function() {
  return this.state;
};

Switch.prototype.set_state = function(state) {
  this.state = state;
};


function Probe() {
}

module.exports.Observable = Observable;
module.exports.Switch = Switch;
module.exports.Probe = Probe;


