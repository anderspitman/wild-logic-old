var assert = require("assert")
var core = require("../core")

Switch = core.Switch;
Probe = core.Probe;
connectOutputToInput = core.connectOutputToInput;

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
      assert.equal(false, probe.getState());
    })
  })

})
