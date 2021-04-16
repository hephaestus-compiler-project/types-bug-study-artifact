class Bug:
    """Base class to represent a bug.

    This class contains the following fields:

    * bug_id:     Attributes
    ----------
    bug_id : str
        The bug_id is the unique identifier of the bug. For Scala2 and
        Dotty bugs, we use scala or dotty as a prefix, a dash, and the GitHub
        issue id.
    characteristics : list[Characteristic]
        A list of program characteristics that exist in the test case.
    test_case_correct : bool
        True if the test case is compilable, otherwise False.
    symptom : Symptom
        The symptom of the bug.
    root_cause: RootCause
        The cause that introduced the bug.
    category: Category
        The bug cause category.
    lines: int
        Deprecated
    """
    language = ""

    def __init__(self, bug_id, characteristics, test_case_correct, symptom,
                 root_cause, category, lines=0):
        self.bug_id = bug_id
        self.characteristics = characteristics
        self.test_case_correct = test_case_correct
        self.symptom = symptom
        self.root_cause = root_cause
        self.category = category
        self.lines = 0 # test case loc

    def __repr__(self):
        return "Bug: {} (\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n)".format(
            self.bug_id,
            "Characteristics: \n\t\t" + "\n\t\t".join([str(c) for c in self.characteristics]),
            "Test Case Correct: " + str(self.test_case_correct),
            "Symptom: " + str(self.symptom),
            "Root Cause: " + str(self.root_cause),
            "Category: " + str(self.category),
            "Test case loc: " + str(self.lines)
        )

    def __str__(self):
        return self.__repr__()


class KotlinBug(Bug):
    """Class to represent Kotlin Bugs.
    """
    language = "Kotlin"
    compiler = "kotlinc"


class GroovyBug(Bug):
    """Class to represent Groovy Bugs.
    """
    language = "Groovy"
    compiler = "groovyc"


class JavaBug(Bug):
    """Class to represent Java Bugs.
    """
    language = "Java"
    compiler = "javac (openjdk)"


class ScalaBug(Bug):
    """Class to represent Scala2 Bugs.
    """
    language = "Scala"
    compiler = "scala"


class ScalaDottyBug(ScalaBug):
    """Class to represent Dotty Bugs.
    """
    compiler = "dotty"
