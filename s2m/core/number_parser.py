from s2m.core.utils import natural_log, _set_words, reverse_dict, dec
    
class NumberParser: 

    DIGITS = {'deux' : 2, 
            'trois' : 3, 
            'quatre' : 4, 
            'cinq' : 5,
            'six' : 6, 
            'sept' : 7, 
            'huit' : 8, 
            'neuf' : 9,
            }

    DIGITS_REVERSE = reverse_dict(DIGITS)
    
    NUMBERS = {'douze' : 12, 
               'treize' : 13, 
               'quatorze' : 14,
               'quinze' : 15, 
               'seize' : 16,
               }

    NUMBERS_REVERSE = reverse_dict(NUMBERS)
    
    # Verifier l'utilité de la distinction others / other_numbers
    OTHER_NUMBERS = {'zéro' : 0,
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
               'quadrillon' : 24, 
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
               'décillion' : 60, 
               'décilliard' : 63,
               }

    POWERS_REVERSE = reverse_dict(POWERS)
    
    SAFE_DOZENS = {'vingt' : 20, 
                   'trente' : 30, 
                   'quarante' : 40,
                   'cinquante' : 50, 
                   'septante' : 70, 
                   'octante' : 80,
                   'nonante' : 90,
                  }

    DOZENS_REVERSE = {20 : 'vingt',
                      30 : 'trente',
                      40 : 'quarante',
                      50 : 'cinquante',
                      60 : 'soixante',
                      70 : 'soixante',
                      80 : 'quatre vingt',
                      90 : 'quatre vingt'}
    
    COMMA = ['virgule', 'point']

    NUMBER_WORDS = list(DIGITS.keys()) \
                   + list(NUMBERS.keys()) \
                   + list(OTHER_NUMBERS.keys()) \
                   + OTHERS \
                   + list(POWERS.keys()) \
                   + list(SAFE_DOZENS.keys()) \
                   + COMMA \
                   + ['et']
    
    def __getattr__(self, p):
        if p == 'words':
            return self.words or []

    def _integer_parser(self): 
        total_value = 0
        while self.words: 
            value = self._integer_parser_lt1000()
            if value is not None and not self._end_of_parsed_integer(): 
                if self.words[0] in self.POWERS: 
                    total_value += value * (10 ** self.POWERS[self.words[0]]) 
                    del self.words[0]
                    if self._end_of_parsed_integer(): 
                        return total_value
                else : 
                    return total_value + value
            elif not self._end_of_parsed_integer() and \
                 self.words[0] == 'mille': 
                total_value += 1000
                self.words = self.words[1:]
                if not self._end_of_parsed_integer(): 
                    value = self._integer_parser_lt1000() 
                    return total_value + value
                return total_value
            elif value is not None:
                return total_value + value
            else:
                return None
            
    def number_parser(self, words, strict=False):
        self.words = _set_words(words)
        value = self._integer_parser()
        if value is None:
            return None
        if self.words:
            if self.words[0] in self.COMMA:
                del self.words[0]
                decimal = 0
                while True:
                    while self.words and self.words[0] == 'zero':
                        decimal += 1
                        del self.words[0]
                    comp = self._integer_parser()
                    if comp:
                        decimal += natural_log(comp) + 1
                        value += float(comp) / (10 ** decimal)
                    else:
                        break
        if not (strict and self.words):
            return value
        else:
            raise ValueError('[strict=True] String %r does not represent any valid number.' % ''.join(words))
                
    def _end_of_parsed_integer(self): 
        return (not self.words) or self.words[0] in self.COMMA
    
    def _integer_parser_60_80 (self): 
        if self.words[0] == 'soixante': 
            self.words = self.words[1:]
            if len (self.words) > 1 and self.words[0] == 'et' and self.words[1] in ['un', 'onze']: 
                value = 60 + self.OTHER_NUMBERS[self.words[1]]
                del self.words[0]
                del self.words[0]
                return value
            elif not self._end_of_parsed_integer(): 
                value = self._integer_parser_lt20() 
                if value:
                    return value + 60
            else:
                return 60
        elif len(self.words) > 1 and self.words[0] == 'quatre' and self.words[1] == 'vingt':
            self.words = self.words[2:]
            if self._end_of_parsed_integer():
                return 80
            elif self.words[0] in self.DIGITS: 
                value = 80 + self.DIGITS[self.words[0]]
                self.words = self.words[1:]
                return value
            elif self.words[0] in ['un', 'onze']: 
                value = 80 + self.OTHER_NUMBERS[self.words[0]]
                self.words = self.words[1:]
                return value
            elif self.words[0] in self.NUMBERS: 
                value = 80 + self.NUMBERS[self.words[0]]
                self.words = self.words[1:]
                return value
            elif self.words[0] == 'dix': 
                self.words = self.words[1:]
                if len (self.words) != 0 and self.words[0] in self.DIGITS: 
                    value = 90 + self.DIGITS[self.words[0]]
                    del self.words[0]
                    return value
                return 90
        return None
    
    def _integer_parser_lt100(self): 
        if self.words[0] in self.SAFE_DOZENS: 
            value = self.SAFE_DOZENS[self.words[0]] 
            del self.words[0]
            if not self._end_of_parsed_integer(): 
                if self.words[0] == 'et': 
                    if len (self.words) > 1 and self.words[1] == 'un': 
                        del self.words[0]
                        del self.words[0]
                        return value + 1
                elif self.words[0] in self.DIGITS: 
                    value += self.DIGITS[self.words[0]]
                    del self.words[0]
            return value
        elif self.words[0] == 'soixante' or \
                (len (self.words) > 1 \
                 and self.words[0] == 'quatre' \
                 and self.words[1] == 'vingt'): 
            return self._integer_parser_60_80() 
        return self._integer_parser_lt20() 
        
    def _integer_parser_lt1000(self): 
        if self.words[0] == 'cent': 
            self.words = self.words[1:]
            if self._end_of_parsed_integer(): 
                return 100
            value = self._integer_parser_lt100() 
            if value: 
                return 100 + value
            return None
        elif len(self.words) > 1 and self.words[1] == 'cent': 
            try : 
                value = 100 * self.DIGITS[self.words[0]]
                del self.words[0]
                del self.words[0]
                if not self._end_of_parsed_integer(): 
                    new_value = self._integer_parser_lt100() 
                    if new_value:
                        return value + new_value
                return value
            except Exception: 
                pass
        return self._integer_parser_lt100() 
    
    def _integer_parser_lt20(self): 
        if self.words[0] in self.DIGITS: 
            value = self.DIGITS[self.words[0]]
            del self.words[0]
            return value
        if self.words[0] in self.OTHER_NUMBERS: 
            value = self.OTHER_NUMBERS[self.words[0]]
            del self.words[0]
            return value
        if self.words[0] in self.NUMBERS: 
            value = self.NUMBERS[self.words[0]]
            del self.words[0]
            return value
        if self.words[0] == 'dix': 
            del self.words[0]
            value = 10
            if not self._end_of_parsed_integer(): 
                if self.words[0] in self.DIGITS: 
                    value += self.DIGITS[self.words[0]]
                    del self.words[0]
            return value
        return None

    def _transcribe_lt99(self, n):
        l = []
        m = n // 10
        n %= dec(10)
        if m in [1, 7, 9]:
            if m != 1:
                l.append(self.DOZENS_REVERSE[10*m])
            if n == 0:
                l.append('dix')
            elif n == 1:
                if m == 7:
                    l.append('et')
                l.append('onze')
            elif n < 7:
                l.append(self.NUMBERS_REVERSE[10+n])
            else:
                l.append('dix')
                l.append(self.DIGITS_REVERSE[n])
        else:
            if m > 1:
                l.append(self.DOZENS_REVERSE[10*m])
            if n == 1:
                if m not in [0, 8]:
                    l.append('et')
                l.append('un')
            else:
                l.append(self.DIGITS_REVERSE[n])
        return ' '.join(l)
    
    def _transcribe_lt999(self, n):
        if n == 0:
            return ''
        l = []
        m = n // dec(100)
        if m == 1:
            l.append('cent')
        elif m > 1:
            l.append(self.DIGITS_REVERSE[m])
            l.append('cent')
        n %= dec(100)
        t = self._transcribe_lt99(n)
        if t:
            l.append(t)
        return ' '.join(l)
        
    def transcribe(self, n):
        l = []
        n = dec(n)
        if n < 1:
            l.append('zéro')
        else:
            i = natural_log(n)
            j = i // 3
            for k in range(j, 0, -1):
                m = n // 10**(3*k)
                p = self._transcribe_lt999(m)
                if p:
                    l.append(p)
                    l.append(self.POWERS_REVERSE[3*k])
                n %= dec(10**(3*k))
            m = int(n)
            if m > 0:
                l.append(self._transcribe_lt999(m))
                n %= dec(1)
        if n > 0:
            l.append('virgule')
            while n != 0:
                n *= dec(10)
                m = int(n)
                if m == 0:
                    l.append('zéro')
                elif m == 1:
                    l.append('un')
                else:
                    l.append(self.DIGITS_REVERSE[m])
                n %= dec(1)
        return ' '.join(l)            
                        
    def __call__(self, words, strict=False):
        return self.number_parser(words, strict=strict) 
    
#==============================================================================
#     
#==============================================================================
    
if __name__ == "__main__" : 
    
    parser = NumberParser() 
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
