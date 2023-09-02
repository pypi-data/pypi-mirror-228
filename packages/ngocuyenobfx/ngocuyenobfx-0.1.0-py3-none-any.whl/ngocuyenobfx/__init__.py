"""

uyenobf.

Data Obf By Ngoc Uyen

"""

__version__ = "0.4"
__author__ = 'huynhngocuyen'
import ast
from io import TextIOWrapper
from uyenobf.transformers import TryCatchTransformer
from uyenobf.transformers import TryNormalizerTransformer
from uyenobf.transformers import MemoryTransformer
from uyenobf.transformers import InOutlineTransformer
from uyenobf.transformers import ControlFlowTransformer
from uyenobf.transformers import MBAExprTransformer
from uyenobf.transformers import OpaqueTransformer
from uyenobf.transformers import RenamerTransformer
from uyenobf.transformers import StringTransformer
from uyenobf.logger import Logger

class ObfuscatorSettings():
    def __init__(self):
        self.transformers = []
        self.logger_enabled = True
    def addTransformer(self, transformer):
        self.transformers.append(transformer)
    def setLoggerEnabled(self, value):
        self.logger_enabled = value
    
    def MBAExpression(self, wrapping_value):
        """ 
        
        MBA Expression Transformer
        
        @param wrapping_value - Enable num obfuscating
        
        """
        self.addTransformer(MBAExprTransformer.MBAExprTransformer(wrapping_value))
    def InOutline(self):
        """ 
        
        In Outline Transformer
        
        """
        self.addTransformer(InOutlineTransformer.InOutlineTransformer())
    def ControlFlow(self):
        """ 
        
        Control Flow Transformer
        
        """
        self.addTransformer(ControlFlowTransformer.ControlFlowTransformer())
    def TryCatch(self, safe_mode: bool, iterations: int):
        """ 
        
        Try Catch Transformer
        
        @param safe_mode - Ignores try-catch for return
        
        @param iterations - Iterations (Default - 1; Medium - 3; Hard - 5)
        
        """
        self.addTransformer(TryCatchTransformer.TryCatchTransformer(safe_mode, iterations))
    def TryNormalizer(self, iterations: int):
        """ 
        
        Try Normalizer Transformer
        
        @param iterations - Iterations (Default - 5)
        
        """
        self.addTransformer(TryNormalizerTransformer.TryNormalizierTransformer(iterations))
    def Opaque(self, iterations: int):
        """ 
        
        Opaque Transformer
        
        """
        self.addTransformer(OpaqueTransformer.OpaqueTransformer(iterations))
    def Renamer(self, mode: int):
        """ 
        
        Renamer Transformer
        
        """
        self.addTransformer(RenamerTransformer.RenamerTransformer(mode))
    def ObscureString(self):
        """ 
        
        Renamer Transformer
        
        """
        self.addTransformer(StringTransformer.StringTransformer())

class Obfuscator:
    def obfuscate(input_file: TextIOWrapper, out_file: TextIOWrapper, settings: ObfuscatorSettings):
        Logger.init(settings.logger_enabled)
        Logger.logger.name = __class__.__name__
        
        Logger.logger.info(f"Obfuscating \"{input_file.name}\" ")
        
        tree = ast.parse(input_file.read())
        
        for transformer in settings.transformers:
            transformer.setTree(tree)
            Logger.logger.name = transformer.__class__.__name__
            
            tree = transformer.proceed()
        
        out_file.write(ast.unparse(tree))