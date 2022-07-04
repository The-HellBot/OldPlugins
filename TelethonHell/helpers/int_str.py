# pass a string to convert it into integers
async def make_int(str_input):
    str_list = str_input.split(" ")
    int_list = []
    for x in str_list:
        int_list.append(int(x))
    return int_list


# pass a integer list to convert it into string
async def make_str(int_input):
    int_list = int_input
    str_list = []
    for x in int_list:
        str_list.append(str(x))
    str_out = " ".join(str_list)
    return str_out
