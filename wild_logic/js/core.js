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
};

_.extend(Switch.prototype, WithOutputsMixin);


function Probe() {
  this.state = false;
}

Probe.prototype.getState = function() {
  return this.state;
};

Probe.prototype.callback = function(state) {
  this.state = state;
};

function verifyGateFromTruthTable(gateClass, truthTable) {
  var numColumns = truthTable[0][0].length;
  var switches = [];
  var gate = new gateClass();
  var probe = new Probe();
  for (var i=0; i<numColumns; i++) {
    var sw = new Switch();
    switches.push(sw);
    sw.addOutput(gate);
  }
  gate.addOutput(probe);
  for (var row of truthTable) {
    for (var j=0; j<numColumns; j++) {
      switches[j].setState(row[0][j]);
    }
    if (probe.getState() != row[1]) {
      return false;
    }
  }
  return true;
}

module.exports.Switch = Switch;
module.exports.Probe = Probe;
module.exports.WithOutputsMixin = WithOutputsMixin;
module.exports.verifyGateFromTruthTable = verifyGateFromTruthTable;
