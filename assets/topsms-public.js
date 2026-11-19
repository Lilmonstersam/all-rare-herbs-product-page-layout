(function ( $ ) {
	'use strict';

	/**
	 * All of the code for your public-facing JavaScript source
	 * should reside in this file.
	 *
	 * Note: It has been assumed you will write jQuery code here, so the
	 * $ function reference has been prepared for usage within the scope
	 * of this function.
	 *
	 * This enables you to define handlers, for when the DOM is ready:
	 *
	 * $(function() {
	 *
	 * });
	 *
	 * When the window is loaded:
	 *
	 * $( window ).load(function() {
	 *
	 * });
	 *
	 * ...and/or other possibilities.
	 *
	 * Ideally, it is not considered best practise to attach more than a
	 * single DOM-ready or window-load handler for a particular page.
	 * Although scripts in the WordPress core, Plugins and Themes may be
	 * practising this, we should strive to set a better example in our own work.
	 */
	jQuery( document ).ready(
		function ($) {
			var consentMoveTimer;

			function findConsentControl() {
				var $byId = $( '#topsms-customer-consent, [id*="topsms-customer-consent"], [id*="topsms/customer-consent"], [name*="topsms/customer-consent"], [name*="topsms-customer-consent"]' );
				if ( $byId.length ) {
					return $byId.first();
				}

				return $( '.wc-block-checkout label' ).filter(
					function () {
						return $.trim( $( this ).text() ).replace( /\s+/g, ' ' ) === 'Receive SMS Notifications';
					}
				).first();
			}

			function moveConsentAbovePlaceOrder() {
				var $consent = findConsentControl();
				if ( ! $consent.length ) {
					return;
				}

				var $wrapper = $consent.closest( '.wc-block-components-checkbox' );
				if ( ! $wrapper.length ) {
					$wrapper = $consent.closest( '#topsms-customer-consent' );
				}
				if ( ! $wrapper.length ) {
					$wrapper = $consent;
				}

				var $actions = $( '.wc-block-checkout__actions' ).first();
				if ( $actions.length && $wrapper.next()[0] !== $actions[0] ) {
					$wrapper.addClass( 'topsms-consent-above-place-order' );
					$wrapper.insertBefore( $actions );
				}
			}

			function scheduleConsentMove() {
				window.clearTimeout( consentMoveTimer );
				consentMoveTimer = window.setTimeout( moveConsentAbovePlaceOrder, 50 );
			}

			moveConsentAbovePlaceOrder();
			$( document.body ).on( 'updated_checkout', scheduleConsentMove );
			if ( window.MutationObserver ) {
				var checkoutRoot = document.querySelector( '.wc-block-checkout, form.woocommerce-checkout' );
				if ( checkoutRoot ) {
					new MutationObserver( scheduleConsentMove ).observe( checkoutRoot, { childList: true, subtree: true } );
				}
			}

			// When the checkbox changes, update cart
			$( document ).on(
				'change',
				'#topsms-customer-consent',
				function () {
					// Save the checkbox state
					var isChecked = $( this ).is( ':checked' ) ? 1 : 0;

					// Get nonce from the field that wp_nonce_field created
					var nonce = $( '#topsms_consent_nonce' ).val();

					// Trigger cart update
					$( 'body' ).trigger( 'update_checkout' );

					// Use AJAX to store the preference in the session
					$.ajax(
						{
							type: 'POST',
							url: wc_checkout_params.ajax_url,
							data: {
								'action': 'topsms_update_consent',
								'consent': isChecked,
								'security': nonce
							}
						}
					);
				}
			);
		}
	);

    jQuery( document ).ready(
        function($) {
            // Get url params.
            function getUrlParameter(name) {
                name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
                var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
                var results = regex.exec(location.search);
                return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
            }

            // Check if utm parameters exist and if source is topsms.
            var utmSource = getUrlParameter('utm_source');
            if (utmSource && utmSource.toLowerCase() === 'topsms') {
                if (typeof topsmsPublic === 'undefined' || !topsmsPublic.adminAjaxUrl) {
                    return;
                }

                var utmData = {
                    utm_campaign: getUrlParameter('utm_campaign'),
                    utm_id: getUrlParameter('utm_id'),
                };

                // Use AJAX to set utm cookie.
                $.ajax({
                    type: 'POST',
                    url: topsmsPublic.adminAjaxUrl,
                    data: {
                        'action': 'topsms_capture_utm_parameters',
                        'utm_data': utmData,
                        'security': topsmsPublic.nonce
                    }
                });
            }
        }
    );

})( jQuery );
