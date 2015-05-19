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

module.exports.Not = Not;
