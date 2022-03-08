odoo.define("pos_tax_name.models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");

    var _super = models.Order.prototype;
    models.Order = models.Order.extend({
        get_tax_name: function(){
            var details = {};
            var fulldetails = [];

            this.orderlines.each(function(line){
                var ldetails = line.get_tax_details();
                for(var id in ldetails){
                    if(ldetails.hasOwnProperty(id)){
                        details[id] = (details[id] || 0) + ldetails[id];
                    }
                }
            });

            for(var id in details){
                if(details.hasOwnProperty(id)){
                    fulldetails.push({amount: details[id], tax: this.pos.taxes_by_id[id], name: this.pos.taxes_by_id[id].name});
                }
            }

            return fulldetails;
        },

    });

    return models;
});



odoo.define("pos_unit_name.models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");
    var field_utils = require('web.field_utils');
    var utils = require('web.utils');

    var round_di = utils.round_decimals;
    var round_pr = utils.round_precision;

    var _super = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        get_unit_name: function(){
            var unit = this.get_unit();
            if(unit.category_id.name != 'Weight'){
                return "";
            }
            return unit.name;
        },
        get_quant_2_decimals: function(){
            var quant = parseFloat(this.get_quantity_str());
            quant = field_utils.format.float(quant, {digits: [69, 2]});

            return quant;
        },

        get_display_price_one: function(){
            var rounding = this.pos.currency.rounding;
            var price_unit = this.get_unit_price();
            if (this.pos.config.iface_tax_included !== 'total') {
                return round_pr(price_unit * (1.0 - (this.get_discount() / 100.0)), rounding);
            } else {
                var product =  this.get_product();
                var taxes_ids = product.taxes_id;
                var taxes =  this.pos.taxes;
                var product_taxes = [];

                _(taxes_ids).each(function(el){
                    product_taxes.push(_.detect(taxes, function(t){
                        return t.id === el;
                    }));
                });

                var all_taxes = this.pos.compute_all(product_taxes, price_unit, 1, this.pos.currency.rounding);

                return round_pr(all_taxes.total_included * (1 - this.get_discount()/100), rounding);
            }
        },

    });

    return models;
});


