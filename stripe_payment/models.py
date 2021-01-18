from django.db import models
from model_utils import Choices


class ProductModel(models.Model):
    """
    Class for defining how product model should be represented.
    """

    product_name = models.CharField(max_length=20, null=False, blank=False)
    product_description = models.TextField(max_length=1000, null=False, blank=False)
    product_price = models.DecimalField(max_digits=6, null=False, blank=False, decimal_places=2)
    product_image_url = models.URLField(max_length=500, null=False, blank=False)

    def __str__(self):
        """
        Function to return product name.
        """
        return self.product_name


class PurchaseInfoModel(models.Model):
    """"
    Class for defining how product purchase information model should look like.
    """

    Status_Choice = Choices(
        ("S", "Success"),
        ("F", "Failure")
    )

    customer_name = models.CharField(max_length=128, null=False, blank=True)
    email = models.EmailField(null=True, blank=True)
    country = models.CharField(max_length=50, null=False, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    currency = models.CharField(max_length=20, null=False, blank=True)
    receipt_url = models.URLField(max_length=500, null=False, blank=False)
    mobile_no = models.IntegerField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    transaction_id = models.CharField(max_length=50, null=False, blank=True)
    transaction_status = models.CharField(max_length=1, null=False, blank=False, choices=Status_Choice)
    product = models.ManyToManyField(ProductModel)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Function to return transaction_id.
        """
        return self.transaction_id

