import random
knowntypes = (
    "i1", "i2", "i3", "i4", "i5", "i6", "i7", "i8", "i16", "i32", "i64", "i128",
    "i256", "i512", "i1024"
)

def genmangle():
    qwp = list("CHRONICLES_BY_NDRAEY___I_TRIED_TO_MAKE_OWN_COMPILER_WITH_LLVM_ABCDEFGHIJKLMNOPQRSTUVWXYZ_LUCARIO_PIKACHU_BULBASAUR")
    c = "CV_"
    for i in range(15):
        c += qwp[random.randint(0,len(qwp)-1)]
    return c

def gen_llvm_type_align(typ):
    t = typ
    if t[0] == "i":
        t = int(t[1:])
    return t//8

def gen_llvm_function_snippet(typ, name, generated_arguments, llvm_code):
    code = f"define {typ} @{name}({generated_arguments}) "
    code += "{\n"
    for i in llvm_code.split("\n"):
        code += "\t"+i+"\n"
    code += "}"
    return code

def gen_llvm_allocate(name, typ, align=None):
    return f"%{name} = alloca {typ}{', align '+align if align else ''}"

def gen_llvm_variable(typ, name):
    return gen_llvm_allocate(name, typ)

def gen_llvm_getelementptr(varset, typ, ptrval, idxtyp, idx1, idx2=None, inbounds=False):
    return f"%{varset} = getelementptr {'inbounds ' if inbounds else ''}{typ}, {typ}* {ptrval}, {idxtyp} {idx1}{f', {idxtyp} {idx2}' if idx2!=None else ''}"

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

def gen_llvm_array_of(count, typ):
    return f"[{count} x {typ}]"

def gen_llvm_return(typ, value=None):
    return f"ret {typ}{' '+str(value) if value!=None else ''}"

def gen_llvm_call(typ, name, args):
    return f"ret {typ} @{name}({args})"

def gen_llvm_set_array_element(arrayelemscount, arrayelemstype, name, idxtype, idx, value):
    mng = genmangle()
    code = ""
    code += gen_llvm_getelementptr(mng, gen_llvm_array_of(arrayelemscount, arrayelemstype),
                                   name, idxtype, 0, idx, True)+"\n"
    code += gen_llvm_set_variable(arrayelemstype, arrayelemstype+"*", mng, value)+"\n"
    return code, mng

def gen_llvm_set_array_element_pointer(arrayelemscount, arrayelemstype, name, idxtype, idx, value):
    mng = genmangle()
    code = ""
    code += gen_llvm_getelementptr(mng, arrayelemstype, name, idxtype, idx, None, True)+"\n"
    code += gen_llvm_set_variable(arrayelemstype, arrayelemstype+"*", mng, value)+"\n"
    return code, mng

def gen_llvm_struct(name, types):
    return f"%{name} = type "+"{ "+', '.join(types)+" }"

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
            if arith:
                pass
                # Error!
            arith = True
            sign = elem
        else:
            if not arith:
                pass
                # Error;
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

def gen_llvm_set_string(arraylength, arraytype, name, value):
    code = ""
    for n, i in enumerate(value):
        code += gen_llvm_set_array_element(arraylength, arraytype, name, "i32", n, ord(i))[0]
    addcode, mangled = gen_llvm_set_array_element(arraylength, arraytype, name, "i32", n+1, 0)
    code += addcode+"\n"

    return code, mangled

def gen_llvm_set_string_pointer(arraylength, arraytype, name, value):
    code = ""
    for n, i in enumerate(value):
        code += gen_llvm_set_array_element_pointer(arraylength, arraytype, name, "i32", n, ord(i))[0]
    addcode, mangled = gen_llvm_set_array_element_pointer(arraylength, arraytype, name, "i32", n+1, 0)
    code += addcode+"\n"

    return code, mangled

if __name__=="__main__":
    # Firstly, allocating memory for variable
    outercode = "declare i32 @puts(i8* noundef) nounwind\n\n"
    code = ""

    '''
    code += gen_llvm_variable("i32", "test")+"\n"
    # Next, we parsing expression and generating code for LLVM
    # Note: We should mangle result variable, because LLVM doesn't support reassignation
    addcode, mangled = gen_llvm_expression("i32", "test", ['72','+','8','+','9','+','4'])
    code += addcode+"\n"

    # Generating second variable
    code += gen_llvm_variable("i32","hello")+"\n"
    # Parsing and generating (it's last expression, ignoring mangled variable) --------\
    code += gen_llvm_expression("i32", "hello", ["%"+mangled, '+', '1'])[0]+"\n" # <---/
    '''

    # Equivalent to: int main() { char array[16]; array[0] = 'N'; ... puts(array);}

    code += gen_llvm_allocate("array", gen_llvm_array_of(14, "i8"))+"\n"
    addcode, mangled = gen_llvm_set_string(14, "i8", "%array", "Hello, World!")
    code += addcode+"\n"
    
    code += gen_llvm_getelementptr("totalarr", gen_llvm_array_of(14, "i8"),
                                   "%array", "i32", 0, 0, True)+"\n"
    code += "call i32 @puts(i8* %totalarr)\n"
    # We using a function, so we should return from it
    code += gen_llvm_return("i32", 0)
    # Wrapping our code into function
    print(outercode+gen_llvm_function_snippet("i32", "main", "", code))
    print("!llvm.ident = !{!1}")
    print("!1 = !{!\"Chronicles compiler v0.0.1 by NDRAEY\"}")
