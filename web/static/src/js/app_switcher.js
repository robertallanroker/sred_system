odoo.define('web.AppSwitcher', function (require) {
"use strict";

var core = require('web.core');
var Widget = require('web.Widget');
var Model = require('web.Model');
var QWeb = core.qweb;
var utils = require('web.utils');
var _t = core._t;

var AppSwitcher = Widget.extend({
    template: 'AppSwitcher',
    events: {
        'click .o_action_app': 'on_app_click',
        'click .oe_instance_buy': 'enterprise_buy',
        'click .oe_instance_renew': 'enterprise_renew',
        'click .oe_instance_upsell': 'enterprise_upsell',
        'click a.oe_instance_register_show': function(ev) {$('.oe_instance_register_form').slideToggle();},
        'click #confirm_enterprise_code': 'enterprise_code_submit',
        'click .oe_instance_hide_panel': 'enterprise_hide_panel',
    },
    init: function (parent, menu_data) {
        this._super.apply(this, arguments);
        this.menu_data = menu_data;
    },
    willStart: function() {
        // Force the background image to be in the browser cache before the
        // stylesheet requests it
        var bg_loaded = $.Deferred();
        var bg = new Image();
        bg.onload = function () {
            bg_loaded.resolve();
        };
        bg.src = '/web/static/src/img/application-switcher-bg.jpg';

        return $.when(this._super.apply(this, arguments), bg_loaded);
    },
    start: function () {
        var self = this;
        self.enterprise_expiration_check();
        return this._super.apply(this, arguments);
    },
    /** Checks for the database expiration date and display a warning accordingly. */
    enterprise_expiration_check: function() {
        var self = this;
        if (!self.session) {
            return;
        }
        var P = new Model('ir.config_parameter');
        if (!odoo.db_info) {
            $.when(
                this.session.user_has_group('base.group_user'),
                this.session.user_has_group('base.group_system'),
                P.call('get_param', ['database.expiration_date']),
                P.call('get_param', ['database.enterprise_code']),
                P.call('get_param', ['database.expiration_reason'])
            ).then(function(is_user, is_admin, dbexpiration_date, dbenterprise_code, dbexpiration_reason) {
                // don't show the expiration warning for portal users
                if (!is_user) {
                    return;
                }
                var today = new moment();
                // if no date found, assume 1 month and hope for the best
                dbexpiration_date = new moment(dbexpiration_date || new moment().add(30, 'd'));
                var duration = moment.duration(dbexpiration_date.diff(today));
                var options = {
                    'diffDays': Math.round(duration.asDays()),
                    'dbexpiration_reason': dbexpiration_reason,
                    'warning': is_admin?'admin':(is_user?'user':false),
                    'dbenterprise_code': dbenterprise_code
                };
                self.enterprise_show_panel(options);
            });
        } else {
            $.when(
                P.call('get_param', ['database.enterprise_code'])
            ).then(function(dbenterprise_code) {
                // don't show the expiration warning for portal users
                if (!(odoo.db_info.warning))  {
                    return;
                }
                var today = new moment();
                // if no date found, assume 1 month and hope for the best
                var dbexpiration_date = new moment(odoo.db_info.expiration_date || new moment().add(30, 'd'));
                var duration = moment.duration(dbexpiration_date.diff(today));
                var options = {
                    'diffDays': Math.round(duration.asDays()),
                    'dbexpiration_reason': odoo.db_info.expiration_reason,
                    'warning': odoo.db_info.warning,
                    'dbenterprise_code': dbenterprise_code
                };
                self.enterprise_show_panel(options);
            });
        }
    },
    enterprise_show_panel: function(options) {
        //Show expiration panel 30 days before the expiry
        var self = this;
        var hide_cookie = utils.get_cookie('oe_instance_hide_panel');
        if ((options.diffDays <= 30 && !hide_cookie) || options.diffDays <= 0) {

            var expiration_panel = $(QWeb.render('WebClient.database_expiration_panel', {
                has_mail: _.includes(odoo._modules, 'mail'),
                diffDays: options.diffDays,
                dbenterprise_code:options.dbenterprise_code,
                dbexpiration_reason:options.dbexpiration_reason,
                warning: options.warning
            })).prependTo(self.$('.o_apps'));

            if (options.diffDays <= 0) {
                expiration_panel.children().addClass('alert-danger');
                expiration_panel.find('a.oe_instance_register_show').on('click.widget_events', self.events['click a.oe_instance_register_show']);
                expiration_panel.find('.oe_instance_buy').on('click.widget_events', self.proxy('enterprise_buy'));
                expiration_panel.find('.oe_instance_renew').on('click.widget_events', self.proxy('enterprise_renew'));
                expiration_panel.find('.oe_instance_upsell').on('click.widget_events', self.proxy('enterprise_upsell'));
                expiration_panel.find('#confirm_enterprise_code').on('click.widget_events', self.proxy('enterprise_code_submit'));
                expiration_panel.find('.oe_instance_hide_panel').hide();
                $.blockUI({message: expiration_panel.find('.database_expiration_panel')[0],
                           css: { cursor : 'auto' },
                           overlayCSS: { cursor : 'auto' } });
            }
        }
    },
    enterprise_hide_panel: function(ev) {
        ev.preventDefault();
        utils.set_cookie('oe_instance_hide_panel', true, 24*60*60);
        $('.database_expiration_panel').hide();
    },
    /** Save the registration code then triggers a ping to submit it*/
    enterprise_code_submit: function(ev) {
        ev.preventDefault();
        var enterprise_code = $('.database_expiration_panel').find('#enterprise_code').val();
        if (!enterprise_code) {
            var $c = $('#enterprise_code');
            $c.attr('placeholder', $c.attr('title')); // raise attention to input
            return;
        }
        var P = new Model('ir.config_parameter');
        var Publisher = new Model('publisher_warranty.contract');
        $.when(
            P.call('get_param', ['database.expiration_date']),
            P.call('set_param', ['database.enterprise_code', enterprise_code]))
        .then(function(old_date, enterprise_code) {
            utils.set_cookie('oe_instance_hide_panel', '', -1);
            Publisher.call('update_notification', [[]]).then(function() {
                $.unblockUI();
                $.when(
                    P.call('get_param', ['database.expiration_date']),
                    P.call('get_param', ['database.expiration_reason']))
                .then(function(dbexpiration_date, dbexpiration_reason) {
                    $('.oe_instance_register').hide();
                    $('.database_expiration_panel .alert').removeClass('alert-info alert-warning alert-danger');
                    if (dbexpiration_date != old_date) {
                        $('.oe_instance_hide_panel').show();
                        $('.database_expiration_panel .alert').addClass('alert-success');
                        $('.valid_date').html(moment(dbexpiration_date).format('LL'));
                        $('.oe_instance_success').show();
                    } else {
                        $('.database_expiration_panel .alert').addClass('alert-danger');
                        $('.oe_instance_error, .oe_instance_register_form').show();
                        $('#confirm_enterprise_code').html('Retry');
                    }
                });
            });
        });
    },
    enterprise_buy: function(ev) {
        var limit_date = new moment().subtract(15, 'days').format("YYYY-MM-DD");
        new Model("res.users").call("search_count", [[["share", "=", false],["login_date", ">=", limit_date]]]).then(function(users) {
            window.location = $.param.querystring("https://www.odoo.com/odoo-enterprise/upgrade", {num_users: users});
        });
    },
    enterprise_renew: function(ev) {
        new Model('ir.config_parameter').call('get_param', ['database.enterprise_code']).then(function(contract) {
            var params = contract ? {contract: contract} : {};
            window.location = $.param.querystring("https://www.odoo.com/odoo-enterprise/renew", params);
        });
    },
    enterprise_upsell: function(ev) {
        var limit_date = new moment().subtract(15, 'days').format("YYYY-MM-DD");
        new Model('ir.config_parameter').call('get_param', ['database.enterprise_code']).then(function(contract) {
            new Model("res.users").call("search_count", [[["share", "=", false],["login_date", ">=", limit_date]]]).then(function(users) {
                var params = contract ? {contract: contract, num_users: users} : {num_users: users};
                window.location = $.param.querystring("https://www.odoo.com/odoo-enterprise/upsell", params);
            });
        });
    },
    on_app_click: function (ev) {
        ev.preventDefault();
        this.trigger_up('app_clicked', {
            menu_id: $(ev.currentTarget).data('menu'),
            action_id: $(ev.currentTarget).data('action-id'),
        });
    },
});

return AppSwitcher;

});
