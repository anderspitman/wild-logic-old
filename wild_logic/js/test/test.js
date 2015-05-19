var assert = require("assert")
var core = require("../core")

Switch = core.Switch;
Probe = core.Probe;
connectOutputToInput = core.connectOutputToInput;

describe('Core tests', function(){
  
  describe('Test switch class', function() {
    it('Basic functionality', function() {
      test_switch = new Switch();
      assert.equal(false, test_switch.getState());
      test_switch.toggle();
      assert.equal(true, test_switch.getState());
    }),

    it('Listeners', function() {
      probe = new Probe();
      test_switch = new Switch();
      connectOutputToInput(test_switch, probe);
      assert.equal(probe.getState(), false);
      test_switch.toggle();
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
