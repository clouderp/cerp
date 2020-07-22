odoo.define('cerp_core.tree', function (require) {
    "use strict";
    var ListView = require('web.ListView');
    var ListController = require('web.ListController');
    var viewRegistry = require('web.view_registry');

    var CloudERPListController = ListController.extend({
        buttons_template: 'CloudERPListView.buttons',
    });

    var CloudERPListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: CloudERPListController,
        }),
    });

    viewRegistry.add('cerp_core_tree', CloudERPListView);
});
