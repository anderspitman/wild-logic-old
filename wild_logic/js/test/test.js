var assert = require("assert")
var core = require("../core")

Observable = core.Observable;
Switch = core.Switch;
Probe = core.Probe;

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

  describe('Instantiate switch object', function() {
    it('Should exist', function() {
    })
  })

})
