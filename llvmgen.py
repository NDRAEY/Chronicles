import random
knowntypes = (
    "i1", "i2", "i3", "i4", "i5", "i6", "i7", "i8", "i16", "i32", "i64", "i128",
    "i256", "i512", "i1024"
)

def genmangle():
    qwp = list("CHRONICLES_BY_NDRAEY___I_TRIED_TO_MAKE_OWN_COMPILER_WITH_LLVM_ABCDEFGHIJKLMNOPQRSTUVWXYZ_LUCARIO_PIKACHU_BULBASAUR")
    c = "CV_"
    for i in range(20):
        c += qwp[random.randint(0,len(qwp)-1)]
    return c

def gen_llvm_type_align(typ):
    t = typ
    if t[0] in ("u", "i"):
        t = int(t[1:])
    return t//8

def gen_llvm_function_snippet(typ, name, generated_arguments, llvm_code):
    code = f"define {typ} @{name}({generated_arguments}) "
    code += "{\n"
    for i in llvm_code.split("\n"):
        code += "\t"+i+"\n"
    code += "}"
    return code

def gen_llvm_variable(typ, name):
    return f"%{name} = alloca {typ}, align {gen_llvm_type_align(typ)}"

def gen_llvm_set_variable(typ, type_to, name, value):
    return f"store {typ} {value}, {type_to} %{name}"

def gen_llvm_operation_add(varset, varget, typ, value):
    return f"%{varset} = add nsw {typ} %{varget}, {value}"

def gen_llvm_operation_sub(varset, varget, typ, value):
    return f"%{varset} = sub nsw {typ} %{varget}, {value}"

def gen_llvm_operation_mul(varset, varget, typ, value):
    return f"%{varset} = mul nsw {typ} %{varget}, {value}"

def gen_llvm_operation_div(varset, varget, typ, value):
    return f"%{varset} = sdiv {typ} %{varget}, {value}"

def gen_llvm_operation_shl(varset, varget, typ, value):
    return f"%{varset} = shl {typ} %{varget}, {value}"

def gen_llvm_operation_shr(varset, varget, typ, value):
    return f"%{varset} = shr {typ} %{varget}, {value}"

def gen_llvm_load(varset, typ, typload, varget):
    return f"%{varset} = load {typ}, {typload} %{varget}"

def gen_llvm_return(typ, value=None):
    return f"ret {typ}{' '+value if value else ''}"

def gen_llvm_expression(typ, varname, expression):
    code = ""
    arithsigns = ['+','-','/','*']
    i = 0
    arith = False
    sign = None
    firsttime = False

    curmng = varname

    code += gen_llvm_set_variable(typ, typ+"*", varname, expression[0])+"\n"

    i += 1
    
    while i<len(expression):
        elem = expression[i]

        if elem in arithsigns:
            arith = True
            sign = elem
        else:
            if sign=="+":
                if not firsttime:
                    mangled = genmangle()
                    code += gen_llvm_load(mangled, typ, typ+"*", curmng)+"\n"
                    mangled2 = genmangle()
                    code += gen_llvm_operation_add(mangled2, mangled, typ, elem)+"\n"
                else:
                    mangled2 = genmangle()
                    code += gen_llvm_operation_add(mangled2, curmng, typ, elem)+"\n"
                code += gen_llvm_set_variable(typ, typ+"*", varname, "%"+mangled2)+"\n"
                curmng = mangled2
            elif sign=="-":
                if not firsttime:
                    mangled = genmangle()
                    code += gen_llvm_load(mangled, typ, typ+"*", curmng)+"\n"
                    mangled2 = genmangle()
                    code += gen_llvm_operation_sub(mangled2, mangled, typ, elem)+"\n"
                else:
                    mangled2 = genmangle()
                    code += gen_llvm_operation_sub(mangled2, curmng, typ, elem)+"\n"

                code += gen_llvm_set_variable(typ, typ+"*", varname, "%"+mangled2)+"\n"
                curmng = mangled2
            elif sign=="*":
                if not firsttime:
                    mangled = genmangle()
                    code += gen_llvm_load(mangled, typ, typ+"*", curmng)+"\n"
                    mangled2 = genmangle()
                    code += gen_llvm_operation_mul(mangled2, mangled, typ, elem)+"\n"
                else:
                    mangled2 = genmangle()
                    code += gen_llvm_operation_mul(mangled2, curmng, typ, elem)+"\n"
                code += gen_llvm_set_variable(typ, typ+"*", varname, "%"+mangled2)+"\n"
                curmng = mangled2
            elif sign=="/":
                if not firsttime:
                    mangled = genmangle()
                    code += gen_llvm_load(mangled, typ, typ+"*", curmng)+"\n"
                    mangled2 = genmangle()
                    code += gen_llvm_operation_div(mangled2, mangled, typ, elem)+"\n"
                else:
                    mangled2 = genmangle()
                    code += gen_llvm_operation_div(mangled2, curmng, typ, elem)+"\n"
                code += gen_llvm_set_variable(typ, typ+"*", varname, "%"+mangled2)+"\n"
                curmng = mangled2
            firsttime = True
        i+=1
    return code, curmng

if __name__=="__main__":
    # Firstly, allocatong memory for variable
    code = gen_llvm_variable("i32", "test")+"\n"
    # Next, we parsing expression and generating code for LLVM
    # Note: We should mangle result variable, because LLVM doesn't support reassignation
    addcode, mangled = gen_llvm_expression("i32", "test", ['72','+','8','+','9','+','4'])
    code += addcode+"\n"

    # Generating second variable
    code += gen_llvm_variable("i32","hello")+"\n"
    # Parsing and generating (it's last expression, ignnoring mangled variable) --\
    code += gen_llvm_expression("i32", "hello", ["%"+mangled, '+', '1'])[0] # <---/
    # We using a function, so we should return from it
    code += gen_llvm_return("void")
    # Wrapping our code into function
    print(gen_llvm_function_snippet("void", "main", "", code))
