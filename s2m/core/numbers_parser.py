from utils import natural_log, _set_words
    
class NumberParser () : 

    DIGITS = {'deux' : 2, 
            'trois' : 3, 
            'quatre' : 4, 
            'cinq' : 5,
            'six' : 6, 
            'sept' : 7, 
            'huit' : 8, 
            'neuf' : 9,
            }
    
    NUMBERS = {'douze' : 12, 
               'treize' : 13, 
               'quatorze' : 14,
               'quinze' : 15, 
               'seize' : 16,
               }
    
    OTHER_NUMBERS = {'zero' : 0,
              'un' : 1,
              'onze' : 11,
              }
    
    OTHERS = ['dix', 'onze', 'soixante', 'cent', 'mille']
    
    POWERS = { 'mille' : 3,
               'million' : 6, 
               'milliard' : 9, 
               'billion' : 12, 
               'billard' : 15,
               'trillion' : 18,
               'trilliard' : 21, 
               'quatrillon' : 24, 
               'quadrillard' : 27,
               'quintillion' : 30,
               'quintillard' : 33, 
               'sextillion' : 36, 
               'sextillard' : 39,
               'septillion' : 42, 
               'septilliard' : 45, 
               'octillon' : 48,
               'octilliard' : 51,
               'nonillion' : 54, 
               'nonilliard' : 57, 
               'decillion' : 60, 
               'decilliard' : 63,
               }
    
    SAFE_DOZENS = {'vingt' : 20, 
                   'trente' : 30, 
                   'quarante' : 40,
                   'cinquante' : 50, 
                   'septante' : 70, 
                   'octante' : 80,
                   'nonante' : 90,
                  }
    
    def integer_parser (self, words = None) : 
        if words : 
            self.words = _set_words (words) 
        total_value = 0
        while self.words : 
            value = self._integer_parser_lt1000 ()
            if value and not self._end_of_parsed_integer () : 
                if self.words[0] in self.POWERS : 
                    total_value += value * (10 ** self.POWERS[self.words[0]]) 
                    self.words = self.words[1:]
                    if self._end_of_parsed_integer () : 
                        return total_value
                else : 
                    return total_value + value
            elif not self._end_of_parsed_integer () and \
            self.words[0] == 'mille' : 
                total_value += 1000
                self.words = self.words[1:]
                if not self._end_of_parsed_integer () : 
                    value = self._integer_parser_lt1000 () 
                    return total_value + value
                return total_value
            else : 
                if value :
                    total_value += value 
                return total_value
            
    def number_parser (self, words) :
        value = self.integer_parser(words)
        if self.words :
            if self.words[0] in ['virgule', 'point'] :
                self.words = self.words[1:]
                decimal = 0
                while True :
                    while self.words and self.words[0] == 'zero' :
                        decimal += 1
                        self.words = self.words[1:]
                    comp = self.integer_parser()
                    if comp :
                        decimal += natural_log(comp) + 1
                        value += comp / (10 ** decimal)
                    else :
                        break                    
        return value
                
    def _end_of_parsed_integer (self) : 
        return (not self.words) or self.words[0] == 'virgule' or self.words[0] == 'point'
    
    def _integer_parser_60_80 (self) : 
        if self.words[0] == 'soixante': 
            self.words = self.words[1:]
            if len (self.words) > 1 and self.words[0] == 'et' and self.words[1] in ['un', 'onze'] : 
                value = 60 + self.OTHER_NUMBERS[self.words[1]]
                self.words = self.words[2:]
                return value
            elif not self._end_of_parsed_integer() : 
                value = self._integer_parser_lt20 () 
                if value :
                    return value + 60
                return 60
        elif len (self.words) > 2 and self.words[0] == 'quatre' and self.words[1] == 'vingt' : 
            if self.words[2] in self.DIGITS : 
                value = 80 + self.DIGITS[self.words[2]]
                self.words = self.words[3:]
                return value
            elif self.words[2] in ['un', 'onze'] : 
                value = 80 + self.OTHER_NUMBERS[self.words[2]]
                self.words = self.words[3:]
                return value
            elif self.words[2] in self.NUMBERS : 
                value = 80 + self.NUMBERS[self.words[2]]
                self.words = self.words[3:]
                return value
            elif self.words[2] == 'dix' : 
                self.words = self.words[3:]
                if len (self.words) != 0 and self.words[0] in self.DIGITS : 
                    value = 90 + self.DIGITS[self.words[0]]
                    self.words = self.words[1:]
                    return value
                return 90
        return None
    
    def _integer_parser_lt100 (self) : 
        if self.words[0] in self.SAFE_DOZENS : 
            value = self.SAFE_DOZENS[self.words[0]] 
            self.words = self.words[1:]
            if not self._end_of_parsed_integer () : 
                if self.words[0] == 'et' : 
                    if len (self.words) > 1 and self.words[1] == 'un' : 
                        self.words = self.words[2:]
                        return value + 1
                elif self.words[0] in self.DIGITS : 
                    value += self.DIGITS[self.words[0]]
                    self.words = self.words[1:]
            return value
        elif self.words[0] == 'soixante' or (len (self.words) > 1 and self.words[0] == 'quatre' and self.words[1] == 'vingt') : 
            return self._integer_parser_60_80 () 
        return self._integer_parser_lt20 () 
        
    def _integer_parser_lt1000 (self) : 
        if self.words[0] == 'cent' : 
            self.words = self.words[1:]
            if self._end_of_parsed_integer () : 
                return 100
            value = self._integer_parser_lt100 () 
            if value : 
                return 100 + value
            return None
        elif len (self.words) > 1 and self.words[1] == 'cent' : 
            try : 
                value = 100 * self.DIGITS[self.words[0]]
                self.words = self.words[2:]
                if not self._end_of_parsed_integer () : 
                    new_value = self._integer_parser_lt100 () 
                    if new_value :
                        return value + new_value
                return value
            except Exception : 
                pass
        return self._integer_parser_lt100 () 
    
    def _integer_parser_lt20 (self) : 
        if self.words[0] in self.DIGITS : 
            value = self.DIGITS[self.words[0]]
            self.words = self.words [1:]
            return value
        if self.words[0] in self.OTHER_NUMBERS : 
            value = self.OTHER_NUMBERS[self.words[0]]
            self.words = self.words [1:]
            return value
        if self.words[0] in self.NUMBERS : 
            value = self.NUMBERS[self.words[0]]
            self.words = self.words [1:]
            return value
        if self.words[0] == 'dix' : 
            self.words = self.words [1:]
            value = 10
            if not self._end_of_parsed_integer () : 
                if self.words[0] in self.DIGITS : 
                    value += self.DIGITS[self.words[0]]
                    self.words = self.words [1:]
            return value
        return None
        
    def __call__ (self, words) : 
        return self.number_parser (words) 
    
#==============================================================================
#     
#==============================================================================
    
if __name__ == "__main__" : 
    
    parser = NumberParser () 
    assert parser(['un']) == 1
    assert parser(['huit']) == 8
    assert parser(['dix']) == 10 
    assert parser(['onze']) == 11
    assert parser(['quatorze']) == 14
    assert parser(['dix','sept']) == 17
    assert parser(['vingt','et', 'un']) == 21 
    assert parser(['trente', 'quatre']) == 34
    assert parser(['quarante', 'huit']) == 48 
    assert parser(['cinquante']) == 50 
    assert parser(['soixante','sept']) == 67
    assert parser(['soixante','et', 'onze']) == 71 
    assert parser(['soixante','quatorze']) == 74
    assert parser(['soixante','dix', 'huit']) == 78 
    assert parser(['quatre','vingt', 'huit']) == 88
    assert parser(['quatre', 'vingt', 'douze']) == 92 
    assert parser(['quatre', 'vingt', 'dix', 'huit']) == 98
    assert parser(['nonante', 'neuf']) == 99
    assert parser(['cent']) == 100
    assert parser('trois cent quatre') == 304
    assert parser(['huit','cent']) == 800
    assert parser('huit cent douze') == 812
    assert parser(['mille']) == 1000
    assert parser(['mille', 'deux']) == 1002
    assert parser(['mille', 'deux', 'cent']) == 1200 
    assert parser(['mille', 'deux', 'cent', 'deux']) == 1202
    assert parser(['deux', 'mille', 'deux', 'cent', 'deux']) == 2202 
    assert parser(['douze', 'mille', 'deux', 'cent', 'deux']) == 12202
    assert parser('sept cent million') == 700000000
    assert parser('onze milliard sept cent million deux cent mille trois cent quatre') == 11700200304
    assert parser('trois cent quatorze trillion onze milliard sept cent million deux cent mille trois cent quatre') == 314000000011700200304
    assert parser ('trois virgule quarante deux quarante deux') == 3.4242
    assert parser ('trente trois point zero zero huit cent quatre') == 33.00804
    assert parser ('cent cinquante et un virgule quarante six') == 151.46
    assert parser ('deux cent soixante et un mille six cent quarante trois virgule huit million quatre cent quatre vingt trois mille cinq cent douze') == 261643.8483512