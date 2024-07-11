<?php

namespace MNS\Jaayegah\Includes\Logistics;

use Automattic\WooCommerce\Internal\DataStores\Orders\CustomOrdersTableController;
use MNS\Jaayegah\Includes\Admin\Options;
use MNS\Jaayegah\Includes\Logistic;
use MNS\Jaayegah\Includes\Order;
use MNS\Jaayegah\Includes\RestApi;
use MNS\Jaayegah\Includes\Shippings\Method;
use MNS\Jaayegah\Templates\Snippets;

class SnappBox extends Logistic
{
	public function init()
	{
		$this->key = 'snappbox';
		$this->name = __('Snapp Box', 'mnsjay');
		$this->name_en = 'Snapp Box';
		$this->icon = MNS_JAAYEGAH_URL . 'assets/img/snappbox.png';
		$this->base_url = 'https://corporate.snapp.site';
		$this->supports = ['costs'];
		$this->options = [
			'active' => [
				'title' => __('Activation', 'mnsjay'),
				'type' => 'checkbox',
				'default' => '',
				'description' => sprintf(
					__('Activate %s logistic service.', 'mnsjay'),
					'<a href="https://corporate.snapp.site/" target="_blank">' . $this->name . '</a>'
				),
			],
			'token' => [
				'title' => __('Token', 'mnsjay'),
				'type' => 'text',
				'class' => 'regular-text code',
				'default' => '',
				'description' => sprintf(
					__('Enter your %s account access token.<br>Webhook URL: %s', 'mnsjay'),
					$this->name,
					'<code>' . mns_jaayegah()->utils()->get_webhook_url('snappbox') . '</code>'
				),
			],
			'origin_fullname' => [
				'title' => __('Sender Fullname', 'mnsjay'),
				'type' => 'text',
				'default' => '',
				'class' => 'regular-text',
				'description' => __('Enter sender fullname.', 'mnsjay'),
			],
			'origin_mobile' => [
				'title' => __('Sender Mobile Number', 'mnsjay'),
				'type' => 'text',
				'default' => '',
				'class' => 'regular-text',
				'description' => __('Enter sender mobile number.', 'mnsjay'),
			],
		];
		$this->method_options = [
			'city' => [
				'title' => __('Terminal City', 'mnsjay'),
				'type' => 'select',
				'options' => static::cities(),
				'default' => 'tehran',
				'class' => 'regular-text',
				'description' => __('Choose terminal origin city.', 'mnsjay'),
			],
			'delivery' => [
				'title' => __('Delivery Type', 'mnsjay'),
				'type' => 'select',
				'options' => static::deliveries(),
				'default' => 'bike',
				'class' => 'regular-text',
				'description' => __('Choose the type of delivery vehicle. Make sure to choose a delivery type that is supported in your city.', 'mnsjay'),
			],
			'payment' => [
				'title' => __('Payment Type', 'mnsjay'),
				'type' => 'select',
				'options' => static::payment_types(),
				'default' => 'cod',
				'class' => 'regular-text',
				'description' => __('Choose the type of shipping payment.', 'mnsjay'),
			],
		];

		if (!$this->is_active())
			return;

		add_action('add_meta_boxes', [$this, 'register_metaboxes']);
		add_action('mns_jaayegah_rest_register_routes', [$this, 'register_routes']);
		add_filter('mns_jaayegah_shipping_snappbox_base_cost', [$this, 'calculate_cost'], 10, 3);
		add_action('mns_jaayegah_webhook_snappbox', [$this, 'webhook_update_order']);
	}

	public function is_active()
	{
		return $this->get_option('active') === 'yes';
	}

	public static function order_statuses()
	{
		return [
			'PENDING' => 'در انتظار پیک',
			'ACCEPTED' => 'پذیرفته شده',
			'ARRIVED_AT_PICK_UP' => 'رسیده به مبدا',
			'PICKED_UP' => 'جمع‌آوری شده',
			'ARRIVED_AT_DROP_OFF' => 'رسیده به مقصد',
			'DELIVERED' => 'تحویل شده',
			'CANCELLED' => 'لغو شده'
		];
	}

	public static function deliveries()
	{
		return [
			'bike-without-box' => 'پیک - ارسال سریع',
			'bike' => 'باکس پلاس - با جعبه',
			'van' => 'وانت سبک',
			'van-heavy' => 'وانت سنگین',
			'truck' => 'اثاث کشی - منزل و محل کار',
			'big-box' => 'بیگ باکس',
			'box-plus' => 'باکس پلاس',
			'easy-destination' => 'باکس پلاس ایزی - با مقصد تقریبی',
			'carbox2' => 'کارباکس'
		];
	}

	public static function cities()
	{
		return [
			'tehran' => 'تهران',
			'mashhad' => 'مشهد',
			'karaj' => 'کرج',
			'isfahan' => 'اصفهان',
			'tabas' => 'طبس',
			'zanjan' => 'زنجان',
			'ilam' => 'ایلام',
			'qom' => 'قم',
			'birjand' => 'بیرجند',
			'shiraz' => 'شیراز'
		];
	}

	public static function payment_types()
	{
		return [
			'cod' => 'پرداخت در مقصد',
			'prepaid' => 'پرداخت در مبدا'
		];
	}

	public static function cities_deliveries()
	{
		return [
			'mashhad' => [
				'bike-without-box',
				'bike',
				'van',
				'truck',
				'easy-destination',
				'van-heavy'
			],
			'karaj' => [
				'van',
				'bike',
				'big-box'
			],
			'isfahan' => [
				'bike-without-box',
				'bike',
				'van',
				'truck'
			],
			'tabas' => [
				'bike-without-box',
				'bike',
				'van',
				'truck'
			],
			'zanjan' => [
				'bike-without-box',
				'bike'
			],
			'tehran' => [
				'bike-without-box',
				'bike',
				'van',
				'van-heavy',
				'truck',
				'big-box',
				'nxh',
				'nxb',
				'box-plus',
				'easy-destination',
				'carbox2'
			],
			'ilam' => [
				'bike-without-box'
			],
			'qom' => [
				'bike-without-box',
				'bike',
				'van',
				'big-box'
			],
			'birjand' => [
				'van'
			],
			'shiraz' => [
				'bike',
				'truck',
				'bike-without-box'
			]
		];
	}

	public static function convert_currency($price, ?string $from = null, ?string $to = null)
	{
		$from = $from ? $from : get_woocommerce_currency();
		$to = $to ? $to : get_woocommerce_currency();

		if ($from === $to)
			return $price;

		$ratio = [
			'IRR' => 1,
			'IRT' => 0.1,
			'IRHR' => 0.001,
			'IRHT' => 0.0001,
		];

		if (!isset($ratio[$to]) or !isset($ratio[$from]))
			return $price;

		$ratio = $ratio[$to] / $ratio[$from];

		return ceil($price * $ratio);
	}

	protected function _post(string $endpoint, array $body = [])
	{
		$response = $this->request($endpoint, [
			'method' => 'POST',
			'headers' => [
				'Content-type' => 'application/json',
				'Authorization' => $this->get_option('token'),
			],
			'body' => wp_json_encode($body),
		]);

		if (is_wp_error($response))
			return $response;

		if (!is_array($response))
			return new \WP_Error('no-response', 'No response from Snapp Box servers', $response);

		if (isset($response['api_status']) and $response['api_status'] !== 'success')
			return new \WP_Error('api-error', $response['message'] ?? 'Unknown error', $response);

		return $response;
	}

	public function calculate_cost(float $cost, array $package, Method $method): float
	{
		if ($method->get_data()->base_options('payment', $this->get_key()) === 'cod')
			return 0;

		$products = array_map(function ($cart_item) {
			return [
				'packageValue' => (int) static::convert_currency(wc_get_price_including_tax($cart_item['data']), null, 'IRR'),
				'externalRefType' => 'INSURANCE',
				'externalRefId' => 99,
				'quantity' => $cart_item['quantity'],
				'quantityMeasuringUnit' => 'unit'
			];
		}, $package['contents']);

		$args = [
			'city' => $method->get_data()->base_options('city', $this->get_key()),
			'customerWalletType' => null,
			'deliveryCategory' => $method->get_data()->base_options('delivery', $this->get_key()),
			'isReturn' => false,
			'loadAssistance' => false,
			'voucherCode' => null,
			'waitingTime' => 0,
			'items' => array_values($products),
			'terminals' => [
				[
					'address' => $method->get_origin()->get_address(),
					'sequenceNumber' => 1,
					'latitude' => $method->get_origin()->get_coords()->get_lat(),
					'longitude' => $method->get_origin()->get_coords()->get_lng(),
					'type' => 'pickup'
				],
				[
					'address' => empty($package['destination']['address']) ? 'خیابان' : trim($package['destination']['address']),
					'sequenceNumber' => 2,
					'latitude' => $method->get_destination_coords($package)->get_lat(),
					'longitude' => $method->get_destination_coords($package)->get_lng(),
					'type' => 'drop'
				]
			]
		];

		$try = 0;
		$tolerance = 5;

		do {

			$try++;
			$response = $this->_post('/v1/customer/order/pricing', $args);

		} while (is_wp_error($response) and $try <= $tolerance);

		if (is_wp_error($response) or !isset($response['finalCustomerFare'])) {
			$cost = 0;
		} else {
			$cost = $response['finalCustomerFare'];
		}

		$cost = static::convert_currency($cost, 'IRR');
		$cost = ceil($cost / 1000) * 1000;

		return $cost;
	}

	public function get_order_meta(Order $order, string $key)
	{
		return $order->get_meta('snappbox_' . $key);
	}

	public function set_order_meta(Order $order, string $key, $value)
	{
		$order->set_meta('snappbox_' . $key, $value);
	}

	protected function register_order(Order $order)
	{
		if (!$this->is_order($order))
			return new \WP_Error($this->get_key(), sprintf(__('This is\'n %s order.', 'mnsjay'), $this->name));

		$method = current($this->get_shipping_methods($order));

		$products = array_map(function ($order_item) {
			$order_item = new \WC_Order_Item_Product($order_item);
			return [
				'pickedUpSequenceNumber' => 1,
				'dropOffSequenceNumber' => 2,
				'name' => $order_item->get_name(),
				'quantity' => $order_item->get_quantity(),
				'quantityMeasuringUnit' => 'unit',
				'packageValue' => ceil(static::convert_currency($order_item->get_total(), null, 'IRR')),
				'externalRefType' => 'INSURANCE',
				'externalRefId' => 99
			];
		}, $order->get_order()->get_items());

		if ($order->get_order()->has_shipping_address()) {
			$fullname = $order->get_order()->get_formatted_shipping_full_name();
			$address = trim($order->get_order()->get_shipping_address_1() . ' ' . $order->get_order()->get_shipping_address_2());
			$coords = $order->get_coords('shipping');
		} else {
			$fullname = $order->get_order()->get_formatted_billing_full_name();
			$address = trim($order->get_order()->get_billing_address_1() . ' ' . $order->get_order()->get_billing_address_2());
			$coords = $order->get_coords('billing');
		}

		$args = [
			'data' => [
				'itemDetails' => array_values($products),
				'orderDetails' => [
					'city' => $method->get_data()->base_options('city', $this->get_key()),
					'customerWalletType' => null,
					'deliveryCategory' => $method->get_data()->base_options('delivery', $this->get_key()),
					'deliveryFarePaymentType' => $method->get_data()->base_options('payment', $this->get_key()),
					'isReturn' => false,
					'loadAssistance' => false,
					'pricingId' => null,
					'sequenceNumberDeliveryCollection' => 1,
					'orderLevelServices' => [
						[
							'id' => 4,
							'quantity' => 1
						]
					],
					'customerName' => $fullname,
					'customerEmail' => $order->get_order()->get_billing_email(),
					'customerPhonenumber' => $order->get_order()->get_billing_phone(),
					'customerRefId' => 'mns_jaayegah_' . $order->get_id(),
					'voucherCode' => null,
					'waitingTime' => 0,
				],
				'pickUpDetails' => [
					[
						'id' => null,
						'type' => 'pickup',
						'sequenceNumber' => 1,
						'paymentType' => $method->get_data()->base_options('payment', $this->get_key()),
						'contactName' => $this->get_option('origin_fullname'),
						'contactPhoneNumber' => $this->get_option('origin_mobile'),
						'address' => $method->get_origin()->get_address(),
						'latitude' => $method->get_origin()->get_coords()->get_lat(),
						'longitude' => $method->get_origin()->get_coords()->get_lng(),
						'editMerchandiseInfo' => null,
						'plate' => '',
						'unit' => '',
						'comment' => '',
						'vendorId' => 0,
						'services' => [
							[
								'itemServiceId' => 1,
								'quantity' => 1
							]
						]
					]
				],
				'dropOffDetails' => [
					[
						'id' => null,
						'type' => 'drop',
						'sequenceNumber' => 2,
						'paymentType' => $method->get_data()->base_options('payment', $this->get_key()),
						'contactName' => $fullname,
						'contactPhoneNumber' => $order->get_order()->get_billing_phone(),
						'address' => $address,
						'latitude' => $coords->get_lat(),
						'longitude' => $coords->get_lng(),
						'editMerchandiseInfo' => null,
						'plate' => '',
						'unit' => '',
						'comment' => '',
						'vendorId' => 0,
						'services' => [
							[
								'itemServiceId' => 1,
								'quantity' => 1
							]
						]
					]
				]
			]
		];

		return $this->_post('/v1/customer/create_order', $args);
	}

	public function register_metaboxes()
	{
		$screen = wc_get_container()->get(CustomOrdersTableController::class)->custom_orders_table_usage_is_enabled()
			? wc_get_page_screen_id('shop-order')
			: 'shop_order';

		add_meta_box('mns_jaayegah_snappbox_order', $this->name, [$this, 'order_metabox_output'], $screen, 'side', 'default');
	}

	public function register_routes(RestApi $rest_api)
	{
		register_rest_route($rest_api->namespace() . '/' . $this->key, '/register', [
			'methods' => \WP_REST_Server::CREATABLE,
			'callback' => [$this, 'rest_order_register'],
			'args' => [
				'order_id' => [
					'default' => 0,
					'required' => true,
					'sanitize_callback' => fn($value, $request, $param) => intval($value),
					'validate_callback' => function ($value) {
						return \Automattic\WooCommerce\Utilities\OrderUtil::is_order($value, wc_get_order_types());
					}
				],
			],
			'permission_callback' => fn() => current_user_can('edit_shop_orders')
		]);

		register_rest_route($rest_api->namespace() . '/' . $this->key, '/cancel', [
			'methods' => \WP_REST_Server::CREATABLE,
			'callback' => [$this, 'rest_order_cancel'],
			'args' => [
				'order_id' => [
					'default' => 0,
					'required' => true,
					'sanitize_callback' => fn($value, $request, $param) => intval($value),
					'validate_callback' => function ($value) {
						return \Automattic\WooCommerce\Utilities\OrderUtil::is_order($value, wc_get_order_types());
					}
				],
			],
			'permission_callback' => fn() => current_user_can('edit_shop_orders')
		]);
	}

	public function rest_order_register(\WP_REST_Request $request)
	{
		$order = mns_jaayegah()->utils()->get_order($request->get_param('order_id'));
		$response = $this->register_order($order);

		if (is_wp_error($response))
			return $response;

		$this->set_order_meta($order, 'orderId', intval($response['orderId']));
		$this->set_order_meta($order, 'finalCustomerFare', $response['finalCustomerFare']);
		$this->set_order_meta($order, 'trackingUrl', $response['details']['trackingUrl']);
		$this->set_order_meta($order, 'maskedId', $response['details']['maskedId']);
		$this->set_order_meta($order, 'status', $response['details']['status']);

		$admin_note = sprintf(__('This order registered in Snapp Box. Order Number: %s', 'mnsjay'), $response['orderId']);
		$tracking_note = sprintf(__('Tracking URL: %s', 'mnsjay'), $response['details']['trackingUrl']);
		$customer_note = __('Your shipment registered in Snapp Box.', 'mnsjay');

		$order->get_order()->set_status(Options::get_order_waiting_status());
		$order->get_order()->add_order_note($admin_note);
		$order->get_order()->add_order_note($tracking_note);
		$order->get_order()->add_order_note($customer_note, true);
		$order->get_order()->save();

		do_action('mns_jaayegah_snappbox_after_register', $order);

		return new \WP_REST_Response(true);
	}

	public function rest_order_cancel(\WP_REST_Request $request)
	{
		$order = mns_jaayegah()->utils()->get_order($request->get_param('order_id'));

		$response = $this->_post('/v1/customer/cancel_order', [
			'orderId' => $this->get_order_meta($order, 'orderId')
		]);

		if (is_wp_error($response))
			return $response;

		$this->set_order_meta($order, 'orderId', null);
		$this->set_order_meta($order, 'finalCustomerFare', null);
		$this->set_order_meta($order, 'trackingUrl', null);
		$this->set_order_meta($order, 'maskedId', null);
		$this->set_order_meta($order, 'status', null);

		$admin_note = __('This order canceled from Snapp Box by shop admin.', 'mnsjay');

		$order->get_order()->set_status(Options::get_order_packaged_status());
		$order->get_order()->add_order_note($admin_note);
		$order->get_order()->save();

		do_action('mns_jaayegah_tipax_after_cancel', $order);

		return new \WP_REST_Response(true);
	}

	public function webhook_update_order($inputs)
	{
		if (empty($inputs['webhookType']) or empty($inputs['customerRefId']))
			return;

		$order_id = (int) explode('_', $inputs['customerRefId'])[2];
		$order = mns_jaayegah()->utils()->get_order($order_id);

		if (!$order)
			return;

		switch ($inputs['webhookType']) {

			case 'ORDER_ACCEPTED':

				$this->set_order_meta($order, 'status', $inputs['orderStatus']);
				$this->set_order_meta($order, 'bikerName', $inputs['bikerName']);
				$this->set_order_meta($order, 'bikerPhone', $inputs['bikerPhone']);
				$this->set_order_meta($order, 'bikerPhotoUrl', $inputs['bikerPhotoUrl']);

				$admin_note = sprintf(__('This order accepted by %s in Snapp Box. Phone: %s', 'mnsjay'), $inputs['bikerName'], $inputs['bikerPhone']);
				$customer_note = sprintf(__('Your shipment accepted by %s in Snapp Box.', 'mnsjay'), $inputs['bikerName']);

				$order->get_order()->set_status(Options::get_order_ready_status());
				$order->get_order()->add_order_note($admin_note);
				$order->get_order()->add_order_note($customer_note, true);
				$order->get_order()->save();

				break;

			case 'ORDER_STATUS_UPDATE':

				$this->set_order_meta($order, 'status', $inputs['orderStatus']);

				if ($inputs['orderStatus'] === 'ARRIVED_AT_PICK_UP') {

					$admin_note = __('Snapp Box biker arrived at pickup location.', 'mnsjay');

				} elseif ($inputs['orderStatus'] === 'PICKED_UP') {

					$admin_note = __('Snapp Box biker picked the shipment up.', 'mnsjay');

				} elseif ($inputs['orderStatus'] === 'ARRIVED_AT_DROP_OFF') {

					$admin_note = __('Snapp Box biker arrived at dropoff location.', 'mnsjay');

				} elseif ($inputs['orderStatus'] === 'DELIVERED') {

					$order->get_order()->set_status(Options::get_order_delivery_status());
					$admin_note = __('Snapp Box biker delivered the shipment to customer.', 'mnsjay');

				}

				$order->get_order()->add_order_note($admin_note);
				$order->get_order()->save();

				break;

			case 'ORDER_CANCELLED':

				$this->set_order_meta($order, 'status', $inputs['orderStatus']);

				$admin_note = __('This order canceled from Snapp Box.', 'mnsjay');

				$order->get_order()->set_status(Options::get_order_packaged_status());
				$order->get_order()->add_order_note($admin_note);
				$order->get_order()->save();

				break;
		}
	}

	public function order_metabox_output($order)
	{
		$order = mns_jaayegah()->utils()->get_order($order);

		if (!$this->is_order($order)) {
			echo '<p>' . __('This order shipping is not a Snapp Box method. To access this panel, add a Snapp Box shipping method first.', 'mnsjay') . '</p>';
			return;
		}

		Snippets::load_template('metabox/order-snappbox', [
			'order' => $order,
			'snappbox' => $this
		]);
	}
}
