
odoo.define('cerp_basic.tour', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;
    tour.register('cerp_basic_tour', {
	url: "/web",
    }, [tour.STEPS.SHOW_APPS_MENU_ITEM, {
        trigger: '.o_app[data-menu-xmlid="cerp_basic.menu_root"]',
        content: _t('Manage costs and usage of cloud accounts? click here.'),
        position: 'right',
    }, {
	trigger: '.o-kanban-button-new',
	content: _t('Let\'s install a cloud provider.'),
	position: 'bottom'
    }]);
});
