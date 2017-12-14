from s2m.core.number_parser import NumberParser
from s2m.core.parser import Parser
from s2m.core.S2MParser import S2MParser

#Tests du number parser pour tester la lecture de nombres en lettres
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
assert parser('trois virgule quarante deux quarante deux') == 3.4242
assert parser('trente trois point zero zero huit cent quatre') == 33.00804
assert parser('cent cinquante et un virgule quarante six') == 151.46
assert parser('deux cent soixante et un mille six cent quarante trois virgule huit million quatre cent quatre vingt trois mille cinq cent douze') == 261643.8483512

#Tests de parser d'opérations binaires
parser = S2MParser()
assert "2 + 2" in parser.parse("deux plus deux")
assert "2 * 2" in parser.parse("deux fois deux")
