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

function connectPublisherToSubscriber(publisher, subscriber) {
  var callback = subscriber.callback.bind(subscriber);
  publisher.subject.subscribe(callback);
  // ensure input starts with correct value
  callback(publisher.state);
}

module.exports.Switch = Switch;
module.exports.Probe = Probe;
module.exports.connectPublisherToSubscriber = connectPublisherToSubscriber;


