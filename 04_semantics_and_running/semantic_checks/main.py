# all semantics schecks are implemented in this file

from semantics_common import SemData


def run_program(tree, semdata, local_vars):
    semdata.old_stacks = []
    semdata.stack = []
    eval_node(tree, semdata, local_vars)


def eval_node(node, semdata, local_vars):
    # symtbl = semdata.symtbl
    nodetype = node.nodetype
    if nodetype == 'program':
        # Copy and store current stack
        semdata.old_stacks.append(semdata.stack.copy())
        eval_node(node.child_vars, semdata, local_vars)
        eval_node(node.child_return, semdata, local_vars)
        semdata.stack = semdata.old_stacks.pop()
        return None
    elif nodetype == 'regexp':
        for i in node.children_vars:
            eval_node(i, semdata, local_vars)
    elif nodetype == 'variable_defintion':
        if (len(local_vars) == 0):
            try:
                semdata.stack.index(node.value)
                print("\nVariable {0} already exists!\n".format(node.value))
            except:
                semdata.stack.append(node.value)
                eval_node(node.child_expr, semdata, local_vars)
        else:
            try:
                local_vars.index(node.value)
                print("\nVariable {0} already exists!\n".format(node.value))
            except:
                local_vars.append(node.value)
                eval_node(node.child_expr, semdata, local_vars)
    elif nodetype == 'return_value':
        eval_node(node.child_expr, semdata, local_vars)
        local_vars.clear()
    elif nodetype == 'simple_expression':
        eval_node(node.child_term, semdata, local_vars)
    elif nodetype == 'term':
        for i in node.children_factors:
            eval_node(i, semdata, local_vars)
    elif nodetype == 'factor':
        eval_node(node.child_atom, semdata, local_vars)
    elif nodetype == 'atom_var':
        if (len(local_vars) == 0):
            try:
                semdata.stack.index(node.value)
                semdata.stack.append(node.value)
            except:
                print("\nVariable {0} doesn't exist!\n".format(node.value))
        else:
            try:
                local_vars.index(node.value)
                local_vars.append(node.value)
            except:
                print("\nVariable {0} doesn't exist!\n".format(node.value))
    elif nodetype == 'atom_const':  # constant definitions allowed only in global scope
        try:
            semdata.stack.index(node.value)
            semdata.stack.append(node.value)
        except:
            print("\nConstant {0} doesn't exist!\n".format(node.value))
    elif nodetype == 'constant_definition':
        try:
            semdata.stack.index(node.value)
            print("\nConstant {0} already exists!\n".format(node.value))
        except:
            semdata.stack.append(node.value)
    elif nodetype == 'function_definition_empty':

        if (len(local_vars) != 0):
            print("\nNo function definitions inside the other function!\n")
        else:
            try:
                semdata.stack.index(node.value)
                print("\nFunction {0} is already defined!\n".format(node.value))
            except:
                local_vars.append(node.value)  # to know that we are now inside this function
                semdata.stack.append(node.value)
                eval_node(node.child_formals, semdata, local_vars)
                eval_node(node.child_return, semdata, local_vars)
    elif nodetype == 'function_definition_with_vars':
        if (len(local_vars) != 0):
            print("\nNo function definitions inside the other function!\n")
        else:
            try:
                semdata.stack.index(node.value)
                print("\nFunction {0} is already defined!\n".format(node.value))
            except:
                local_vars.append(node.value)
                semdata.stack.append(node.value)
                eval_node(node.child_formals, semdata, local_vars)
                eval_node(node.child_return, semdata, local_vars)
    elif nodetype == 'formals':
        eval_node(node.child_params, semdata, local_vars)
    elif nodetype == 'var_list':
        for var in node.children_vars:
            eval_node(var, semdata, local_vars)
    elif nodetype == 'variable':
        try:
            semdata.stack.index(node.value)
            print("\nVariable {0} is already defined! It can't be used as a parameter!\n".format(node.value))
        except:
            local_vars.append(node.value)
            # semdata.stack.append(node.value)
    elif nodetype == 'arguments':
        eval_node(node.child_expr, semdata, local_vars)
    elif nodetype == 'constIDENT':
        try:
            semdata.stack.index(node.value)
            semdata.stack.append(node.value)
            if (len(local_vars) != 0):
                local_vars.append(node.value)
        except:
            print("\nUndefined constant {0}!\n".format(node.value))
    elif nodetype == 'function_call':
        try:
            semdata.stack.index(node.value)
            if (len(local_vars) != 0):
                local_vars.append(node.value)
            else:
                semdata.stack.append(node.value)
            eval_node(node.child_args, semdata, local_vars)
        except:
            print("\nFunction {0} is undefined!\n".format(node.value))
            eval_node(node.child_args, semdata, local_vars)
    else:
        None


# import sys
import tokenizer
import tree_generation
import tree_print

parser = tree_generation.parser

import semantics_check


def main():
    while True:
        command = input()
        task = command.split(' ')[0]
        if (task == "-h" or task == "--help"):
            print(
                "usage: main.py [-h] [--who | -f FILE]\n-h, --help  show this help message and exit\n --who  print out student IDs and NAMEs of authors\n -f FILE, --file FILE  filename to process")
            break
        elif (task == "--who"):
            print("Evgeniia Onosovskaia, 281251")
        elif ((task == "-f" or task == "--file") and len(command.split(' ')) == 2):
            file_name = command.split(' ')[1]
            ast_tree = tree_generation.parse_result(file_name)

            semdata = SemData()
            local_vars = []
            semdata.in_function = None
            # semantics_check.semantic_checks(ast_tree, semdata)
            # tree_print.treeprint(ast_tree)
            run_program(ast_tree, semdata, local_vars)
        else:
            print("Incorrect command, please try again!")


main()