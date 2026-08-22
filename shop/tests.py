from django.test import TestCase
from django.contrib.auth.models import User

from .models import Category, Product, Cart, CartItem


class ShopTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        # User
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        # Category
        cls.category = Category.objects.create(
            name="Fashion",
            slug="fashion",
            description="Fashion products"
        )

        # Product
        cls.product = Product.objects.create(
            name="Test T-Shirt",
            slug="test-t-shirt",
            category=cls.category,
            description="Test product",
            price=25.00,
            stock=10,
            available=True,
            image=""
        )


    # ==========================================
    # CATEGORY TEST
    # ==========================================

    def test_category_created(self):

        self.assertEqual(
            self.category.name,
            "Fashion"
        )

        self.assertEqual(
            self.category.slug,
            "fashion"
        )


    # ==========================================
    # PRODUCT TEST
    # ==========================================

    def test_product_created(self):

        self.assertEqual(
            self.product.name,
            "Test T-Shirt"
        )

        self.assertEqual(
            self.product.price,
            25.00
        )

        self.assertEqual(
            self.product.stock,
            10
        )

        self.assertTrue(
            self.product.available
        )


    # ==========================================
    # CATEGORY → PRODUCT RELATION
    # ==========================================

    def test_category_products_relation(self):

        self.assertEqual(
            self.category.products.count(),
            1
        )

        self.assertEqual(
            self.category.products.first(),
            self.product
        )


    # ==========================================
    # CART CREATION
    # ==========================================

    def test_cart_creation(self):

        cart = Cart.objects.create(
            user=self.user
        )

        self.assertEqual(
            cart.user,
            self.user
        )


    # ==========================================
    # ADD PRODUCT TO CART
    # ==========================================

    def test_add_product_to_cart(self):

        cart = Cart.objects.create(
            user=self.user
        )

        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=1
        )

        self.assertEqual(
            cart.items.count(),
            1
        )

        self.assertEqual(
            cart_item.product,
            self.product
        )

        self.assertEqual(
            cart_item.quantity,
            1
        )


    # ==========================================
    # CART TOTAL
    # ==========================================

    def test_cart_total_price(self):

        cart = Cart.objects.create(
            user=self.user
        )

        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        self.assertEqual(
            cart.get_total_price(),
            50
        )


    # ==========================================
    # CART TOTAL ITEMS
    # ==========================================

    def test_cart_total_items(self):

        cart = Cart.objects.create(
            user=self.user
        )

        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=3
        )

        self.assertEqual(
            cart.get_total_items(),
            3
        )


    # ==========================================
    # CART ITEM COST
    # ==========================================

    def test_cart_item_cost(self):

        cart = Cart.objects.create(
            user=self.user
        )

        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=4
        )

        self.assertEqual(
            cart_item.get_cost(),
            100
        )


    # ==========================================
    # ADD TO CART VIEW
    # ==========================================

    def test_cart_add_view(self):

        self.client.login(
            username="testuser",
            password="testpassword123"
        )

        response = self.client.get(
            f"/cart/add/{self.product.id}/"
        )

        self.assertEqual(
            response.status_code,
            302
        )

        cart = Cart.objects.get(
            user=self.user
        )

        self.assertTrue(
            cart.items.filter(
                product=self.product
            ).exists()
        )


    # ==========================================
    # ADD SAME PRODUCT AGAIN
    # ==========================================

    def test_add_same_product_again(self):

        self.client.login(
            username="testuser",
            password="testpassword123"
        )

        self.client.get(
            f"/cart/add/{self.product.id}/"
        )

        self.client.get(
            f"/cart/add/{self.product.id}/"
        )

        cart_item = CartItem.objects.get(
            cart__user=self.user,
            product=self.product
        )

        self.assertEqual(
            cart_item.quantity,
            2
        )


    # ==========================================
    # CART DETAIL VIEW
    # ==========================================

    def test_cart_detail_view(self):

        self.client.login(
            username="testuser",
            password="testpassword123"
        )

        response = self.client.get(
            "/cart/"
        )

        self.assertEqual(
            response.status_code,
            200
        )


    # ==========================================
    # REMOVE FROM CART
    # ==========================================

    def test_cart_remove_view(self):

        self.client.login(
            username="testuser",
            password="testpassword123"
        )

        self.client.get(
            f"/cart/add/{self.product.id}/"
        )

        self.client.get(
            f"/cart/remove/{self.product.id}/"
        )

        cart = Cart.objects.get(
            user=self.user
        )

        self.assertFalse(
            cart.items.filter(
                product=self.product
            ).exists()
        )