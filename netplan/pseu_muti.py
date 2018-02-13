output1 = {"output":[1,2,3,4,5],"forecast":9,"d":15}
output2 = {"output":[1,2,3,4,5],"forecast":12,"d":16}
output3 = {"output":[1,2,3,4,5],"forecast":9,"d":13}

output_dict = {"fun1":output1,"fun2":output2,"fun3":output3}

fun_choose = {"fun1":0,"fun2":1,"fun3":1}

for f , v in fun_choose.items():
	if v == 0 : output_dict.pop(f)

best_fun = ""

d = None

for f,v in output_dict.items():
	if d == None : d = v['d'] ; best_fun = f
	if v['d'] < d : best_fun = f

result = output_dict[best_fun]["forecast"]

print(result)