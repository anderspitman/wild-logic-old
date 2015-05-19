var assert = require("assert")
var core = require("../core")

Observable = core.Observable;
Switch = core.Switch;
Probe = core.Probe;
connectOutputToInput = core.connectOutputToInput;

describe('Core tests', function(){
  
  describe('Observable', function() {
    it('Callback', function() {
      var observable = new Observable();
      assert.equal(false, observable.get_state());
      observable.set_state(true);
      assert.equal(true, observable.get_state());
      var called1 = false;
      var called2 = false;
      observable.add_listener(function() {
        called1 = true;
      });
      observable.add_listener(function() {
        called2 = true;
      });
      observable.set_state(false);
      assert.equal(true, called1);
      assert.equal(true, called2);
    })
  }),

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
