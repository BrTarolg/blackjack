import random

class Deck(object):

    def __init__(self):
        self.suits = ["S","D","H","C"]
        self.faces = range(2,11) + ["A","K","J","Q"]
        self.source = []
        for x in self.faces:
            for y in self.suits:
                self.source.append((x,y))

    def deal(self):
        dealt_card = self.source.pop(0)
        print "just dealt", dealt_card
        return dealt_card

    def shuffle(self):
        random.shuffle(self.source)

class Hand(object):

    def __init__(self,cards=[]):
        self.hand = []
        self.hand.extend(cards)
        self.betsize = 0

    def hand_eval(self, what_type):
        convert = {"K": 10, "Q": 10, "J": 10, "A": 1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10}
        hand_length = len(self.hand)
        true_value = 0
        Ace = False
        for x in range(hand_length):
            converted_card = convert.get(self.hand[x][0])
            true_value += converted_card
            if self.hand[x][0] == "A":
                Ace = True
        if what_type == "big" and Ace == True:
            return true_value+10
        else:
            return true_value

    def hand_eval_true(self):
        if self.hand_eval("big") == self.hand_eval("small"):
            foo = self.hand_eval("small")
            return foo
        elif (self.hand_eval("big") > 21):
            return self.hand_eval("small")
        else:
            return self.hand_eval("big")

    def hit(self):
        card = Player.main_deck.deal()
        self.hand.append(card)

    def hold(self):
        pass

    def double(self):
        self.betsize = self.betsize*2
        self.hit()

    def makebet(self):
        goodinput = False
        while not goodinput:
            try:
                self.betsize = int(raw_input("> input betsize please "))
                goodinput = True
            except ValueError:
                print "that's not a number dude, try again"
                continue

    def dealer(self):
        print "computer's turn!"
        while (self.hand_eval_true() < 17):
            self.hit()
            print "dealers hand is", self.hand
            print "dealers value is small: ", self.hand_eval("small"), " big: ", self.hand_eval("big")

    def return_cards(self,deck):
        hand_length = len(self.hand)
        for x in range(hand_length):
            foo = self.hand.pop()
            deck.source.append(foo)
        deck.shuffle()
        print "the size of the deck is now" ,len(deck.source)

class Player(object):
    main_chips = 1000
    main_deck = Deck()

    def __init__(self):
        self.mainhand = Hand()
        self.handlist = []

    def split(self,instance):
        if len(instance.hand) != 2 or instance.hand[0][0] != instance.hand [1][0]:
            print "hand len != 2 or no pair"
            pass
        else:
            cards1 = [instance.hand.pop(0)]
            foohand = Hand(cards1)
            foohand.betsize = instance.betsize
            self.play(foohand)

    def win_check(self,instance,dealer):
        dealer_value = dealer.mainhand.hand_eval_true
        player_value = instance.hand_eval_true

        if player_value() == 21:
            print "blackjack!"
            Player.main_chips += instance.betsize*1.5
        elif player_value() > 21 or (dealer_value() >= player_value() and dealer_value() <= 21):
            print "you lose!"
            Player.main_chips -= instance.betsize
        else:
            print "you won!"
            Player.main_chips += instance.betsize

        print "you now have chips:", Player.main_chips

    def play(self,instance):
        #plays out the hand to finalise its value
        self.handlist.append(instance)
        endhand = False
        can_double = True
        print "your current hand is", instance.hand
        print "your current hand value is", instance.hand_eval_true()
        print "the dealer is showing", Engine.a_dealer.mainhand.hand_eval_true()

        while (instance.hand_eval_true() < 21 and endhand == False):
            choice = raw_input("> would you like to hit, hold, double or split?\n")
            if choice == "hit":
                instance.hit()
                can_double = False
            elif choice == "hold":
                instance.hold()
                endhand = True
            elif choice == "double" and can_double == True:
                instance.double()
                endhand = True
            elif choice == "split":
                self.split(instance)
            else:
                print "you picked something that isn't there, try again!"
            print "your hand is", instance.hand
            print "the value of that hand is", instance.hand_eval_true()
            print "the dealer value is", Engine.a_dealer.mainhand.hand_eval_true()



class Engine(object):
    ace_start = [("A","S"),("A","C")]
    a_player = Player()
    a_dealer = Player()
    a_player.mainhand.hand = ace_start
    def __init__(self):
        pass

    def play(self):
        Engine.a_player.main_deck.shuffle()
        Engine.a_player.mainhand.makebet()
        Engine.a_dealer.mainhand.hit()
        #Engine.a_player.mainhand.hit()
        #Engine.a_player.mainhand.hit()
        Engine.a_player.play(Engine.a_player.mainhand)
        Engine.a_dealer.mainhand.dealer()
        for x in Engine.a_player.handlist:
            Engine.a_player.win_check(x,Engine.a_dealer)
            x.return_cards(Engine.a_player.main_deck)
        Engine.a_dealer.mainhand.return_cards(Engine.a_player.main_deck)

a_game = Engine()
a_game.play()

"""things to do
return the cards to the Deck
clear the handlist"""
