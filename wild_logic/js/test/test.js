var assert = require("assert");
var core = require("../core");
var gates = require("../gates");

Switch = core.Switch;
Probe = core.Probe;
connectPublisherToSubscriber = core.connectPublisherToSubscriber;

Not = gates.Not;
And = gates.And;
Or = gates.Or;

describe('Core tests', function(){
  
  describe('Test switch class', function() {
    it('Init to false', function() {
      var test_switch = new Switch();
      var probe = new Probe();
      connectPublisherToSubscriber(test_switch, probe);
      assert.equal(probe.getState(), false);
    }),

    it('Set state', function() {
      var probe = new Probe();
      var test_switch = new Switch();
      connectPublisherToSubscriber(test_switch, probe);
      test_switch.setState(true);
      assert.equal(probe.getState(), true);
    })

  }),

  describe('Test probe class', function() {
    it('Initially false', function() {
      var probe = new Probe();
      assert.equal(probe.getState(), false);
    }),

    it("Set to true", function() {
      var probe = new Probe();
      var test_switch = new Switch();
      connectPublisherToSubscriber(test_switch, probe);
      test_switch.setState(true);
      assert.equal(probe.getState(), true);
    }),

    it("Set to true then false", function() {
      var probe = new Probe();
      var test_switch = new Switch();
      connectPublisherToSubscriber(test_switch, probe);
      test_switch.setState(true);
      assert.equal(probe.getState(), true);
      test_switch.setState(false);
      assert.equal(probe.getState(), false);
    })
  }),

  describe('Test connectPublisherToSubscriber', function() {
    it('Propagate values when first connected', function() {
      var testSwitch = new Switch();
      var probe = new Probe();
      testSwitch.setState(true);
      connectPublisherToSubscriber(testSwitch, probe);
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
      connectPublisherToSubscriber(testSwitch, not);
      connectPublisherToSubscriber(not, probe);
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
  }),

  describe('Test AND gate', function() {
    var switches;
    var and;
    var probe;

    beforeEach(function() {
      switches = [ new Switch(), new Switch() ];
      and = new And();
      probe = new Probe();
      switches.forEach(function(sw) {
        and.addInput(sw);
      });
      connectPublisherToSubscriber(and, probe);
    }),

    it('Init to false', function() {
      assert.equal(probe.getState(), false);
    }),

    it("One true still false", function() {
      switches[0].setState(true);
      assert.equal(probe.getState(), false);
    })

    it("All inputs true set gate true", function() {
      switches.forEach(function(sw) {
        sw.setState(true);
      });
      assert.equal(probe.getState(), true);
    }),

    it("Start true setting 1 false changes to false", function() {
      switches.forEach(function(sw) {
        sw.setState(true);
      });
      assert.equal(probe.getState(), true);
      switches[0].setState(false);
      assert.equal(probe.getState(), false);
    }),

    it("3 input AND", function() {
      sw = new Switch();
      switches.push(sw);
      and.addInput(sw);
      switches.forEach(function(sw) {
        sw.setState(false);
      });
      assert.equal(probe.getState(), false);
      switches[0].setState(true);
      assert.equal(probe.getState(), false);
      switches[1].setState(true);
      assert.equal(probe.getState(), false);
      switches[2].setState(true);
      assert.equal(probe.getState(), true);
    }),

    it("Chained ANDs", function() {
      probe = new Probe();
      switches.push(new Switch());
      switches.push(new Switch());
      switches.forEach(function(sw) {
        sw.setState(false);
      });
      and0 = new And();
      and0.addInput(switches[0]);
      and0.addInput(switches[1]);
      and1 = new And();
      and1.addInput(switches[2]);
      and1.addInput(switches[3]);
      and2 = new And();
      and2.addInput(and0);
      and2.addInput(and1);
      connectPublisherToSubscriber(and2, probe);
      assert.equal(probe.getState(), false);
      switches.forEach(function(sw) {
        sw.setState(true);
      });
      assert.equal(probe.getState(), true);
      switches[2].setState(false);
      assert.equal(probe.getState(), false);
    }),

    it("addOutput", function() {
      newProbe = new Probe();
      and.addOutput(newProbe);
      assert.equal(newProbe.getState(), false);
      switches.forEach(function(sw) {
        sw.setState(true);
      });
      assert.equal(newProbe.getState(), true);
      switches[1].setState(false);
      assert.equal(newProbe.getState(), false);
    })



    //it("Adding same input twice fails", function() {
    //  try {
    //    and.addInput(switches[0]);
    //    and.addInput(switches[0]);
    //  }
    //  catch (e) {
    //    return;
    //  }
    //  assert(false);
    //})

  }),

  describe('Test OR gate', function() {
    var switches;
    var or;
    var probe;

    beforeEach(function() {
      switches = [ new Switch(), new Switch() ];
      or = new Or();
      probe = new Probe();
      switches.forEach(function(sw) {
        or.addInput(sw);
      });
      connectPublisherToSubscriber(or, probe);
    }),

    it('Init to false', function() {
      assert.equal(probe.getState(), false);
    }),

    it('One input true evaluates to true', function() {
      switches[0].setState(true);
      assert.equal(probe.getState(), true);
    }),

    it('All inputs true evaluates to true', function() {
      switches.forEach(function(sw) {
        sw.setState(true);
      });
      assert.equal(probe.getState(), true);
    }),

    it('All inputs false evaluates to false', function() {
      switches.forEach(function(sw) {
        sw.setState(false);
      });
      assert.equal(probe.getState(), false);
    }),

    it('Start false then true', function() {
      switches.forEach(function(sw) {
        sw.setState(false);
      });
      assert.equal(probe.getState(), false);
      switches[1].setState(true);
      assert.equal(probe.getState(), true);
    })

  })

})
