odoo.define('document_format_zoopet.models', function (require) {
    "use strict";

    // Primero importamos los módulos básicos del POS
    var models = require('point_of_sale.models');

    // Verificamos si existe el módulo l10n_es_pos
    var es_pos_models;
    try {
        es_pos_models = require('l10n_es_pos.models');
    } catch (e) {
        // Si no existe, seguimos con la implementación normal
        console.log('l10n_es_pos no encontrado, usando modelos base del POS');
    }

    // Obtenemos el modelo Order correcto según lo que esté disponible
    var _super_order = models.Order.prototype;

    models.Order = models.Order.extend({
        export_for_printing: function () {
            var result = _super_order.export_for_printing.apply(this, arguments);

            // Tus modificaciones al ticket
            if (this.pos.config.name.includes('Tienda 1')) {
                    result.company.name = "Zoopet S.L.U";
                } else {
                    result.company.name = "PetPoint";
                }

            return result;
        },
    });

    return models;
});
