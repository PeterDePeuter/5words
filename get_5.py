from ast import Not
from concurrent.futures import thread
from operator import le
import re
import sys

onlyalpha = re.compile("^[a-z]+$")


def readfile()->list:
    allwords_list = []
    for word in open("small_list.txt").readlines():   
        word = word[:-1]
        word = word.lower()


        if ( len(word) != 5):
            continue
        if ( not onlyalpha.match(word)):
            continue

        #all letters in the word should be unique
        unique = True
        uq_letters = set()
        for letter in word:
            if letter in uq_letters:
                unique = False
                break
            uq_letters.add(letter)
        if not unique:
            continue

        allwords_list.append(word)
    return allwords_list




class CWordList(object):
    def __init__(self,wordlist:list):
        self.sourcewordset = set(wordlist)
        self.Populate()

    def Populate(self):
        self.all_letters={}
        for char in range(ord("a"),ord("z")+1):
            self.all_letters[chr(char)] = set()
        for word in self.sourcewordset:
            for letter in word:
                self.all_letters[letter].add(word)
        self.wordset = self.sourcewordset

    ###removes a word from wordlist and resets the rest
    def RemoveWord(self,word):
        self.sourcewordset.remove(word)
        self.Populate()

    ###we get a word, and want to remove all the other words from the wordlist which contain a letter from this word
    def Clean(self,word):
        removed = set()
        for letter in word:
            wordstoremove = list(self.all_letters[letter])
            for toclean in wordstoremove:
                if not toclean in removed:
                    self.wordset.remove(toclean)
                    removed.add(toclean)
                self.all_letters[letter].remove(toclean)

    def GetFirst(self):
        return next(iter(self.wordset))

    def len(self):
        return len(self.wordset)
    


#word list is een lijst van alle woorden 
#all_letters is een lijst van alle letters en per letter een lijst van alle woorden die deze letter bevatten


def find(wordlist):
    AllWords = CWordList(wordlist)
    while AllWords.len() > 5: 
        first = AllWords.GetFirst()
        print(f"first : {first}")

        #remove all the words with the letters in this word
        AllWords.Clean(first)

        if ( AllWords.len() == 0):
            #dat was geen success .... ander woord zoeken
            AllWords.RemoveWord(first)
            print("kaput in 1")
        else:
            print(f"we hebben er nog over : {AllWords.len()}")

            #OK now we have only words with different letters in the list, take a random one as second 
            second = AllWords.GetFirst()
            print(f"second : {second}")

            #remove all the words with the letters in the second word
            AllWords.Clean(second)
            if ( AllWords.len() == 0):
                #dat was geen success .... ander woord zoeken
                AllWords.RemoveWord(first)
                #print("kaput in 2")
            else:
                print(f"we hebben er nog over : {AllWords.len()}")

                third = AllWords.GetFirst()       
                #remove all the words with the letters in the third word
                AllWords.Clean(third)
                if ( AllWords.len() == 0):
                    #dat was geen success .... ander woord zoeken
                    AllWords.RemoveWord(first)
                    #print("kaput in 3")
                else:
                    print(f"we hebben er nog over : {AllWords.len()}")
                    fourth =  AllWords.GetFirst()
                    #remove all the words with the letters in the fourth word
                    AllWords.Clean(fourth)

                    if ( AllWords.len() == 0):
                        #dat was geen success .... ander woord zoeken
                        AllWords.RemoveWord(first)
                        #print("kaput in 4")
                    else:
                        print(f"we hebben er nog over : {AllWords.len()}")


                        if ( AllWords.len() == 0):
                            #dat was geen success .... ander woord zoeken
                            AllWords.RemoveWord(first)
                        else:
                            #aha !! we hebben 4 woorden en nog een aantal vijfde !! eens kijken
                            print("success !!!")
                            print(first,second,third,fourth)
                            print(AllWords.wordset)
                            AllWords.RemoveWord(first)

allwords = readfile()

find(allwords)


