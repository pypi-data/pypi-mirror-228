from abc import *
import ast
from typing import List

class DocTemplate(ABC):
    # Ces constantes peuvent être utilisées dans les classes d'implémention
    NEW_LINE = "\n"
    DOCSTRING_SYMBOL = '"""'
    
    # Les mots utilisés dans le template par défault
    TODO_LABEL = "" #"__à compléter__"
    
    SUMMARY_LABEL = "à_remplacer_par_ce_que_fait_la_fonction"
    PARAM_LABEL = "Paramètres :"
    # nouveauté portail MI : on parle vraiment de précondition !
    CU_LABEL = "Précondition : "
    DOCTEST_LABEL = "Exemple(s) :\n$$$ "
    
    def _format_params(self, params) -> str:
        """
        Args:
            params (List): It's a list of the arguments.

        Returns:
            str: Returns the parameter representation section of a node in a docstring. 
        """
        if params is None:
            return ""
        args_to_exclude = ["self", "cls"]
        label = self.PARAM_LABEL + self.NEW_LINE
        format_params = ""
        for p in params:
            arg_type = ast.unparse(p.annotation) if p.annotation else ""     
            arg_name = p.arg 
            if arg_name not in args_to_exclude: 
                format_params += "- %s (%s) : %s\n" %(arg_name, arg_type, self.TODO_LABEL)
        return label + format_params
    
    @abstractmethod
    def get_parameters(self, node:ast.AST) -> List:
        """
        Get the paramters of a given node.
        
        Args:
            node (ast.AST): An AST node. 

        Returns:
            List: Returns a List of arguments of the given node.
        """
        for node in node.body:
            if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                # Trouver les paramètres de la méthode __init__
                return node.args.args
        return []
    
    @abstractmethod
    def _format_general_summary(self) -> str:
        """
        Returns:
            str: Returns a label which will indicate to write a summary of the function.
        """
        pass
    
    @abstractmethod
    def _format_usage_constraints(self) -> str:
        """
        Returns:
            str: Returns the usage constraints representation section in a docstring.
        """
        pass
    
    @abstractmethod
    def _format_return_value(self) -> str:
        """
        Returns:
            str: Returns the return value representation section in a docstring.
        """
        pass
    
    @abstractmethod
    def _format_test_examples(self) -> str:
        """
        Returns:
            str: Returns the test examples representation section in a docstring.
        """
        pass
    
    @abstractmethod
    def get_template(self, node:ast.AST=None) -> str:
        """Build the complete docstring template. 
        This method must invoke the above abstract methods.
        
        Args:
            node (ast.AST): The AST node in which the dosctring will be generated.

        Returns:
            str: Returns the template representation. 
        """
        pass  
    
    @abstractmethod
    def get_id_signature(self) -> str: 
        pass      
    
class DocFunctionTemplate(DocTemplate):
    '''Modifié pour coller au cours de PROG, portail MI, avec volonté
    d'alléger les docstring au max : uniquement la première phrase, la
    precond et les tests (les étudiant·es étant obligés d'indiquer des
    annotations de type).

    '''
    RETURN_LABEL = "Valeur de retour " 
    RETURN_TYPE_LABEL = "(%s) :" #"__type de retour ?__ (%s)%s"
    
    def get_parameters(self, node:ast.AST):
        """
        Get the paramters of a given node.
        
        Args:
            node (ast.AST): An AST node. Must be an ast.FunctionDef or ast.AsyncFunctionDef

        Returns:
            List: Returns a List of arguments of the given node.
        """
        if isinstance(node, ast.FunctionDef):
            return node.args.args
        return []

    def _format_general_summary(self):
        return self.SUMMARY_LABEL + self.NEW_LINE
    
    def _format_usage_constraints(self):
        return self.CU_LABEL + self.TODO_LABEL + self.NEW_LINE   

    def _format_return_value(self, node: ast):
        return_type = ast.unparse(node.returns) if node.returns else ""
        return_descr = self.RETURN_TYPE_LABEL % return_type + self.NEW_LINE
        return self.RETURN_LABEL + return_descr
    
    def _format_test_examples(self):
        label = self.DOCTEST_LABEL + self.NEW_LINE
        todo = self.TODO_LABEL + self.NEW_LINE
        return label + todo
        
    def get_template(self, node: ast.AST):
        '''Les commentaires indiquent les allègements pour le passage SESI ->
        MI.
        '''
        return (
            self.DOCSTRING_SYMBOL + 
            self._format_general_summary() + self.NEW_LINE + 
            # self._format_params(self.get_parameters(node))  + 
            # self._format_return_value(node) + 
            self._format_usage_constraints() +
            self._format_test_examples() + 
            self.DOCSTRING_SYMBOL + self.NEW_LINE
        )
    
    def get_id_signature(self): 
        return "def" 

class DocClassTemplate(DocTemplate): 
    def _format_general_summary(self):
        return self.SUMMARY_LABEL + self.NEW_LINE
    
    def get_parameters(self, node):
        # Parcourir les définitions de méthodes dans la classe
        for sub_node in node.body:
            if isinstance(sub_node, ast.FunctionDef) and sub_node.name == "__init__":
                # Trouver les paramètres de la méthode __init__
                return sub_node.args.args
        return []
     
    def _format_usage_constraints(self):
        return (self.CU_LABEL +
                self.TODO_LABEL +
                self.NEW_LINE 
            )  

    def _format_return_value(self):
        return ""
    
    def _format_test_examples(self):
        label = self.DOCTEST_LABEL + self.NEW_LINE
        todo = self.TODO_LABEL + self.NEW_LINE
        return label + todo
            
    def get_template(self, node):
        return self.DOCSTRING_SYMBOL + \
               self._format_params(self.get_parameters(node)) + \
               self._format_general_summary() + self.NEW_LINE + \
               self._format_usage_constraints() + \
               self._format_test_examples() + \
               self.DOCSTRING_SYMBOL + self.NEW_LINE

    def get_id_signature(self): 
        return "class" 

class DocTemplateFactory:            
    @staticmethod
    def create_template(type:str):
        return DocTemplateFactory.__search_type(type)
    
    @staticmethod
    def __docTemplate_subclasses(cls=DocTemplate):
        return set(cls.__subclasses__()) \
               .union([s for c in cls.__subclasses__() \
                            for s in DocTemplateFactory.__docTemplate_subclasses(c)])
    
    @staticmethod
    def __search_type(type:str) -> DocTemplate|None:
        template_types = DocTemplateFactory.__docTemplate_subclasses()
        
        find_type = [t() for t in template_types if type==t().get_id_signature()]
        return find_type[0] if find_type else None   
