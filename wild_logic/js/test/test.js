var assert = require("assert");
var core = require("../core");
var gates = require("../gates");

Switch = core.Switch;
Probe = core.Probe;
connectOutputToInput = core.connectOutputToInput;

Not = gates.Not;

describe('Core tests', function(){
  
  describe('Test switch class', function() {
    it('Init to false', function() {
      test_switch = new Switch();
      probe = new Probe();
      connectOutputToInput(test_switch, probe);
      assert.equal(probe.getState(), false);
    }),

    it('Set state', function() {
      probe = new Probe();
      test_switch = new Switch();
      connectOutputToInput(test_switch, probe);
      test_switch.setState(true);
      assert.equal(probe.getState(), true);
    })

  }),

  describe('Test probe class', function() {
    it('Initially false', function() {
      probe = new Probe();
      assert.equal(probe.getState(), false);
    }),

    it("Set to true", function() {
      probe = new Probe();
      test_switch = new Switch();
      connectOutputToInput(test_switch, probe);
      test_switch.setState(true);
      assert.equal(probe.getState(), true);
    }),

    it("Set to true then false", function() {
      probe = new Probe();
      test_switch = new Switch();
      connectOutputToInput(test_switch, probe);
      test_switch.setState(true);
      assert.equal(probe.getState(), true);
      test_switch.setState(false);
      assert.equal(probe.getState(), false);
    })
  }),

  describe('Test connectOutputToInput', function() {
    it('Propagate values when first connected', function() {
      testSwitch = new Switch();
      probe = new Probe();
      testSwitch.setState(true);
      connectOutputToInput(testSwitch, probe);
      assert.equal(probe.getState(), true);
    })
  }),

  describe('Test not gate', function() {
    var testSwitch;
    var not;
    var probe;

    beforeEach(function() {
      testSwitch = new Switch();
      not = new Not();
      probe = new Probe();
      connectOutputToInput(testSwitch, not);
      connectOutputToInput(not, probe);
    }),

    it('Init to true', function() {
      assert.equal(probe.getState(), true);
    }),

    it('False to true', function() {
      testSwitch.setState(false);
      assert.equal(probe.getState(), true);
    }),

    it('True to false', function() {
      testSwitch.setState(true);
      assert.equal(probe.getState(), false);
    })
  })

})
