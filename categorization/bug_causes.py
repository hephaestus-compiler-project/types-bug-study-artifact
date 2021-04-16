class BugCause():
    """A base class for bug causes.
    """
    name = ""

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()


class Subcategory():
    """A base class for the bug cause sub-categories.

    For example, Inference is a sub-category of type-related bugs.
    """
    name = ""
    category = None

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()


class TypeRelatedBugs(BugCause):
    """Type-Related Bugs.

    A type operation of the compiler is not implemented correctly.

    Subcategories:
        - Incorrect Type Inference & Substitution
        - Incorrect Type Transformation & Coercion
        - Incorrect Type Comparison & Bound Computation
    """
    name = "Type-related Bugs"


class Inference(Subcategory):
    """Incorrect Type Inference & Type Variable Substitution.
    """
    name = "Incorrect Type Inference & Substitution"
    category = TypeRelatedBugs()


class Approximation(Subcategory):
    """Incorrect Type Transformation / Coercion.
    """
    name = "Incorrect Type Transformation / Coercion"
    category = TypeRelatedBugs()


class TypeComparison(Subcategory):
    """Incorrect Type Comparison & Bound Computation.
    """
    name = "Incorrect Type Comparison & Bound Computation"
    category = TypeRelatedBugs()


class SemanticAnalysisBugs(BugCause):
    """Semantic Analysis Bugs.

    Subcategories:
        - Missing Validation Checks
        - Incorrect Analysis Mechanics
    """
    name = "Semantic Analysis Bugs"


class IncorrectAnalysisMechanics(Subcategory):
    """Incorrect Analysis Mechanics.
    """
    name = "Incorrect Analysis Mechanics"
    category =  SemanticAnalysisBugs()


class MissingValiationChecks(Subcategory): # OtherSemanticChecking Declarations
    """Missing Validation Checks.
    """
    name = "Missing Validation Checks"
    category =  SemanticAnalysisBugs()


class ResolutionEnvironment(BugCause):
    """Resolution Bugs

    Subcategories:
        - Resolution
        - Environment
    """
    name = "Resolution Bugs"


class Resolution(Subcategory):
    """Resolution Bug.
    """
    name = "Resolution"
    category = ResolutionEnvironment()


class Environment(Subcategory):
    """Environment Bug.
    """
    name = "Environment"
    category = ResolutionEnvironment()



class ErrorReporting(BugCause):
    """Bugs Related to Error Handling & Reporting.
    """
    name = "Bugs Related to Error Handling & Reporting"


class Transformation(BugCause):
    """AST Transformation Bugs.
    """
    name = "AST Transformation Bugs"
