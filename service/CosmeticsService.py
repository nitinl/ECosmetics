from dao import ProductRepo


class CosmeticsService:

    @staticmethod
    def processcosmeticsdata(cosmeticsdata):
        CosmeticsService.process_products(cosmeticsdata)

    @staticmethod
    def process_products(products):
        for p in products:
            ProductRepo.create_product(p)
