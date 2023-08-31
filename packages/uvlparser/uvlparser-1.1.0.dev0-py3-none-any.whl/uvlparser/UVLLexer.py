# Generated from uvlparser/UVL.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


from antlr_denter.DenterHelper import DenterHelper
from uvlparser.UVLParser import UVLParser


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\34")
        buf.write("\u011c\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\4\3\4\3\5\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3")
        buf.write("\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\n\3\n")
        buf.write("\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r")
        buf.write("\3\16\3\16\3\17\3\17\3\20\3\20\3\21\3\21\3\21\3\21\3\22")
        buf.write("\3\22\3\22\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\25\3\25")
        buf.write("\3\25\7\25\u0095\n\25\f\25\16\25\u0098\13\25\5\25\u009a")
        buf.write("\n\25\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\5\26\u00bf\n\26\3\26\3\26\5\26\u00c3\n")
        buf.write("\26\3\26\5\26\u00c6\n\26\3\27\6\27\u00c9\n\27\r\27\16")
        buf.write("\27\u00ca\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30")
        buf.write("\5\30\u00d6\n\30\3\31\5\31\u00d9\n\31\3\31\3\31\3\31\7")
        buf.write("\31\u00de\n\31\f\31\16\31\u00e1\13\31\5\31\u00e3\n\31")
        buf.write("\3\31\5\31\u00e6\n\31\3\31\3\31\5\31\u00ea\n\31\3\31\5")
        buf.write("\31\u00ed\n\31\3\32\3\32\3\32\3\32\3\32\5\32\u00f4\n\32")
        buf.write("\3\32\5\32\u00f7\n\32\7\32\u00f9\n\32\f\32\16\32\u00fc")
        buf.write("\13\32\3\32\3\32\3\33\5\33\u0101\n\33\3\33\3\33\7\33\u0105")
        buf.write("\n\33\f\33\16\33\u0108\13\33\3\33\5\33\u010b\n\33\3\33")
        buf.write("\3\33\7\33\u010f\n\33\f\33\16\33\u0112\13\33\5\33\u0114")
        buf.write("\n\33\3\34\6\34\u0117\n\34\r\34\16\34\u0118\3\34\3\34")
        buf.write("\2\2\35\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f")
        buf.write("\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\2+\26")
        buf.write("-\27/\30\61\31\63\32\65\33\67\34\3\2\t\3\2\63;\3\2\62")
        buf.write(";\7\2//\62;C\\aac|\4\2--//\4\2GGgg\4\2--\62;\3\2\"\"\2")
        buf.write("\u0135\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2")
        buf.write("\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2")
        buf.write("\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33")
        buf.write("\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2")
        buf.write("\2\2%\3\2\2\2\2\'\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2")
        buf.write("\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2")
        buf.write("\2\39\3\2\2\2\5C\3\2\2\2\7L\3\2\2\2\tN\3\2\2\2\13Q\3\2")
        buf.write("\2\2\rS\3\2\2\2\17U\3\2\2\2\21W\3\2\2\2\23c\3\2\2\2\25")
        buf.write("e\3\2\2\2\27g\3\2\2\2\31o\3\2\2\2\33r\3\2\2\2\35t\3\2")
        buf.write("\2\2\37v\3\2\2\2!x\3\2\2\2#|\3\2\2\2%\177\3\2\2\2\'\u0088")
        buf.write("\3\2\2\2)\u0099\3\2\2\2+\u00c5\3\2\2\2-\u00c8\3\2\2\2")
        buf.write("/\u00d5\3\2\2\2\61\u00d8\3\2\2\2\63\u00ee\3\2\2\2\65\u0113")
        buf.write("\3\2\2\2\67\u0116\3\2\2\29:\7p\2\2:;\7c\2\2;<\7o\2\2<")
        buf.write("=\7g\2\2=>\7u\2\2>?\7r\2\2?@\7c\2\2@A\7e\2\2AB\7g\2\2")
        buf.write("B\4\3\2\2\2CD\7h\2\2DE\7g\2\2EF\7c\2\2FG\7v\2\2GH\7w\2")
        buf.write("\2HI\7t\2\2IJ\7g\2\2JK\7u\2\2K\6\3\2\2\2LM\7\60\2\2M\b")
        buf.write("\3\2\2\2NO\7}\2\2OP\7\177\2\2P\n\3\2\2\2QR\7}\2\2R\f\3")
        buf.write("\2\2\2ST\7.\2\2T\16\3\2\2\2UV\7\177\2\2V\20\3\2\2\2WX")
        buf.write("\7e\2\2XY\7q\2\2YZ\7p\2\2Z[\7u\2\2[\\\7v\2\2\\]\7t\2\2")
        buf.write("]^\7c\2\2^_\7k\2\2_`\7p\2\2`a\7v\2\2ab\7u\2\2b\22\3\2")
        buf.write("\2\2cd\7*\2\2d\24\3\2\2\2ef\7+\2\2f\26\3\2\2\2gh\7k\2")
        buf.write("\2hi\7o\2\2ij\7r\2\2jk\7q\2\2kl\7t\2\2lm\7v\2\2mn\7u\2")
        buf.write("\2n\30\3\2\2\2op\7c\2\2pq\7u\2\2q\32\3\2\2\2rs\7#\2\2")
        buf.write("s\34\3\2\2\2tu\7(\2\2u\36\3\2\2\2vw\7~\2\2w \3\2\2\2x")
        buf.write("y\7>\2\2yz\7?\2\2z{\7@\2\2{\"\3\2\2\2|}\7?\2\2}~\7@\2")
        buf.write("\2~$\3\2\2\2\177\u0080\7t\2\2\u0080\u0081\7g\2\2\u0081")
        buf.write("\u0082\7s\2\2\u0082\u0083\7w\2\2\u0083\u0084\7k\2\2\u0084")
        buf.write("\u0085\7t\2\2\u0085\u0086\7g\2\2\u0086\u0087\7u\2\2\u0087")
        buf.write("&\3\2\2\2\u0088\u0089\7g\2\2\u0089\u008a\7z\2\2\u008a")
        buf.write("\u008b\7e\2\2\u008b\u008c\7n\2\2\u008c\u008d\7w\2\2\u008d")
        buf.write("\u008e\7f\2\2\u008e\u008f\7g\2\2\u008f\u0090\7u\2\2\u0090")
        buf.write("(\3\2\2\2\u0091\u009a\7\62\2\2\u0092\u0096\t\2\2\2\u0093")
        buf.write("\u0095\t\3\2\2\u0094\u0093\3\2\2\2\u0095\u0098\3\2\2\2")
        buf.write("\u0096\u0094\3\2\2\2\u0096\u0097\3\2\2\2\u0097\u009a\3")
        buf.write("\2\2\2\u0098\u0096\3\2\2\2\u0099\u0091\3\2\2\2\u0099\u0092")
        buf.write("\3\2\2\2\u009a*\3\2\2\2\u009b\u009c\7c\2\2\u009c\u009d")
        buf.write("\7n\2\2\u009d\u009e\7v\2\2\u009e\u009f\7g\2\2\u009f\u00a0")
        buf.write("\7t\2\2\u00a0\u00a1\7p\2\2\u00a1\u00a2\7c\2\2\u00a2\u00a3")
        buf.write("\7v\2\2\u00a3\u00a4\7k\2\2\u00a4\u00a5\7x\2\2\u00a5\u00c6")
        buf.write("\7g\2\2\u00a6\u00a7\7q\2\2\u00a7\u00c6\7t\2\2\u00a8\u00a9")
        buf.write("\7q\2\2\u00a9\u00aa\7r\2\2\u00aa\u00ab\7v\2\2\u00ab\u00ac")
        buf.write("\7k\2\2\u00ac\u00ad\7q\2\2\u00ad\u00ae\7p\2\2\u00ae\u00af")
        buf.write("\7c\2\2\u00af\u00c6\7n\2\2\u00b0\u00b1\7o\2\2\u00b1\u00b2")
        buf.write("\7c\2\2\u00b2\u00b3\7p\2\2\u00b3\u00b4\7f\2\2\u00b4\u00b5")
        buf.write("\7c\2\2\u00b5\u00b6\7v\2\2\u00b6\u00b7\7q\2\2\u00b7\u00b8")
        buf.write("\7t\2\2\u00b8\u00c6\7{\2\2\u00b9\u00be\7]\2\2\u00ba\u00bb")
        buf.write("\5)\25\2\u00bb\u00bc\7\60\2\2\u00bc\u00bd\7\60\2\2\u00bd")
        buf.write("\u00bf\3\2\2\2\u00be\u00ba\3\2\2\2\u00be\u00bf\3\2\2\2")
        buf.write("\u00bf\u00c2\3\2\2\2\u00c0\u00c3\5)\25\2\u00c1\u00c3\7")
        buf.write(",\2\2\u00c2\u00c0\3\2\2\2\u00c2\u00c1\3\2\2\2\u00c3\u00c4")
        buf.write("\3\2\2\2\u00c4\u00c6\7_\2\2\u00c5\u009b\3\2\2\2\u00c5")
        buf.write("\u00a6\3\2\2\2\u00c5\u00a8\3\2\2\2\u00c5\u00b0\3\2\2\2")
        buf.write("\u00c5\u00b9\3\2\2\2\u00c6,\3\2\2\2\u00c7\u00c9\t\4\2")
        buf.write("\2\u00c8\u00c7\3\2\2\2\u00c9\u00ca\3\2\2\2\u00ca\u00c8")
        buf.write("\3\2\2\2\u00ca\u00cb\3\2\2\2\u00cb.\3\2\2\2\u00cc\u00cd")
        buf.write("\7v\2\2\u00cd\u00ce\7t\2\2\u00ce\u00cf\7w\2\2\u00cf\u00d6")
        buf.write("\7g\2\2\u00d0\u00d1\7h\2\2\u00d1\u00d2\7c\2\2\u00d2\u00d3")
        buf.write("\7n\2\2\u00d3\u00d4\7u\2\2\u00d4\u00d6\7g\2\2\u00d5\u00cc")
        buf.write("\3\2\2\2\u00d5\u00d0\3\2\2\2\u00d6\60\3\2\2\2\u00d7\u00d9")
        buf.write("\t\5\2\2\u00d8\u00d7\3\2\2\2\u00d8\u00d9\3\2\2\2\u00d9")
        buf.write("\u00e2\3\2\2\2\u00da\u00e3\7\62\2\2\u00db\u00df\t\2\2")
        buf.write("\2\u00dc\u00de\t\3\2\2\u00dd\u00dc\3\2\2\2\u00de\u00e1")
        buf.write("\3\2\2\2\u00df\u00dd\3\2\2\2\u00df\u00e0\3\2\2\2\u00e0")
        buf.write("\u00e3\3\2\2\2\u00e1\u00df\3\2\2\2\u00e2\u00da\3\2\2\2")
        buf.write("\u00e2\u00db\3\2\2\2\u00e3\u00e5\3\2\2\2\u00e4\u00e6\7")
        buf.write("\60\2\2\u00e5\u00e4\3\2\2\2\u00e5\u00e6\3\2\2\2\u00e6")
        buf.write("\u00ec\3\2\2\2\u00e7\u00e9\t\6\2\2\u00e8\u00ea\t\5\2\2")
        buf.write("\u00e9\u00e8\3\2\2\2\u00e9\u00ea\3\2\2\2\u00ea\u00eb\3")
        buf.write("\2\2\2\u00eb\u00ed\t\7\2\2\u00ec\u00e7\3\2\2\2\u00ec\u00ed")
        buf.write("\3\2\2\2\u00ed\62\3\2\2\2\u00ee\u00fa\7]\2\2\u00ef\u00f4")
        buf.write("\5/\30\2\u00f0\u00f4\5\61\31\2\u00f1\u00f4\5-\27\2\u00f2")
        buf.write("\u00f4\5\63\32\2\u00f3\u00ef\3\2\2\2\u00f3\u00f0\3\2\2")
        buf.write("\2\u00f3\u00f1\3\2\2\2\u00f3\u00f2\3\2\2\2\u00f4\u00f6")
        buf.write("\3\2\2\2\u00f5\u00f7\7.\2\2\u00f6\u00f5\3\2\2\2\u00f6")
        buf.write("\u00f7\3\2\2\2\u00f7\u00f9\3\2\2\2\u00f8\u00f3\3\2\2\2")
        buf.write("\u00f9\u00fc\3\2\2\2\u00fa\u00f8\3\2\2\2\u00fa\u00fb\3")
        buf.write("\2\2\2\u00fb\u00fd\3\2\2\2\u00fc\u00fa\3\2\2\2\u00fd\u00fe")
        buf.write("\7_\2\2\u00fe\64\3\2\2\2\u00ff\u0101\7\17\2\2\u0100\u00ff")
        buf.write("\3\2\2\2\u0100\u0101\3\2\2\2\u0101\u0102\3\2\2\2\u0102")
        buf.write("\u0106\7\f\2\2\u0103\u0105\7\"\2\2\u0104\u0103\3\2\2\2")
        buf.write("\u0105\u0108\3\2\2\2\u0106\u0104\3\2\2\2\u0106\u0107\3")
        buf.write("\2\2\2\u0107\u0114\3\2\2\2\u0108\u0106\3\2\2\2\u0109\u010b")
        buf.write("\7\17\2\2\u010a\u0109\3\2\2\2\u010a\u010b\3\2\2\2\u010b")
        buf.write("\u010c\3\2\2\2\u010c\u0110\7\f\2\2\u010d\u010f\7\13\2")
        buf.write("\2\u010e\u010d\3\2\2\2\u010f\u0112\3\2\2\2\u0110\u010e")
        buf.write("\3\2\2\2\u0110\u0111\3\2\2\2\u0111\u0114\3\2\2\2\u0112")
        buf.write("\u0110\3\2\2\2\u0113\u0100\3\2\2\2\u0113\u010a\3\2\2\2")
        buf.write("\u0114\66\3\2\2\2\u0115\u0117\t\b\2\2\u0116\u0115\3\2")
        buf.write("\2\2\u0117\u0118\3\2\2\2\u0118\u0116\3\2\2\2\u0118\u0119")
        buf.write("\3\2\2\2\u0119\u011a\3\2\2\2\u011a\u011b\b\34\2\2\u011b")
        buf.write("8\3\2\2\2\31\2\u0096\u0099\u00be\u00c2\u00c5\u00ca\u00d5")
        buf.write("\u00d8\u00df\u00e2\u00e5\u00e9\u00ec\u00f3\u00f6\u00fa")
        buf.write("\u0100\u0106\u010a\u0110\u0113\u0118\3\b\2\2")
        return buf.getvalue()


class UVLLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    NOT = 13
    AND = 14
    OR = 15
    EQUIVALENCE = 16
    IMPLICATION = 17
    REQUIRES = 18
    EXCLUDES = 19
    RELATION_WORD = 20
    WORD = 21
    BOOLEAN = 22
    NUMBER = 23
    VECTOR = 24
    NL = 25
    WS = 26

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'namespace'", "'features'", "'.'", "'{}'", "'{'", "','", "'}'", 
            "'constraints'", "'('", "')'", "'imports'", "'as'", "'!'", "'&'", 
            "'|'", "'<=>'", "'=>'", "'requires'", "'excludes'" ]

    symbolicNames = [ "<INVALID>",
            "NOT", "AND", "OR", "EQUIVALENCE", "IMPLICATION", "REQUIRES", 
            "EXCLUDES", "RELATION_WORD", "WORD", "BOOLEAN", "NUMBER", "VECTOR", 
            "NL", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "NOT", "AND", 
                  "OR", "EQUIVALENCE", "IMPLICATION", "REQUIRES", "EXCLUDES", 
                  "INT", "RELATION_WORD", "WORD", "BOOLEAN", "NUMBER", "VECTOR", 
                  "NL", "WS" ]

    grammarFileName = "UVL.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    class UVLDenter(DenterHelper):
        def __init__(self, lexer, nl_token, indent_token, dedent_token, ignore_eof):
            super().__init__(nl_token, indent_token, dedent_token, ignore_eof)
            self.lexer: UVLLexer = lexer

        def pull_token(self):
            return super(UVLLexer, self.lexer).nextToken()

    denter = None

    def nextToken(self):
        if not self.denter:
            self.denter = self.UVLDenter(self, self.NL, UVLParser.INDENT, UVLParser.DEDENT, True)
        return self.denter.next_token()



