from interprete_functions import *

if __name__ == '__main__':
    # Reading file
    with open('code.my') as code:
        code = code.readlines()

    # Syntax analyze and run code
    i = 0
    count = 0
    condition_stack = Stack()
    loop_stack = Stack()
    while i < len(code):
        if isinstance(code[i], str):
            code[i] = code[i].strip()

        if '}' in code[i]:                     # End of scope
            scopes.pop()
            if condition_stack.top()[1]:
                condition_stack.pop()
                count -= 1

        elif 'other' in code[i]:               # else case
            if not condition_stack.top()[0]:
                raise SyntaxError('Other without Check')
            scopes.append({})
            if condition_stack.top()[1]:                         # if else case then does this
                count += 1
                i += 1
                continue
            else:                                       # if not else case then passes else
                while i < len(code) - 1:
                    i += 1
                    code[i] = code[i].strip().split(' ')
                    if code[i][0] in ('check', 'other', 'step', 'till'):
                        count += 1

                    if code[i][0].startswith('}'):
                        if count == 0:
                            condition_stack.pop()
                            scopes.pop()
                            break
                        else:
                            count -= 1

        else:
            if code[i] is None or code[i] == ['']:
                i += 1
                continue
            code[i] = analyze_code(code[i])
            a = run_line(code[i])

            if a != 0:
                condition_stack.push([True, False])
                scopes.append({})

            if a == 2:
                condition_stack.top()[1] = True
                count = 0
                while i < len(code):
                    i += 1
                    code[i] = code[i].strip().split(' ')

                    if code[i][-1] == '{':
                        count += 1

                    if code[i][0] == '}' or code[i][0] == '}\n':
                        if count == 0:
                            scopes.pop()
                            break
                        else:
                            count -= 1

            elif a == 3:
                check_line = i
                first_loop = True

                index1 = code[i].index(':')
                index2 = code[i].index(':', index1 + 1)

                i += 1
                while check_function(['check'] + code[check_line][index1 + 1: index2] + ['{']) == 1:
                    while '}' not in code[i]:
                        if first_loop:
                            code[i] = code[i].strip()
                            code[i] = analyze_code(code[i])
                            a = run_line(code[i])
                            first_loop = False
                        else:
                            if isinstance(code[i], str):
                                code[i] = code[i].strip().split(' ')
                            a = run_line(code[i])
                        i += 1
                        if code[i] is None:
                            i += 1

                    i = check_line + 1
                    assignment_function(code[check_line][index2 + 1:-2])

            elif a == 4:
                check_line = i
                first_loop = True
                i += 1

                while check_function(['check'] + code[check_line][2:-2] + ['{']) == 1:
                    i = check_line + 1
                    if not code[i]:
                        i += 1
                    if not code[i]:
                        i += 1
                    while '}' not in code[i]:
                        if first_loop:
                            code[i] = code[i].strip()
                            code[i] = analyze_code(code[i])

                        a = run_line(code[i])
                        i += 1
                        if code[i] is None:
                            i += 1
                    first_loop = False

        i += 1

    # Output the result to 'output.txt'
    with open('output.txt', 'r') as out:
        print(out.read())

    # Clear the content of 'output.txt'
    with open('output.txt', 'w') as out:
        out.write('')
