from dao import ProductRepo


class CosmeticsService:

    @staticmethod
    def processcosmeticsdata(cosmeticsproducts):
        for product in cosmeticsproducts:
            ProductRepo.create_product(product)
