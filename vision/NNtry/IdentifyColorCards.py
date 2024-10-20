class IdentifyColorCards:
    def __init__(self, _is_it_card_colour_by_hand):
        self.card_colour_list = [] # 0:red 1:blue 2:green
        self.is_it_card_colour_by_hand = _is_it_card_colour_by_hand # True or False

        if self.is_it_card_colour_by_hand:
            print("Yes! Card colour is by hand! You need to call 'IdentifyColorCards.set_card_colour_list()'function.")
        else:
            print("No! Card colour is not by hand!")
            self.__no_card_colour_is_not_by_hand__()

    def set_card_colour_list(self, _card_colour_list):
        self.card_colour_list = _card_colour_list

    def __no_card_colour_is_not_by_hand__(self):
        pass # a function to do analyse


    def get_first_card_colour(self):
        print("first card colour:", self.card_colour_list[0])
        return self.card_colour_list[0]

    def get_second_card_colour(self):
        print("second card colour:", self.card_colour_list[1])
        return self.card_colour_list[1]



if __name__ == '__main__':
    identify_color_cards = IdentifyColorCards(_is_it_card_colour_by_hand=True)
    identify_color_cards.set_card_colour_list([0, 1]) # 测试时修改 0:red 1:blue 2:green

    identify_color_cards.get_first_card_colour()
    identify_color_cards.get_second_card_colour()