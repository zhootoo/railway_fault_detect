class Property:
    def __init__(self,square_feet='',beds = '',baths='',**kwargs):
        super().__init__(**kwargs)
        self.square_feet = square_feet
        self.beds = beds
        self.baths = baths

    def display(self):
        print('PROPERTY DETAILS')
        print('================')
        print('房屋面积: {}'.format(self.square_feet))
        print('卧室数量: {}'.format(self.beds))
        print('浴室数量: {}'.format(self.baths))
        print()

    @staticmethod
    def prompt_init():
        return dict(square_feet = input('房屋面积:'),
                    beds = input('卧室数量:'),
                    baths = input('浴室数量:'))
class House(Property):
    valid_garage = ('连接','分离','无')
    valid_fenced = ('有','无')

    def __init__(self,num_stories='',garage='',fenced='',**kwargs):
        super.__init__(**kwargs)
        self.num_stories = num_stories
        self.garage = garage
        self.fenced = fenced

    def display(self):
        super().display()
        print('HOUSE DETAILS')
        print('#围墙数量: {}'.format(self.num_stories))
        print('车库: {}'.format(self.garage))
        print('围栏:{}'.format(self.fenced))
    @staticmethod
    def prompt_init():
        parent_init = Property.prompt_init()
        laundry = get_valid_input('有无围栏?',House.valid_fenced)
        balcony = get_valid_input('有无车库?',House.valid_garage)
        num_stories = input('多少围墙?')
        parent_init.update({'fenced':laundry,'garage':balcony,'num_stories':num_stories})
        return parent_init

def get_valid_input(input_string,valid_options):
    input_string += ({}).format(','.join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response

class Apartment(Property):
    valid_laundries = ('投币','支付宝','无')

    def __init__(self,laundry='',**kwargs):
        super.__init__(**kwargs)
        self.laundry = laundry

    def display(self):
        super().display()
        print('APARTMENT DETAILS')
        print('洗衣机: %s' %self.laundry)

    @staticmethod
    def prompt_init():
        parent_init = Property.prompt_init()
        laundry = get_valid_input('What laundry?',Apartment.valid_laundries)
        parent_init.update({'laundry':laundry})
        return parent_init

def get_valid_input(input_string,valid_options):
    input_string += ({}).format(','.join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response

class Purchase:
    def __init__(self,price='',taxes='',**kwargs):
        super.__init__(**kwargs)
        self.price = price
        self.taxes = taxes

    def display(self):
        super().display()
        print('PURCHASE DETAILS')
        print('出售价格: {}'.format(self.price))
        print('估计费率: {}'.format(self.taxes))
    @staticmethod
    def prompt_init():
        return dict(price = input('价格：'),taxes = input('税收：'))

class Rental:
    def __init__(self,furnished='',**kwargs):
        super.__init__(**kwargs)
        self.furnished = furnished

    def display(self):
        super().display()
        print('RENTAL DETAILS')
        print('有无家具: {}'.format(self.furnished))
    @staticmethod
    def prompt_init():
        return dict(furnished = get_valid_input('有无家具?',('有','无')))

class AR(Rental,Apartment):
    @staticmethod
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init

class AP(Purchase,Apartment):
    @staticmethod
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init

if __name__=='__main__':
    e.senn_main('hello')
    print(Contact.all_contacts)
    e = Mix('Jhon','14030@qq.com')
