#! /usr/bin/env python3
import json
import argparse
from pprint import pprint


LANGUAGES=["Java", "Kotlin", "Groovy", "Scala"]
SYMPTOMS = [
    "Unexpected Compile-Time Error",
    "Internal Compiler Error",
    "Unexpected Runtime Behavior",
    "Compilation Performance Issue",
    "Misleading Report"
]
BUG_CAUSES = [
    "Type-related Bugs",
    "Semantic Analysis Bugs",
    "Resolution Bugs",
    "Bugs Related to Error Handling & Reporting",
    "AST Transformation Bugs"
]
CHAR_CATEGORIES = [
    'Parametric polymorphism',
    'OOP features',
    'Type system features',
    'Standard library',
    'Functional programming',
    'Standard features',
    'Type inference',
    'Other'
]
CHARS=[
    'Parameterized class',
    'Parameterized type',
    'Parameterized function',
    'Use-site variance',
    'Bounded type parameters',
    'Higher-kinded types',
    'Declaration-site variance',
    'Inheritance',
    'Sealed Classes',
    'Nested class',
    'Anonymous classes',
    'Overriding',
    'Static Method',
    'Overloading',
    'Access modifiers',
    'Multiple implements',
    'Value classes',
    'Singleton object',
    'This',
    'Case classes',
    'Self types',
    'Delegation',
    'Property reference',
    'Data classes',
    'Secondary constructor',
    'Property',
    'Subtyping',
    'Primitive types',
    'Wildcard type',
    'Intersection types',
    'Dependent types',
    'Type alias',
    'Nothing',
    'Algebraic Data Types',
    'Type Lambdas',
    'Type Projection',
    'Opaque types',
    'Union types',
    'Mixins',
    'Match types',
    'Nullable types',
    'Function API',
    'Reflection API',
    'Collection API',
    'Stream API',
    'Coroutines API',
    'Delegation API',
    'Lambda',
    'Function reference',
    'Functional interface',
    'Function type',
    'Eta expansion',
    'Conditionals',
    'Array',
    'Import',
    'Cast',
    'Variable arguments',
    'Try/Catch',
    'Loops',
    'Arithmetic Expressions',
    'Augmented Assignment Operator',
    'Enums',
    'Type argument inference',
    'Variable type inference',
    'Parameter type inference',
    'Flow typing',
    'Return type inference',
    'Builder inference',
    'Type annotations',
    'Java interoperability',
    'Implicits',
    'Erased parameters',
    'Call by name',
    'Default Initializer',
    'Option types',
    'Pattern matching',
    'Inline',
    'Named arguments',
    'Extension function / property',
    'Elvis operator',
    'Null assertion',
    'Safe navigation operator',
    'With',
    'Template string'
]
URL_LOOKUP={
    "JDK": "https://bugs.openjdk.java.net/browse/JDK-",
    "KT": "https://youtrack.jetbrains.com/issue/KT-",
    "GROOVY": "https://issues.apache.org/jira/browse/GROOVY-",
    "Scala2": "https://github.com/scala/bug/issues/",
    "Dotty": "https://github.com/lampepfl/dotty/issues/"
}


def get_args():
    parser = argparse.ArgumentParser(
        description='Query bugs'
    )
    parser.add_argument("data", help="JSON with bugs.")
    parser.add_argument(
        "-l", "--languages",
        default=LANGUAGES,
        nargs="*",
        choices=LANGUAGES,
        help="Select bugs from specific languages."
    )
    parser.add_argument(
        "-b", "--bug-causes",
        default=BUG_CAUSES,
        nargs="*",
        choices=BUG_CAUSES,
        help="Select bugs with specific bug causes"
    )
    parser.add_argument(
        "-s", "--symptoms",
        default=SYMPTOMS,
        nargs="*",
        choices=SYMPTOMS,
        help="Select bugs with specific symptoms."
    )
    parser.add_argument(
        "-C", "--char-categories",
        default=CHAR_CATEGORIES,
        nargs="*",
        choices=CHAR_CATEGORIES,
        help="Select bugs with specific characteristics' categories."
    )
    parser.add_argument(
        "-c", "--characteristics",
        default=CHARS,
        nargs="*",
        choices=CHARS,
        help="Select bugs with specific characteristics."
    )
    parser.add_argument(
        "--is-correct",
        action='store_true',
        help="Select bugs that their test cases are correct"
    )
    parser.add_argument(
        "--is-incorrect",
        action='store_true',
        help="Select bugs that their test cases are incorrect"
    )
    parser.add_argument(
        "-u", "--print-url",
        action='store_true',
        help="Print only the URLs of the bug reports"
    )
    parser.add_argument(
        "-U", "--url",
        action='store_true',
        help="Replace ID with URL"
    )
    parser.add_argument(
        "-o", "--output",
        help="File to save the output"
    )
    return parser.parse_args()


def get_url(k):
    lang = k.split('-')[0]
    bug_id = k.split('-')[1]
    return URL_LOOKUP[lang] + bug_id

def main():
    args = get_args()
    with open(args.data, 'r') as f:
        data = json.load(f)
    data = {k:v for k,v in data.items()
            if v['language'] in args.languages}
    data = {k:v for k,v in data.items()
            if v['bug_cause']['category'] in args.bug_causes}
    data = {k:v for k,v in data.items()
            if v['symptom'] in args.symptoms}
    data = {k:v for k,v in data.items()
            if any(c for c in v['chars']['categories']
                   if c in args.char_categories)}
    data = {k:v for k,v in data.items()
            if any(c for c in v['chars']['characteristics']
                   if c in args.characteristics)}
    if args.is_correct:
        data = {k:v for k,v in data.items()
                if v['is_correct']}

    if args.is_incorrect:
        data = {k:v for k,v in data.items()
                if not v['is_correct']}
    if args.url:
        data = {get_url(k):v for k,v in data.items()}
    if args.print_url:
        if args.output:
            with open(args.output, 'w') as f:
                for k in data.keys():
                    f.write("%s\n" % k)
        else:
            for k in data.keys():
                print(get_url(k))
    else:
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(data, f)
        else:
            pprint(data)


if __name__ == "__main__":
    main()
