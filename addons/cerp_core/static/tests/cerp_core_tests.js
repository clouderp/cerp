odoo.define("cerp_core.cerp_core_tests", function(require) {
    "use strict";

    var testUtils = require('web.test_utils');
    var FormView = require('web.FormView');

    /* global QUnit*/

    QUnit.module("cerp_core", {}, function() {
        QUnit.test("Some random test!", async function(assert) {
            assert.expect(1);
	    var form = await testUtils.createView({
		View: FormView,
		model: 'cerp_core.account',
		res_id: 1,
	    });
	    console.log(form);
	    form.destroy();
	})
    })
})
