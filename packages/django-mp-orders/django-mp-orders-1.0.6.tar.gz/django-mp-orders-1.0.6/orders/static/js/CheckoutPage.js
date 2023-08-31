window.CheckoutPage = class {
    constructor({
        $deliveryMethod,
        $city,
        $warehouse
    }) {
        this._$deliveryMethod = $deliveryMethod;
        this._$city = $city;
        this._$warehouse = $warehouse;
        this._$warehouseLabel = $('[data-role=warehouse-label]');
        this._$addressLabel = $('[data-role=address-label]');
        this._$deliveryTypes = $('[data-role=novaposhta-delivery-types]');
        this._$selfDeliveryOption = $('[data-role=novaposhtaselfdelivery]');
        this._cityReference = '';

        this._buildCityAutocomplete();
        this._buildWarehouseAutocomplete();

        $deliveryMethod.on('change', this._handleDeliveryMethodChange);
        $('[name=novaposhtatype]').change(this._updateAddressLabel);

        this._handleDeliveryMethodChange();
        this._updateAddressLabel();
    }

    _buildCityAutocomplete = () => {
        this._$city.prop('autocomplete', 'off');
        this._$city.autocomplete({
            minChars: 2,
            noCache: true,
            containerClass: 'checkout-autocomplete',
            lookup: (query, done) => $.get(
                'https://mp-team.in.ua/' + lang_code + '/delivery/cities/',
                {query},
                (response) => done(response)
            ),
            onSelect: (item) => {
                this._$warehouse.val('');
                this._cityReference = item.reference;
            }
        });
    }

    _buildWarehouseAutocomplete = () => {
        this._$warehouse.prop('autocomplete', 'off');
        this._$warehouse.autocomplete({
            minChars: 0,
            noCache: true,
            containerClass: 'checkout-autocomplete',
            lookup: (query, done) => $.get(
                'https://mp-team.in.ua/' + lang_code + '/delivery/warehouses/',
                {
                    query,
                    delivery_method: this._$deliveryMethod.val(),
                    city: this._cityReference
                },
                (response) => done(response)
            ),
        });
    }

    _handleDeliveryMethodChange = () => {
        const method = this._$deliveryMethod.val();
        const action = (
            !method || method === "self_delivery"
        ) ? 'hide' : 'show';

        this._$city.parent()[action]();
        this._$warehouse.parent()[action]();
        this._$deliveryTypes[action]();
    }

    _updateAddressLabel = () => {
        if (this._$selfDeliveryOption.is(':checked')) {
            this._$warehouseLabel.show();
            this._$addressLabel.hide();
        } else {
            this._$warehouseLabel.hide();
            this._$addressLabel.show();
        }
    }
}
